import threading
import pickle



class Thread_client(threading.Thread):
    def __init__(self, c, multiplayerClient):
        threading.Thread.__init__(self)
        self.connexion = c
        self.multiplayerClient = multiplayerClient
        self.start()

    def handleGameState(self, message: list) -> None:
        self.multiplayerClient.game.setGrid(message[1])
        self.multiplayerClient.game.setCurrentPlayerN(message[2])
        self.multiplayerClient.game.setCurrentPlayer(
            self.multiplayerClient.game.getPlayerList()[message[2]])

    def handleChatMessage(self, message: list) -> None:
        print("chat not implemented yet")

    def handleQuestion(self, message: list) -> None:
        print("? not implemented yet")

    def handleEmpty(self, message: list) -> None:
        print("\"\" not implemented yet")

    def run(self):
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
                raise Exception("Player disconnected while in game")

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
