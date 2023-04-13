# serveur avec Thread pour plusieurs clients



import socket, sys, threading, pickle

hostname = socket.gethostname()

host = socket.gethostbyname(hostname)
# host = 'LocalHost'
port = 45678
client_list = []
i = 0

# ---------------------------------------------
class ThreadClient(threading.Thread,):

    def __init__(self, c,idd):
        threading.Thread.__init__(self)
        self.connexion = c
        self.start()
        self.idc = idd
        self.current_client = 0


    def nextClient(self) -> None:
        print(self.current_client < (len(connected) - 1), self.current_client, (len(connected) - 1))
        if self.current_client < (len(connected) - 1):
            self.current_client += 1
        else:
            self.current_client = 0


    def run(self):
        # recuperation du message d'un client
        while 1:

                try:

                    msg1 = self.connexion.recv(4096)
                    msg = pickle.loads(msg1)
                    print ("reccu:",msg)
                    print(connected[self.idc])
                    # envoi du message à tous les clients
                    connected[0].send(msg1)
                    connected[1].send(msg1)
                    self.nextClient()
                    msg2 = self.current_client
                    print(msg2)


                    connected[0].send(pickle.dumps(msg2))
                    connected[1].send(pickle.dumps(msg2))



                except Exception as e:
                    print("connection error:")
                    print(e)
                    connected.pop(self.idc)
                    global ide
                    ide -= 1
                    print(connected)


            #self.connexion.close()


                #self.connexion.close()


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
mySocket.listen(4)

# --- acceptation des connexions
connected = {}


ide = 0


while 1:
    connexion, adresse = mySocket.accept()
    print("ide:",ide)

    client_list.append(i)
    print(i)
    i += 1

    connected[ide] = connexion
    ThreadClient(connexion, ide)



    msg = str(ide)
    print(msg)
    connexion.send(msg.encode("Utf8"))
    ide += 1

