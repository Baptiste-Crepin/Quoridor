from game import Game
from Table import Board
from Bot import Bot


class GraphicalGame():
    def __init__(self, width, nbPlayer, nbBarrier, nbBots, num=0) -> None:
        self.game = Game(width, nbPlayer, nbBarrier, nbBots, num)
        self.board = Board (self.game.getSquareWidth(), num)

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
        if isinstance(self.game.getCurrentPlayer(), Bot):
            self.board.newFrame(self.game.getCurrentPlayer())
            self.game.getCurrentPlayer().randomMoves(self.game)
            self.game.nextPlayer()
            return

        event = self.board.handleEvents(self.game.getCurrentPlayer())
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
        while self.board.play:
            while not self.game.checkGameOver():
                self.displayPossibleMoves()

                self.placement()
                self.actualizeGame()

                self.board.newFrame(self.game.getCurrentPlayer())
            # TODO: Game has ended. display the end screen
            self.board.newFrame(self.game.getCurrentPlayer())


if __name__ == "__main__":
    # width = int(input('Width'))
    # nbPlayer = int(input('Nb Player'))
    # nbBarrier = int(input('Nb barrier'))
    width = 5
    nbBarrier = 4
    nbPlayer = 2
    nbBot = 0
    G = GraphicalGame(width, nbPlayer, nbBarrier, nbBot)
    G.mainLoop()
