import pygame
from game import Game
from graphical.menus.board import Board
from Bot import Bot
from endGame import End


class GraphicalGame():
    def __init__(self, width, nbPlayer, nbBarrier, nbBots) -> None:
        self.game = Game(width, nbPlayer, nbBarrier, nbBots)
        self.board = Board(self.game.getSquareWidth())

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

    def displayPossibleMoves(self):
        if not isinstance(self.game.getCurrentPlayer(), Bot):
            self.highlightPlayer(self.game.getCurrentPlayer())
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

    def placement(self):
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
            return

        event = self.board.handleEvents()
        if not event:
            return

        (action, x, y) = event
        clickCoordo = (x, y)

        if action == 'TablePlayer':
            if clickCoordo not in self.game.possibleMoves(self.game.getCurrentPlayer().getCoordinates()):
                return
            self.board.clearHover(self.board.rect)
            self.game.movePlayer(self.game.getCurrentPlayer(), clickCoordo)

        if action == 'VerticalBarrier':
            if (clickCoordo, 'Right') not in self.game.possibleBarrierPlacement(self.game.getCurrentPlayer()):
                return
            self.game.placeWall(clickCoordo, 'Right',
                                self.game.getCurrentPlayer(), place=True)

        if action == 'HorrizontalBarrier':
            if (clickCoordo, 'Down') not in self.game.possibleBarrierPlacement(self.game.getCurrentPlayer()):
                return
            self.game.placeWall(clickCoordo, 'Down',
                                self.game.getCurrentPlayer())

        self.board.clearAllHighlight()
        self.game.nextPlayer()

    def mainLoop(self) -> None:
        self.highlightPlayer(self.game.getCurrentPlayer())
        self.highlightBarrier()
        while True:
            while not self.game.checkGameOver():
                self.displayPossibleMoves()

                self.placement()
                self.actualizeGame()

                self.board.newFrame(
                    self.game.getCurrentPlayer(), self.game.getPlayerList())
            # TODO: Game has ended. display the end screen
            end = End(self.game.getPreviousPlayer(), self.game.getSquareWidth(
            ), self.game.getNumberOfPlayers(), self.game.getNumberOfBarriers(), self.game.getNumberOfBots())
            while self.game.checkGameOver():
                end.setWindow()
                pygame.display.update()
            pygame.quit()


if __name__ == "__main__":
    # width = int(input('Width'))
    # nbPlayer = int(input('Nb Player'))
    # nbBarrier = int(input('Nb barrier'))
    width = 5
    nbBarrier = 10
    nbPlayer = 4
    nbBot = 0
    G = GraphicalGame(width, nbPlayer, nbBarrier, nbBot)
    G.mainLoop()
