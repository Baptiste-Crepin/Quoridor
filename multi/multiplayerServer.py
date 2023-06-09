# serveur with threads for multiple clients
import pickle
import queue
import socket
import sys
import threading
import time
from typing import Any


class serverSubThread(threading.Thread):
    """ class that creates a thread for each client to handle incoming data at any time  """

    def __init__(self, connection: socket.socket, id: int, queue: queue.Queue[int], connected: dict[int, socket.socket],
                 nbBots: int, discostop: threading.Event) -> None:
        threading.Thread.__init__(self)
        self.connection = connection
        self.idc = id
        self.queue = queue
        self.connected = connected
        self.nbBots = nbBots
        self.start()
        self.stopEvent = threading.Event()
        self.discostop = discostop

    def stop(self):
        self.stopEvent.set()
        self.discostop.set()

    def stopped(self):
        return self.stopEvent.is_set()

    def getConnected(self):
        return self.connected

    def nextClient(self) -> int:
        """retrieves the current player from the queue, returns the next one"""
        current_client = self.queue.get()
        print(current_client, '-->', ((current_client + 1) % (len(self.connected) + self.nbBots)), " total clients :",
              len(self.connected) + self.nbBots)
        current_client = (current_client + 1) % (len(self.connected) + self.nbBots)
        self.queue.put(current_client)
        self.queue.task_done()
        return current_client

    def handleGameState(self, message: list[Any]) -> None:
        """defines the next player then add it to the current message for the client to set it as the current player"""
        message[2] = self.nextClient()
        pickeled_message = pickle.dumps(message)
        for i in range(len(self.connected)):
            self.connected[i].send(pickeled_message)

    def handleChatMessage(self, message: list[Any]) -> None:
        print("chat not implemented yet")

    def handleEnd(self, message: list[
        Any]) -> None:  # recieved the end game message send the current player to all clients then ends the server thread
        pickeled_message = pickle.dumps(message)
        for i in range(len(self.connected)):
            self.connected[i].send(pickeled_message)
        time.sleep(0.2)
        if self.is_alive():
            print("Server side Thread is still alive; stoping it now.")
            self.stop()
        while self.is_alive():
            time.sleep(1)

    def run(self) -> None:
        '''
        gets the message from one client and sends it to all the clients
        '''
        message_handlers = {
            'game_state': self.handleGameState,
            'chat': self.handleChatMessage,
            'game_end': self.handleEnd
        }

        while True:
            try:
                received_message = self.connection.recv(4096)
                message = pickle.loads(received_message)

                message_type = message[0]
                if message_type in message_handlers:
                    message_handlers[message_type](message)
                else:
                    print("unexpected data in header can't interpret packet")

            except Exception as e:
                print("connection error:")
                print(e)
                print(self.connected)
                raise Exception("Player disconnected while in game") from e

        # self.connection.close()

    @staticmethod
    def starter(connected: dict[int, socket.socket]):
        message = True
        pickeled_message = pickle.dumps(message)
        time.sleep(1)
        for i in range(len(connected)):
            print("sending starter message to client  :", i)
            connected[i].send(pickeled_message)

    @staticmethod
    def roomstatus(connected: dict[int, socket.socket]):
        msg = str(len(connected))
        pickeled_message = pickle.dumps(msg)
        for i in range(len(connected)):
            print("sending ", msg, " message to client  :", i)
            connected[i].send(pickeled_message)


def acceptConnections(mySocket: socket.socket, init: list[int], initializedQueue: queue.Queue[int],
                      stopEvent: threading.Event, lobbyinfos):
    '''
    accepts the connections of the clients and creates a thread for each of them to handle the messages
    '''
    nbPlayer = init[3]
    nbBots = init[4]
    connected = dict[int, socket.socket]()

    mySocket.listen(nbPlayer)
    while nbPlayer > len(connected):
        connection = mySocket.accept()[0]

        connected[init[0]] = connection
        serverSubThread(connection, init[0], initializedQueue, connected, nbBots, stopEvent)

        init_msg = pickle.dumps(init)
        print("sending init msg")
        connection.send(init_msg)
        serverSubThread.roomstatus(connected)
        lobbyinfos["connectedPlayers"] = len(connected)

        print("Client", init[0], "connected, awaiting other players")
        init[0] += 1
    serverSubThread.starter(connected)
    return connected


def handle_client_request(data: bytes, client_address: tuple[str, int], dsock: socket.socket,
                          lobbyInfo: dict[str, Any]):
    if data == b"SERVER_DISCOVERY_REQUEST":
        print("incoming discovery packet from:", client_address)
        # Convert the server IP address to binary format
        response = pickle.dumps(lobbyInfo)
        dsock.sendto(response, client_address)
        print("handling request")


def discoveryServer(dsock: socket.socket, lobbyInfo: dict, stopEvent: threading.Event):
    """ respond to incoming discovery request until stopped"""
    while not stopEvent.is_set():
        data, addre = dsock.recvfrom(1024)
        if stopEvent.is_set():
            break
        handle_client_request(data, addre, dsock, lobbyInfo)


def createServer(width: int, nbBarrier: int, nbPlayer: int, nbBots: int, name: str, port: int = 45678) -> None:
    '''creates a server with the given parameters'''

    ide = 0
    init = [ide, width, nbBarrier, nbPlayer, nbBots]

    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    lobbyInfo = {'discoverymessage': b"SERVER_DISCOVERY_REQUEST",
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
    initializedQueue.put(0)
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
    discothread = threading.Thread(target=discoveryServer, args=(discoSock, lobbyInfo, stopEvent))
    discothread.start()

    acceptConnections(serverSocket, init, initializedQueue, stopEvent, lobbyInfo, )


if __name__ == "__main__":
    width = 5
    nbBarrier = 10
    nbPlayer = 2
    nbBot = 0
    serverName = "test"
    createServer(width, nbBarrier, nbPlayer, nbBot, serverName, )
