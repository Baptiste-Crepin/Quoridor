import pickle
import socket
import threading
import time
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    # avoid circular import when type checking
    from multiplayerClient import MultiplayerGame


class StoppableThreadClient(threading.Thread):
    """this class runs itself in a thread and is meant to handle client action for each client at any time"""

    def __init__(self, connection: socket.socket, multiplayerClient: 'MultiplayerGame', responseEvent: threading.Event, host: bool):
        # super(StoppableThreadClient, self).__init__()
        super().__init__()
        self.connection = connection
        self.multiplayerClient = multiplayerClient
        self.responseEvent = responseEvent
        self.stopEvent = threading.Event()
        self.start()

    def handleGameState(self, message: list[Any]) -> None:
        """upon reception of a 'gameState' messages update the state of the game accordingly"""
        self.multiplayerClient.game.setGrid(message[1])
        if isinstance(message[2], int):
            self.multiplayerClient.game.setCurrentPlayerIndex(message[2])
            self.multiplayerClient.game.setCurrentPlayer(
                self.multiplayerClient.game.getPlayerList()[message[2]])
        self.multiplayerClient.game.getCurrentPlayer().setBarrier(message[3])




    def handleChatMessage(self, message: list[Any]) -> None:
        print("chat not implemented yet")

    def handleAbort(self, message: list[Any]):
        """ the server has aborted the game due to some network issue aborting the game for the client"""
        print(message)

    def handleEnd(self, message: list[Any]):
        """ upon reception of a 'gameEnd' messages update the state of the game accordingly then stop the thread if
        possible """
        self.multiplayerClient.game.setCurrentPlayer(message[1])
        while not self.stopEvent.is_set():
                print("Thread is still alive; stopping it now.")
                try:
                    self.connection.shutdown(socket.SHUT_RDWR)
                    self.connection.close()
                    self.stopEvent.set()
                except OSError:
                    print(f"Error closing socket: socket already closed")

                time.sleep(0.2)

    def handleReset(self, message: list[Any]):
        """Call resetGameState method of 'MultiplayerGame' instance"""
        self.multiplayerClient.resetGameState()

    def run(self):
        """ this function is executed at the start of the thread try to receive message then calls the appropriate
        method depending on the message type /'header'"""
        time.sleep(0.03)
        message_handlers = {
            'gameState': self.handleGameState,
            'chat': self.handleChatMessage,
            'mpAbort': self.handleAbort,
            'gameEnd': self.handleEnd,
            'resetGame': self.handleReset
        }
        while not self.stopEvent.is_set():
            try:
                message = self.reco()
                self.responseEvent.set()
                message_type = message[0]
                if message[0] == 'gameEnd':
                    self.connection.setblocking(False)

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

    def emit(self):
        """sends the state of the game as well as the amount of remaining barriers for the current player"""
        grid = self.multiplayerClient.game.getGrid()
        barriersLeft = self.multiplayerClient.game.getCurrentPlayer().getBarrier()
        msg = ['gameState', grid, self.multiplayerClient.num, barriersLeft]
        data = pickle.dumps(msg)
        self.connection.sendall(data)

    def ender(self) -> None:
        """ sends the 'gameEnd' with the current player in it """
        currentPlayer = self.multiplayerClient.game.getCurrentPlayer()
        msg = ['gameEnd', currentPlayer]
        data = pickle.dumps(msg)
        self.connection.sendall(data)

    def restart(self) -> None:
        print("sending restart message ")
        msg = ['resetGame', True]
        data = pickle.dumps(msg)
        self.connection.sendall(data)

    def reco(self):
        """receives message from server then return the unpicked version of it """
        dump = self.connection.recv(8192)
        return pickle.loads(dump)
