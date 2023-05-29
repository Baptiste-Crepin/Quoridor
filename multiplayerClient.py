import pickle
import socket
import sys

from Bot import Bot
from Player import Player
from Table import Board
from localGame import LocalGame
from threadClient import Thread_client



class MultiplayerGame(LocalGame):
    def __init__(self, connexion, width, nbBarrier, nbPlayer, nbBots=0, num=-1) -> None:
        super().__init__(width, nbPlayer, nbBarrier, nbBots)
        self.board = Board(self.game.getSquareWidth(), num)
        self.num = num
        self.thread = Thread_client(connexion, self)

    def displayPossibleMoves(self, player: Player):
        self.board.clearAllHighlight()
        if ((not isinstance(player, Bot) or player.getNumber() == self.num + 1) and
                (self.game.getCurrentPlayer().getNumber() == self.num + 1)):
            self.highlightPlayer(player)
            self.highlightBarrier()

    def placement(self, currentPlayer: Player):
        if isinstance(currentPlayer, Bot) and self.num == 0:
            self.board.newFrame(currentPlayer)
            currentPlayer.randomMoves(self.game)
            print("Bot played")
            self.thread.emet()
            return
        event = self.board.handleEvents(currentPlayer)
        if not event:
            return

        (action, x, y) = event
        clickCoordo = (x, y)

        if action == 'TablePlayer':
            if clickCoordo not in self.game.possibleMoves(currentPlayer.getCoordinates()):
                return
            self.board.clearHover(self.board.rect)
            self.game.movePlayer(currentPlayer, clickCoordo)

        if action == 'VerticalBarrier':
            if (clickCoordo, 'Right') not in self.game.possibleBarrierPlacement(currentPlayer):
                return
            self.game.placeWall(clickCoordo, 'Right', currentPlayer, place=True)

        if action == 'HorrizontalBarrier':
            if (clickCoordo, 'Down') not in self.game.possibleBarrierPlacement(currentPlayer):
                return
            self.game.placeWall(clickCoordo, 'Down', currentPlayer)

        self.board.clearAllHighlight()
        self.highlightPlayer(currentPlayer)
        self.highlightBarrier()
        ("tour fini pour " + str(self.num))
        self.thread.emet()

def createGame(host, port):
    # client with thread
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((host, port))
        print("Connexion active")
    except socket.error:
        print("Erreur sur la connection")
        sys.exit()

    serverMessage = connexion.recv(4096)
    startVars = pickle.loads(serverMessage)
    
    print("Game infos:", startVars)
    num = int(startVars[0])
    width = startVars[1]
    nbBarrier = startVars[2]
    nbPlayer = startVars[3]
    nbBots = startVars[4]

    Game = MultiplayerGame(connexion, width, nbBarrier, nbPlayer, nbBots, num)
    Game.mainLoop()

if __name__ == "__main__":
    # TODO: remove this when cleaning up for final version
    # temporary localhost for testing purposes
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    # host = '192.168.1.10'
    port = 45678
    createGame(host, port)