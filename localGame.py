import pygame
from game import Game
from graphical.menus.board import Board
from Bot import Bot
from player import Player
from graphical.menus.endGame import End


class LocalGame():
    def __init__(self, width, nbPlayer, nbBarrier, nbBots) -> None:
        self.game = Game(width, nbPlayer, nbBarrier, nbBots)
        self.board = Board(self.game.getSquareWidth())
        self.newTurn = True

    def highlightPlayer(self, player):
        for PossibleMoveCoordo in self.game.possibleMoves(player.getCoordinates()):
            self.board.rect[PossibleMoveCoordo[1]
                            ][PossibleMoveCoordo[0]].highlighted = True

    def highlightBarrier(self):
        for (possibleBarrierCoordo, direction) in self.game.possibleBarrierPlacement(self.game.getCurrentPlayer()):
            if direction == 'Right':
                self.board.Vbarriers[possibleBarrierCoordo[1]
                                     ][possibleBarrierCoordo[0]].possiblePlacement = True

            if direction == 'Down':
                self.board.Hbarriers[possibleBarrierCoordo[1]
                                     ][possibleBarrierCoordo[0]].possiblePlacement = True

    def displayPossibleMoves(self, player: Player):
        if not self.newTurn:
            return
        self.newTurn = False
        if not isinstance(player, Bot):
            self.highlightPlayer(player)
            self.highlightBarrier()

    def actualizeGame(self):
        for i, row in enumerate(self.game.getGrid()):
            for j, cell in enumerate(row):

                self.board.rect[j][i].player = cell.getPlayer()

                if i < len(self.game.getGrid())-1:
                    self.board.Hbarriers[j][i].placed = cell.getWalls()['Down']

                if j < len(row)-1:
                    self.board.Vbarriers[j][i].placed = cell.getWalls()[
                        'Right']

    def placement(self, currentPlayer: Player):
        if isinstance(currentPlayer, Bot):
            self.board.newFrame(currentPlayer, self.game.getPlayerList())
            currentPlayer.randomMoves(self.game.possibleBarrierPlacement(
                currentPlayer), self.game.possibleMoves(currentPlayer.getCoordinates()))

        player = self.game.getCurrentPlayer()
        if isinstance(player, Bot):
            self.board.newFrame(self.game.getCurrentPlayer(),
                                self.game.getPlayerList())
            randomMove = player.randomMoves(self.game.possibleBarrierPlacement(
                player), self.game.possibleMoves(player.getCoordinates()))
            if isinstance(randomMove[1], int):
                self.game.movePlayer(player, randomMove)
            elif isinstance(randomMove[0], tuple) and isinstance(randomMove[1], str):
                coordo = randomMove[0]
                direction = randomMove[1]
                self.game.placeWall(coordo, direction, player)

            self.game.nextPlayer()
            self.newTurn = True
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
        self.game.nextPlayer()
        self.newTurn = True

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
            end = End(self.game.getPreviousPlayer(), self.game.getSquareWidth(
            ), self.game.getNumberOfPlayers(), self.game.getNumberOfBarriers(), self.game.getNumberOfBots())
            while self.game.checkGameOver():
                end.setWindow()
                pygame.display.update()
            raise SystemExit


if __name__ == "__main__":

    width = 11
    nbBarrier = 4
    nbPlayer = 2
    nbBot = 2
    G = LocalGame(width, nbPlayer, nbBarrier, nbBot)
    G.mainLoop()
