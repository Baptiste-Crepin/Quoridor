import socket
import threading
import time

import pygame

from gameLogic.bot import Bot
from graphical.menus.board import Board
from graphical.menus.endGameMulti import EndGameMulti
from gameLogic.localGame import LocalGame
from multi.threadClient import StoppableThreadClient
from gameLogic.player import Player
from graphical.widgets.menu import Menu


class MultiplayerGame(LocalGame):
    """LocalGame child class  for multiplayer"""

    def __init__(self, connection: socket.socket, fullScreen, width: int, nbBarrier: int, nbPlayer: int, host: bool,
                 startingPlayerIndex: int, nbBots: int = 0, num: int = -1) -> None:
        print(fullScreen)
        super().__init__(width, nbPlayer, nbBarrier, nbBots,[0, 0, 0, 0],fullScreen)
        self.board = Board(self.game.getSquareWidth(),[0, 0, 0, 0],fullScreen)
        self.fullScreen = fullScreen
        self.num = num
        self.response_event = threading.Event()
        self.host = host
        self.startingPlayer = startingPlayerIndex
        self.thread = StoppableThreadClient(
            connection, self, self.response_event, host)

        self.game.setCurrentPlayerIndex(self.startingPlayer)
        self.game.setCurrentPlayer(
            self.game.getPlayerList()[self.startingPlayer])

    def displayPossibleMoves(self, player: Player):
        """highlights the possible moves but only for the client's player"""
        self.board.clearAllHighlight()
        if ((not isinstance(player, Bot) or player.getNumber() == self.num + 1) and
                (self.game.getCurrentPlayer().getNumber() == self.num + 1)):
            self.highlightPlayer(player)
            self.highlightBarrier()

    def placement(self, currentPlayer: Player) -> None:
        """ logic for the player's actions, sends the state of the game when a player finishes he's turn """
        if isinstance(currentPlayer, Bot) and self.num == 0:
            randomAction = currentPlayer.randomAction(
                self.game.possibleBarrierPlacement(currentPlayer))
            if randomAction == 0:
                coord = currentPlayer.randomMove(
                    self.game.possibleMoves(currentPlayer.getCoordinates()))
                self.game.movePlayer(currentPlayer, coord)
            elif randomAction == 1:
                coord, direction = currentPlayer.randomBarrier(
                    self.game.possibleBarrierPlacement(currentPlayer))
                self.game.placeWall(coord, direction, currentPlayer)
            self.thread.emit()  # sends the state of the game to the server when bot plays
            print("Bot played")
            return

        event = self.board.handleEvents()
        if not event:
            return

        (action, x, y) = event
        clickCoord = (x, y)
        if ((not isinstance(self.game.getCurrentPlayer(), Bot) or self.game.getCurrentPlayer().getNumber()
             == self.num + 1) and (self.game.getCurrentPlayer().getNumber() == self.num + 1)):

            if action == 'TablePlayer':
                if clickCoord not in self.game.possibleMoves(currentPlayer.getCoordinates()):
                    return
                self.board.clearHover(self.board.rect)
                self.game.movePlayer(currentPlayer, clickCoord)

            if action == 'VerticalBarrier':
                if (clickCoord, 'Right') not in self.game.possibleBarrierPlacement(currentPlayer):
                    return
                self.game.placeWall(clickCoord, 'Right',
                                    currentPlayer, place=True)

            if action == 'HorizontalBarrier':
                if (clickCoord, 'Down') not in self.game.possibleBarrierPlacement(currentPlayer):
                    return
                self.game.placeWall(clickCoord, 'Down', currentPlayer)

            self.board.clearAllHighlight()
            self.highlightPlayer(currentPlayer)
            self.highlightBarrier()
            print(f"end of turn for player n° {str(self.num)}")
            self.thread.emit()  # sends the state of the game to the server when user plays
            print("waiting for server response ")
            self.response_event.wait()  # waits for the server response
            print("server responded")

            self.response_event.clear()

    def resetGameState(self):
        print("resetting the game")

    def mainLoop(self) -> None:
        """main loop of the class to play until victory is detected by End function"""
        self.highlightPlayer(self.game.getCurrentPlayer())
        self.highlightBarrier()
        while True:
            while not self.game.checkGameOver():
                time.sleep(0.03)
                self.placement(self.game.getCurrentPlayer())
                self.displayPossibleMoves(self.game.getCurrentPlayer())
                self.actualizeGame()
                self.board.newFrame(
                    self.game.getCurrentPlayer(), self.game.getPlayerList())
            # Game has ended. displays the end screen
            self.thread.ender()  # send  the current player and the end game message
            time.sleep(0.4)  # wait for the server to actualize every client
            end = EndGameMulti(self.game.getPreviousPlayer(), self.fullScreen, self.game.getSquareWidth(
            ), self.game.getNumberOfPlayers(), self.game.getNumberOfBarriers(), self.game.getNumberOfBots(), self.score, self.host)
            Menu.newMenu(self, end)
