import threading
import pickle


class Thread_client(threading.Thread):
    def __init__(self, c, multiplayerClient):
        threading.Thread.__init__(self)
        self.connexion = c
        self.multiplayerClient = multiplayerClient
        self.start()

    def run(self):
        while 1:
            data = self.reco()
            print("R")
            # print( type(data))
            if type(data) is list:
                print("reciev:", data)
                self.multiplayerClient.game.setGrid(data)
                # G.actualizeGame()
                # G.board.newFrame()
                # G.nextPlayer
            else:

                self.multiplayerClient.game.setCurrentPlayerN(data)
                self.multiplayerClient.game.setCurrentPlayer(self.multiplayerClient.game.getPlayerList()[data])
                print("reciev:", data)

        # self.connexion.close()

    def emet(self):
        gr = self.multiplayerClient.game.getGrid()
        data = pickle.dumps(gr)
        self.connexion.send(data)
        # self.connexion.send(msg.encode("Utf8"))
        # self.connexion.close()

    def reco(self):
        dump = self.connexion.recv(4096)
        message = pickle.loads(dump)
        return message
