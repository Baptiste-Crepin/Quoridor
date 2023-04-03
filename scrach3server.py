# serveur avec Thread pour plusieurs clients



import socket, sys, threading, pickle

hostname = socket.gethostname()

host = socket.gethostbyname(hostname)
# host = 'LocalHost'
port = 45678


# ---------------------------------------------
class ThreadClient(threading.Thread,):

    def __init__(self, c,idd):
        threading.Thread.__init__(self)
        self.connexion = c
        self.start()
        self.idc = idd

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
                except:
                    print("connection error")
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
    connected[ide] = connexion
    ThreadClient(connexion, ide)



    msg = str(ide)
    print(msg)
    connexion.send(msg.encode("Utf8"))
    ide += 1
