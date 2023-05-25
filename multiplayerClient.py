import pickle
import socket
import sys

from Bot import Bot
from Player import Player
from Table import Board
from localGame import LocalGame
from threadClient import Thread_client



class MultiplayerGame(LocalGame):
    def __init__(self, width, nbPlayer, nbBarrier, nbBots=0, num=-1) -> None:
        super().__init__(width, nbPlayer, nbBarrier, nbBots)
        self.board = Board(self.game.getSquareWidth(), num)
        self.num = num
        print("NUM", num)

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
            th.emet()
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

        print("tour fini pour " + str(num))
        th.emet()


if __name__ == "__main__":
    # width = int(input('Width'))
    # nbPlayer = int(input('Nb Player'))
    # nbBarrier = int(input('Nb barrier'))
    # width = 5
    # nbBarrier = 4
    # nbPlayer = 2
    # client avec Thread

    # ============================================================
    hostname = socket.gethostname()

    host = socket.gethostbyname(hostname)
    # host = '192.168.1.10'
    port = 45678

    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((host, port))
        print("Connexion active")
    except socket.error:
        print("Erreur sur la connection")
        sys.exit()

    msg = connexion.recv(4096)
    msg = pickle.loads(msg)
    print("reccu:", msg)
    width = msg[1]
    nbBarrier = msg[2]
    nbPlayer = msg[3]
    nbBots = msg[4]

    num = int(msg[0])

    # =========================================================

    G = MultiplayerGame(width, nbPlayer, nbBarrier, nbBots, num)
    th = Thread_client(connexion, G)
    G.mainLoop()
