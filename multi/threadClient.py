import threading
import pickle
import time
from typing import Any, TYPE_CHECKING
import socket

if TYPE_CHECKING:
    # avoid circular import when type checking
    from multiplayerClient import MultiplayerGame


class StoppableThreadClient(threading.Thread):
    def __init__(self, connection: socket.socket, multiplayerClient: 'MultiplayerGame'):
        # super(StoppableThreadClient, self).__init__()
        super().__init__()
        self.connection = connection
        self.multiplayerClient = multiplayerClient
        self.stopEvent = threading.Event()
        self.start()

    def handleGameState(self, message: list[Any]) -> None:
        self.multiplayerClient.game.setGrid(message[1])
        self.multiplayerClient.game.getCurrentPlayer().setBarrier(message[3])
        self.multiplayerClient.game.setCurrentPlayerN(message[2])
        self.multiplayerClient.game.setCurrentPlayer(
            self.multiplayerClient.game.getPlayerList()[message[2]])

    def stop(self):
        self.stopEvent.set()

    def stopped(self):
        return self.stopEvent.is_set()

    def handleChatMessage(self, message: list[Any]) -> None:
        print("chat not implemented yet")

    def handleEnd(self, message: list[Any]):
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
                    raise Exception("Player disconnected while in game") from e
        self.connection.close()

    def emet(self):
        grid = self.multiplayerClient.game.getGrid()
        barriersLeft = self.multiplayerClient.game.getCurrentPlayer().getBarrier()
        msg = ['game_state', grid, self.multiplayerClient.num, barriersLeft]
        data = pickle.dumps(msg)
        self.connection.send(data)

    def ender(self) -> None:
        currentplayer = self.multiplayerClient.game.getCurrentPlayer()
        msg = ['game_end', currentplayer]
        data = pickle.dumps(msg)
        self.connection.send(data)

    def reco(self):
        dump = self.connection.recv(4096)
        return pickle.loads(dump)
