# server with threads for multiple clients
import pickle
import queue
import socket
import sys
import threading
import time
from typing import Any

from multi.discoveryServer import SearchServer


class ServerSubThread(threading.Thread):
    """ class that creates a thread for each client to handle incoming data at any time  """

    def __init__(self, connection: socket.socket, id: int, queue: queue.Queue[int], connected: dict[int, socket.socket],
                 nbBots: int, startingPlayer: int) -> None:
        threading.Thread.__init__(self)
        self.connection = connection
        self.startingPlayer = startingPlayer
        self.clientId = id
        self.queue = queue
        self.connected = connected
        self.nbBots = nbBots
        self.stopEvent = threading.Event()
        self.response_event = threading.Event()
        self.start()

    def stop(self):
        self.stopEvent.set()



    def getConnected(self):
        return self.connected

    def nextClient(self) -> int:
        """retrieves the current player from the queue, returns the next one"""
        current_client = self.queue.get()
        print(current_client, '-->', ((current_client + 1) % (len(self.connected) + self.nbBots)), " total clients :",
              len(self.connected) + self.nbBots)
        current_client = (
            current_client + 1) % (len(self.connected) + self.nbBots)
        self.queue.put(current_client)
        self.queue.task_done()
        return current_client

    def handleGameState(self, message: list[Any]) -> None:
        """defines the next player then add it to the current message for the client to set it as the current player"""
        message[2] = self.nextClient()
        pickled_message = pickle.dumps(message)
        for i in range(len(self.connected)):
            self.connected[i].sendall(pickled_message)

    def handleChatMessage(self, message: list[Any]) -> None:
        print("chat not implemented yet")

    def handleEnd(self, message: list[
            Any]) -> None:  # received the end game message send the current player to all clients then ends the server thread
        pickled_message = pickle.dumps(message)
        for i in range(len(self.connected)):
            self.connected[i].sendall(pickled_message)
        time.sleep(0.2)
        while not self.stopEvent.is_set():
            print("Thread is still alive; stopping it now.")
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
                self.stopEvent.set()
            except OSError:
                print(f"Error closing socket: socket already closed")
            time.sleep(0.2)


    def restartMP(self, message: list[Any]) -> None:
        print("restarting the multiplayer for all client")
        pickled_message = pickle.dumps(message)
        for i in range(len(self.connected)):
            self.connected[i].sendall(pickled_message)

    def disconnectMessage(self, message: list[Any]):
        message = ['mpAbort', message]
        pickled_message = pickle.dumps(message)
        for i in range(len(self.connected)):
            self.connected[i].sendall(pickled_message)

    def run(self) -> None:
        '''
        gets the message from one client and sends it to all the clients
        '''
        messageHandlers = {
            'gameState': self.handleGameState,
            'chat': self.handleChatMessage,
            'gameEnd': self.handleEnd,
            'resetGame': self.restartMP
        }

        while not self.stopEvent.is_set():
            try:
                received_message = self.connection.recv(4096)
                message = pickle.loads(received_message)
                message_type = message[0]
                if message_type == 'resetGame':
                    self.connection.setblocking(False)
                if message_type in messageHandlers:
                    messageHandlers[message_type](message)
                else:
                    print("unexpected data in header can't interpret packet")

            except Exception as e:
                print("connection error:")
                print(e)
                self.disconnectMessage(
                    [f"Client {self.clientId} has disconnected."])
                raise Exception("Player disconnected while in game") from e

    @staticmethod
    def starter(connected: dict[int, socket.socket]):
        message = ["starter", True]
        pickled_message = pickle.dumps(message)
        time.sleep(1)
        for i in range(len(connected)):
            print("sending starter message to client  :", i)
            connected[i].sendall(pickled_message)

    @staticmethod
    def roomStatus(connected: dict[int, socket.socket]):
        msg = ["lenConnected", len(connected)]
        pickled_message = pickle.dumps(msg)
        for i in range(len(connected)):
            print("sending ", msg, " message to client  :", i)
            connected[i].sendall(pickled_message)


def acceptConnections(mySocket: socket.socket, init: list[int], initializedQueue: queue.Queue[int],
                      lobbyInfos: dict[str, Any], startingPlayer: int) -> tuple[dict[int, socket.socket],
                                                                                list[ServerSubThread]]:
    '''
    accepts the connections of the clients and creates a thread for each of them to handle the messages
    '''
    nbPlayer = init[3]
    nbBots = init[4]
    connected = dict[int, socket.socket]()

    mySocket.listen(nbPlayer)

    init.append(startingPlayer)
    print(init)
    serverInsances = []
    while nbPlayer > len(connected):
        print("starting player", startingPlayer)
        connection = mySocket.accept()[0]

        connected[init[0]] = connection

        serverInsances.append(ServerSubThread(connection, init[0],
                                              initializedQueue, connected, nbBots, init[5]))
        print("new instance of  subServer:", serverInsances)

        init_msg = pickle.dumps(init)
        print("sending init msg")
        connection.sendall(init_msg)
        lobbyInfos["connectedPlayers"] = len(connected)
        print("Client", init[0], "connected, awaiting other players")
        ServerSubThread.roomStatus(connected)
        init[0] += 1
    # ServerSubThread.starter(connected) this line was meant to send the starter message to all client but is now
    # called by the user
    return connected, serverInsances


def handle_client_request(data: bytes, client_address: tuple[str, int], discoSock: socket.socket,
                          lobbyInfo: dict[str, Any]):
    if data == b"SERVER_DISCOVERY_REQUEST":
        print("incoming discovery packet from:", client_address)
        # Convert the server IP address to binary format
        response = pickle.dumps(lobbyInfo)
        discoSock.sendto(response, client_address)
        print("handling request")


def discoveryServer(discoSock: socket.socket, lobbyInfo: dict[str, Any], stopEvent: threading.Event):
    """ respond to incoming discovery request until stopped"""
    discoSock.settimeout(1)
    try:
        while not stopEvent.is_set():
            try:
                data, address = discoSock.recvfrom(1024)
                handle_client_request(data, address, discoSock, lobbyInfo)
            except socket.timeout:
                # Timeout occurred, check if we need to stop the thread
                continue
    finally:
        # Close the socket here, in the same thread that was using it.
        discoSock.close()
        print("Stopped discovery server")


def createServer(width: int, nbBarrier: int, nbPlayer: int, nbBots: int, name: str, startingPlayer: int, port: int =
                 45678) -> list[ServerSubThread]:
    '''creates a server with the given parameters'''

    ide = 0
    init = [ide, width, nbBarrier, nbPlayer, nbBots]
    host = SearchServer.getSelfHost()

    lobbyInfo = {'discoveryMessage': b"SERVER_DISCOVERY_REQUEST",
                 'ip': host,
                 'port': port,
                 'lobbyName': name,
                 'players': nbPlayer,
                 'width': width,
                 'barriers': nbBarrier,
                 'bots': nbBots,
                 'connectedPlayers': 0
                 }

    initializedQueue = queue.Queue[int]()
    initializedQueue.put(startingPlayer)
    initializedQueue.task_done()

    # --- server creation
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    discoSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        serverSocket.bind((host, port))
        discoSock.bind(('0.0.0.0', 5555))
    except socket.error as e:
        print("error whilst launching server")
        print(e)
        sys.exit()
    print(f"\n\n\n{'=' * 15} Server |{host} : {port}| on {'=' * 15}\n\n")
    stopEvent = threading.Event()
    discoThread = threading.Thread(
        target=discoveryServer, args=(discoSock, lobbyInfo, stopEvent))
    discoThread.start()
    if isinstance(lobbyInfo["connectedPlayers"], int):
        lobbyInfo["connectedPlayers"] += 1

    connections, serverInsances = acceptConnections(serverSocket, init, initializedQueue,
                                                    lobbyInfo, startingPlayer)
    stopEvent.set()
    time.sleep(0.3)
    discoThread.join()
    discoSock.close()
    print("stopped discovery response procedure")

    return serverInsances
