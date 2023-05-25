# serveur avec Thread pour plusieurs clients


import queue
import socket, sys, threading, pickle



hostname = socket.gethostname()

host = socket.gethostbyname(hostname)
# host = 'LocalHost'
port = 45678
client_list = []
i = 0
# created an unbounded queue
q = queue.Queue()
q.put(0)
q.task_done()


# ---------------------------------------------
class ThreadClient(threading.Thread):

    def __init__(self, c, idd):
        threading.Thread.__init__(self)
        self.connexion = c
        self.start()
        self.idc = idd

    def nextClient(self) -> int:
        current_client = q.get()
        print(current_client)
        if current_client < (len(connected) - 1 + nbBots):
            current_client += 1
        else:
            current_client = 0
        q.put(current_client)
        q.task_done()
        return current_client

    def run(self):
        # recuperation du message d'un client
        while 1:

            try:
                msg1 = self.connexion.recv(4096)
                msg = pickle.loads(msg1)
                print("reccu:", msg)
                print(connected[self.idc])

                msg2 = self.nextClient()
                print(msg2)

                print("CONNECTED LIST", connected)

                for i in range(len(connected)):
                    # sends the board to the clients
                    connected[i].send(msg1)
                    # sends current player turn to the clients
                    connected[i].send(pickle.dumps(msg2))



            except Exception as e:
                print("connection error:")
                print(e)
                # connected.pop(self.idc)
                print(connected)
                raise Exception("Player disconnected while in game")

        # self.connexion.close()


# ==================================================

# --- creation du serveur
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((host, port))
except socket.error:
    print("wrong addr")
    sys.exit()
print("")
print("==== Server on, awaiting messages ====")


# --- acceptation des connexions
connected = {}

ide = 0
width = 7
nbBarrier = 4
nbPlayer = 2
nbBots = 2
mySocket.listen(nbPlayer)

init = [0, width, nbBarrier, nbPlayer, nbBots]

while 1:
    connexion, adresse = mySocket.accept()
    print("ide:", ide)

    client_list.append(i)

    connected[ide] = connexion
    ThreadClient(connexion, ide)
    print(i)
    print(init)
    init[0] = i

    init_msg = pickle.dumps(init)
    connexion.send(init_msg)
    i += 1

    ide += 1
