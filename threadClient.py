import threading
import pickle
import time


class StoppableThreadClient(threading.Thread):
    def __init__(self, c, multiplayerClient):
        super(StoppableThreadClient, self).__init__()
        self.connexion = c
        self.multiplayerClient = multiplayerClient
        self.stopEvent = threading.Event()
        self.start()

    def handleGameState(self, message: list) -> None:
        self.multiplayerClient.game.setGrid(message[1])
        self.multiplayerClient.game.getCurrentPlayer().setBarrier(message[3])
        self.multiplayerClient.game.setCurrentPlayerN(message[2])
        self.multiplayerClient.game.setCurrentPlayer(self.multiplayerClient.game.getPlayerList()[message[2]])

    def stop(self):
        self.stopEvent.set()

    def stopped(self):
        return self.stopEvent.is_set()

    def handleChatMessage(self, message: list) -> None:
        print("chat not implemented yet")

    def handleQuestion(self, message: list) -> None:
        print("? not implemented yet")

    def handleEmpty(self, message: list) -> None:
        print("\"\" not implemented yet")

    def handleEnd(self, message: list):
        self.multiplayerClient.game.setCurrentPlayer(message[1])
        if self.is_alive():
            print("Thread is still alive; stoping it now.")
            self.stop()
        while self.is_alive():
            time.sleep(1)

    def run(self):
        while not self.stopped():
            message_handlers = {
                'game_state': self.handleGameState,
                'chat': self.handleChatMessage,
                '?': self.handleQuestion,
                'game_end': self.handleEnd,
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
        self.connexion.close()

    def emet(self):
        grid = self.multiplayerClient.game.getGrid()
        barriersLeft = self.multiplayerClient.game.getCurrentPlayer().getBarrier()
        msg = ['game_state']
        msg.append(grid)
        msg.append(self.multiplayerClient.num)
        msg.append(barriersLeft)
        print('sending:', msg)
        data = pickle.dumps(msg)
        self.connexion.send(data)

    def ender(self) -> None:
        msg = []
        currentplayer = self.multiplayerClient.game.getCurrentPlayer()
        msg.append('game_end')
        print("ending the game")
        msg.append(currentplayer)
        data = pickle.dumps(msg)
        self.connexion.send(data)

    def reco(self):
        dump = self.connexion.recv(4096)
        message = pickle.loads(dump)
        return message
