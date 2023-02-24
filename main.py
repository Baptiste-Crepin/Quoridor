from game import Game
from Table import Board


class GraphicalGame():
    def __init__(self, width, nbPlayer, nbBarrier) -> None:
        self.game = Game(width, nbPlayer, nbBarrier)
        self.board = Board(self.game.getSquareWidth())

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

        if action == 'move' and not self.game.movePawn(clickCoordo, self.game.getCurrentPlayer()):
            return

        if action == 'placeV':
            if not self.game.placeWall(clickCoordo, 'Right', self.game.getCurrentPlayer()):
                return

        if action == 'placeH':
            if not self.game.placeWall(clickCoordo, 'Down', self.game.getCurrentPlayer()):
                return

        self.game.display()

        self.game.NextPlayer()

    def mainLoop(self) -> None:

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