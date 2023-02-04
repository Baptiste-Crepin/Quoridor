from game import Game
from Table import Board


class GraphicalGame():
    def __init__(self, width) -> None:
        self.game = Game(width, 2)
        self.board = Board(self.game.getSquareWidth())

    def mainLoop(self) -> None:
        while self.board.play:
            self.board.handleEvents()

            self.board.newFrame()


if __name__ == "__main__":
    width = int(input('Width'))
    G = GraphicalGame(width)
    G.mainLoop()
