import pickle
import socket
import sys
import time
import pygame

from Bot import Bot
from player import Player
from graphical.menus.board import Board
from localGame import LocalGame
from threadClient import StoppableThreadClient
from graphical.menus.endGame import End

DISCOVERY_MSG = b"SERVER_DISCOVERY_REQUEST"


class SearchServer():
    def __init__(self) -> None:
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.discoSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discoSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def discover(self):
        self.discoSock.sendto(DISCOVERY_MSG, ('<broadcast>', 5555))
        # Set a timeout of 5 seconds for waiting for responses
        self.discoSock.settimeout(1.0)
        result = list()
        serverList = list()

        try:
            start_time = time.time()
            while time.time() - start_time < 3:

                data, _ = self.discoSock.recvfrom(1024)
                try:
                    server_info = pickle.loads(data)
                    serverList.append(server_info)
                    print("Server info:", server_info)
                except pickle.UnpicklingError:
                    print("Received a non-Python object.")

        except socket.timeout:
            print('request timed out / no server found')
        for server in serverList:
            result.append(server)
        return result

    def connect(self, ip, port):
        try:
            self.connexion.connect((ip, port))
            print("Connexion active")
            serverMessage = self.connexion.recv(4096)
            startVars = pickle.loads(serverMessage)
            print("startvars : ", startVars)
            return startVars
        except socket.error:
            print("Erreur sur la connection")
            sys.exit()

    def multiLaunch(self, startVars):
        try:
            serverMessage = self.connexion.recv(4096)
            unpickeled_message = pickle.loads(serverMessage)

            print(unpickeled_message)
            if unpickeled_message == True:
                print("starting game", startVars)
                self.connexion.setblocking(True)
                createGame(self.connexion, startVars)
                return True
        except:
            return False


class MultiplayerGame(LocalGame):
    def __init__(self, connexion, width, nbBarrier, nbPlayer, nbBots=0, num=-1) -> None:
        super().__init__(width, nbPlayer, nbBarrier, nbBots)
        self.board = Board(self.game.getSquareWidth())
        self.num = num
        self.thread = StoppableThreadClient(connexion, self)

    def displayPossibleMoves(self, player: Player):
        self.board.clearAllHighlight()
        if ((not isinstance(player, Bot) or player.getNumber() == self.num + 1) and
                (self.game.getCurrentPlayer().getNumber() == self.num + 1)):
            self.highlightPlayer(player)
            self.highlightBarrier()

    def placement(self, currentPlayer: Player):
        if isinstance(currentPlayer, Bot) and self.num == 0:
            self.board.newFrame(currentPlayer, self.game.getPlayerList())
            currentPlayer.randomMoves(self.game.possibleBarrierPlacement(
                currentPlayer), self.game.possibleMoves(currentPlayer.getCoordinates()))
            print("Bot played")
            self.thread.emet()
            return
        event = self.board.handleEvents()
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
            self.game.placeWall(clickCoordo, 'Right',
                                currentPlayer, place=True)

        if action == 'HorrizontalBarrier':
            if (clickCoordo, 'Down') not in self.game.possibleBarrierPlacement(currentPlayer):
                return
            self.game.placeWall(clickCoordo, 'Down', currentPlayer)

        self.board.clearAllHighlight()
        self.highlightPlayer(currentPlayer)
        self.highlightBarrier()
        print("tour fini pour " + str(self.num))
        self.thread.emet()

    def mainLoop(self) -> None:
        self.highlightPlayer(self.game.getCurrentPlayer())
        self.highlightBarrier()
        while True:
            while not self.game.checkGameOver():

                self.displayPossibleMoves(self.game.getCurrentPlayer())

                self.placement(self.game.getCurrentPlayer())
                self.actualizeGame()

                self.board.newFrame(
                    self.game.getCurrentPlayer(), self.game.getPlayerList())
            # TODO: Game has ended. display the end screen
            self.thread.ender()
            time.sleep(0.4)
            end = End(self.game.getPreviousPlayer(), self.game.getSquareWidth(
            ), self.game.getNumberOfPlayers(), self.game.getNumberOfBarriers(), self.game.getNumberOfBots())


            while self.game.checkGameOver():
                end.mainLoop()
                pygame.display.update()
            raise SystemExit


def createGame(connexion, startVars):

    print("Game infos:", startVars)
    num = int(startVars[0])
    width = startVars[1]
    nbBarrier = startVars[2]
    nbPlayer = startVars[3]
    nbBots = startVars[4]

    Game = MultiplayerGame(connexion, width, nbBarrier, nbPlayer, nbBots, num)
    Game.mainLoop()
