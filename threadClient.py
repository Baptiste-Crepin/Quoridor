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
            if data[0] == 'board':
                print("reciev:", data)
                self.multiplayerClient.game.setGrid(data[1])
                # G.actualizeGame()
                # G.board.newFrame()
                # G.nextPlayer
            elif data[0] == 'turn':
                self.multiplayerClient.game.setCurrentPlayerN(data[1])
                self.multiplayerClient.game.setCurrentPlayer(self.multiplayerClient.game.getPlayerList()[data[1]])
                print("reciev:", data)

            elif data[0] == 'chat':
                return
            elif data[0] == '?':
                return
            elif data[0] == '':
                return


        # self.connexion.close()

    def emet(self):
        gr = self.multiplayerClient.game.getGrid()
        msg = ["board"]
        msg.append(gr)
        data = pickle.dumps(msg)
        self.connexion.send(data)
        # self.connexion.send(msg.encode("Utf8"))
        # self.connexion.close()

    def reco(self):
        dump = self.connexion.recv(4096)
        message = pickle.loads(dump)
        print(message)
        return message
