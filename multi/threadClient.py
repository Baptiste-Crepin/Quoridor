import pickle
import socket
import threading
import time
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    # avoid circular import when type checking
    from multiplayerClient import MultiplayerGame


class StoppableThreadClient(threading.Thread):
    """this class runs itself in a thread and is meand to handle client action for each client at any time"""

    def __init__(self, connection: socket.socket, multiplayerClient: 'MultiplayerGame', response_event, host: bool):
        # super(StoppableThreadClient, self).__init__()
        super().__init__()
        self.connection = connection
        self.multiplayerClient = multiplayerClient
        self.response_event = response_event
        self.stopEvent = threading.Event()
        self.start()

    def handleGameState(self, message: list[Any]) -> None:
        """upon reception of a 'game_state' messages update the state of the game accordingly"""
        self.multiplayerClient.game.setGrid(message[1])
        self.multiplayerClient.game.setCurrentPlayerIndex(message[2])
        self.multiplayerClient.game.setCurrentPlayer(
            self.multiplayerClient.game.getPlayerList()[message[2]])
        self.multiplayerClient.game.getCurrentPlayer().setBarrier(message[3])

    def stop(self):
        self.stopEvent.set()

    def stopped(self):
        return self.stopEvent.is_set()

    def handleChatMessage(self, message: list[Any]) -> None:
        print("chat not implemented yet")

    def handleAbort(self, message: list[Any]):
        """ the server has aborted the game due to some network issue aborting the game for the client"""
        print(message)

    def handleEnd(self, message: list[Any]):
        """ upon reception of a 'game_end' messages update the state of the game accordingly then stop the thread if
        possible """
        self.multiplayerClient.game.setCurrentPlayer(message[1])
        if self.is_alive():
            print("Thread is still alive; stopping it now.")
            self.stop()
        while self.is_alive():
            time.sleep(1)

    def handleReset(self, message: list[Any]):
        """Call resetGameState method of 'MultiplayerGame' instance"""
        self.multiplayerClient.resetGameState()

    def run(self):
        """ this function is executed at the start of the thread try to receive message then calls the appropriate
        method depending on the message type /'header'"""
        while not self.stopped():
            time.sleep(0.03)
            message_handlers = {
                'game_state': self.handleGameState,
                'chat': self.handleChatMessage,
                'mpAbort': self.handleAbort,
                'game_end': self.handleEnd,
                'resetGame': self.handleReset
            }
            while True:
                try:

                    message = self.reco()
                    message_type = message[0]
                    self.response_event.set()
                    if message_type in message_handlers:
                        message_handlers[message_type](message)
                    else:
                        print("unexpected data in header can't interpret packet")
                except Exception as e:
                    print("connection error:")
                    print(e)
                    raise Exception("Player disconnected while in game") from e
                time.sleep(0.03)
        # self.connection.close()

    def emet(self):
        """sends the state of the game as well as the amount of remaining barriers for the current player"""
        grid = self.multiplayerClient.game.getGrid()
        barriersLeft = self.multiplayerClient.game.getCurrentPlayer().getBarrier()
        msg = ['game_state', grid, self.multiplayerClient.num, barriersLeft]
        data = pickle.dumps(msg)
        self.connection.sendall(data)

    def ender(self) -> None:
        """ sends the 'game_end' with the current player in it """
        currentplayer = self.multiplayerClient.game.getCurrentPlayer()
        msg = ['game_end', currentplayer]
        data = pickle.dumps(msg)
        self.connection.sendall(data)

    def restart(self) -> None:
        print("sending restart message ")
        msg = ['resetGame', True]
        data = pickle.dumps(msg)
        self.connection.sendall(data)

    def reco(self):
        """receives message from server then return the unpicked version of it """
        dump = self.connection.recv(4096)
        return pickle.loads(dump)
