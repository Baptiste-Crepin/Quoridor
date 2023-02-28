from game import Game
from Table import Board


class GraphicalGame():
    def __init__(self, width, nbPlayer, nbBarrier) -> None:
        self.game = Game(width, nbPlayer, nbBarrier)
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
        self.board.player = self.game.getCurrentPlayer()
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
        self.highlightPlayer(self.game.getCurrentPlayer())
        self.highlightBarrier()

    def mainLoop(self) -> None:
        self.highlightPlayer(self.game.getCurrentPlayer())
        self.highlightBarrier()
        while self.board.play:
            while not self.game.checkGameOver():
                self.placement()
                self.actualizeGame()

                self.board.newFrame()
            # TODO: Game has ended. display the end screen
            self.board.newFrame()


if __name__ == "__main__":
    # width = int(input('Width'))
    # nbPlayer = int(input('Nb Player'))
    # nbBarrier = int(input('Nb barrier'))
    width = 5
    nbBarrier = 4
    nbPlayer = 4
    G = GraphicalGame(width, nbPlayer, nbBarrier)
    G.mainLoop()
