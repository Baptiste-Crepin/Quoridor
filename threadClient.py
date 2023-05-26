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
            if data[0] == 'game_state':
                print("reciev:", data)
                self.multiplayerClient.game.setGrid(data[1])
                # G.actualizeGame()
                # G.board.newFrame()
                # G.nextPlayer
                self.multiplayerClient.game.setCurrentPlayerN(data[2])
                self.multiplayerClient.game.setCurrentPlayer(self.multiplayerClient.game.getPlayerList()[data[2]])

            elif data[0] == '?':
                return
            elif data[0] == 'chat':
                return
            elif data[0] == '?':
                return
            elif data[0] == '':
                return


        # self.connexion.close()

    def emet(self):
        grid = self.multiplayerClient.game.getGrid()
        msg = ['game_state']
        msg.append(grid)
        msg.append(self.multiplayerClient.num)
        print('sending:', msg)
        data = pickle.dumps(msg)

        self.connexion.send(data)
        # self.connexion.send(msg.encode("Utf8"))
        # self.connexion.close()

    def reco(self):
        dump = self.connexion.recv(4096)
        message = pickle.loads(dump)
        return message
