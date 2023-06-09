import socket
import time

import pygame

from Bot import Bot
from graphical.menus.board import Board
from graphical.menus.endGame import End
from localGame import LocalGame
from multi.threadClient import StoppableThreadClient
from player import Player


class MultiplayerGame(LocalGame):
    """LocalGame child class  for multiplayer"""

    def __init__(self, connection: socket.socket, width: int, nbBarrier: int, nbPlayer: int, nbBots: int = 0,
                 num: int = -1) -> None:
        super().__init__(width, nbPlayer, nbBarrier, nbBots)
        self.board = Board(self.game.getSquareWidth())
        self.num = num
        self.thread = StoppableThreadClient(connection, self)

    def displayPossibleMoves(self, player: Player):
        """highlights the possible moves but only for the client's player"""
        self.board.clearAllHighlight()
        if ((not isinstance(player, Bot) or player.getNumber() == self.num + 1) and
                (self.game.getCurrentPlayer().getNumber() == self.num + 1)):
            self.highlightPlayer(player)
            self.highlightBarrier()

    def placement(self, currentPlayer: Player):
        """ logic for the player's actions, sends the state of the game when a player finishes he's turn """
        if isinstance(currentPlayer, Bot) and self.num == 0:
            self.board.newFrame(currentPlayer, self.game.getPlayerList())
            currentPlayer.randomMoves(self.game.possibleBarrierPlacement(
                currentPlayer), self.game.possibleMoves(currentPlayer.getCoordinates()))
            print("Bot played")

            self.thread.emet()  # sends the state of the game to the server when bot plays
            self.game.nextPlayer()
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
        print(f"tour fini pour {str(self.num)}")
        self.thread.emet()  # sends the state of the game to the server when user plays

        self.game.nextPlayer()

    def mainLoop(self) -> None:
        """main loop of the class to play until victory is detected by End function"""
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
            self.thread.ender()  # send  the current player and the end game message
            time.sleep(0.4)  # wait for the server to actualise every client
            end = End(self.game.getPreviousPlayer(), self.game.getSquareWidth(
            ), self.game.getNumberOfPlayers(), self.game.getNumberOfBarriers(), self.game.getNumberOfBots())
            while self.game.checkGameOver():
                end.mainLoop()
                pygame.display.update()
            raise SystemExit


