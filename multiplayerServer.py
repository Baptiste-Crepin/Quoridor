# serveur with threads for multiple clients
import queue
import socket
import sys
import threading
import pickle
import time


def boutton(connected):
    message = True
    pickeled_message = pickle.dumps(message)
    time.sleep(0.5)
    for i in range(len(connected)):
        print("sending starter message to client  :", i)
        connected[i].send(pickeled_message)


class ThreadClient(threading.Thread):

    def __init__(self, connexion, idd, queue, connected, nbBots):
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.start()
        self.idc = idd
        self.queue = queue
        self.connected = connected
        self.nbBots = nbBots

    def getConnected(self):
        return self.connected

    def nextClient(self) -> int:
        current_client = self.queue.get()
        print(current_client)
        current_client = (
            current_client + 1) % (len(self.connected) + self.nbBots)
        self.queue.put(current_client)
        self.queue.task_done()
        return current_client

    def handleGameState(self, message: list) -> None:
        message[2] = self.nextClient()
        pickeled_message = pickle.dumps(message)
        for i in range(len(self.connected)):
            self.connected[i].send(pickeled_message)

    def handleChatMessage(self, message: list) -> None:
        print("chat not implemented yet")

    def handleQuestion(self, message: list) -> None:
        print("? not implemented yet")

    def handleEmpty(self, message: list) -> None:
        print("\"\" not implemented yet")

    def run(self) -> None:
        '''
        gets the message from one client and sends it to all the clients
        '''
        message_handlers = {
            'game_state': self.handleGameState,
            'chat': self.handleChatMessage,
            '?': self.handleQuestion,
            '': self.handleEmpty,
        }

        while True:
            try:
                received_message = self.connexion.recv(4096)
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
                raise Exception("Player disconnected while in game")

        # self.connexion.close()


def acceptConnexions(mySocket, init, initializedQueue,):
    '''
    accepts the connexions of the clients and creates a thread for each of them to handle the messages
    '''
    nbPlayer = init[3]
    nbBots = init[4]
    connected = {}

    mySocket.listen(nbPlayer)
    while nbPlayer > len(connected):
        connexion = mySocket.accept()[0]

        connected[init[0]] = connexion
        ThreadClient(connexion, init[0], initializedQueue, connected, nbBots)

        init_msg = pickle.dumps(init)
        connexion.send(init_msg)

        print("Client", init[0], "connected, awaiting other players")
        init[0] += 1
    boutton(connected)


def handle_client_request(data, client_address, dsock, lobbyInfo):
    if data == b"SERVER_DISCOVERY_REQUEST":
        print("incomming discovery packet from:", client_address)
        # Convert the server IP address to binary format
        response = pickle.dumps(lobbyInfo)
        dsock.sendto(response, client_address)
        print("handeling request")


def discoveryServer(dsock, lobbyInfo):
    while True:
        data, addre = dsock.recvfrom(1024)
        handle_client_request(data, addre, dsock, lobbyInfo)


def createServer(width, nbBarrier, nbPlayer, nbBots, name, port=45678):
    '''
    creates a server with the given parameters
    '''

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
                 'remining': 1
                 }

    initializedQueue = queue.Queue()
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

    print(f"\n\n\n{'='*15} Server |{host} : {port}| on {'='*15}\n\n")
    discothread = threading.Thread(
        target=discoveryServer, args=(discoSock, lobbyInfo))
    discothread.start()

    acceptConnexions(serverSocket, init, initializedQueue)


if __name__ == "__main__":
    width = 5
    nbBarrier = 10
    nbPlayer = 2
    nbBot = 0
    serverName = "test"
    createServer(width, nbBarrier, nbPlayer, nbBot, serverName)
