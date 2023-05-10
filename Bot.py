from Player import Player
import random
import time


class Bot(Player):
    def __init__(self, number: int, barriers):
        super().__init__(number, barriers)
        self.__level = 0

    def getLevel(self) -> int:
        return self.__level

    def setLevel(self, value: int) -> None:
        self.__level = value

    def randomInArray(self, Array: list) -> tuple:
        return Array[random.randint(0, len(Array)-1)]

    def randomMoves(self, game: object):
        time.sleep(0.5)
        remainingBarriers = len(game.possibleBarrierPlacement(self))
        i = 1
        if remainingBarriers:
            i = random.randint(0, 1)
        if i:
            coordo = self.randomInArray(
                game.possibleMoves(self.getCoordinates()))
            game.movePlayer(self, coordo)
        else:
            barriermove = self.randomInArray(
                game.possibleBarrierPlacement(self))
            game.placeWall(barriermove[0], barriermove[1], self)
