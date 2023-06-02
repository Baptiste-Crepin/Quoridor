from player import Player
import random
import time


class Bot(Player):
    def __init__(self, number: int, barriers):
        super().__init__(number, barriers)

    def randomInArray(self, Array: list) -> tuple:
        return Array[random.randint(0, len(Array)-1)]

    def randomMoves(self, possibleBarrierPlacement: list[tuple[tuple[int, int], str]], possibleMoves: list[tuple[int, int]]) -> tuple[str, tuple[int, int]]:
        time.sleep(0.5)
        # remainingBarriers = len(game.possibleBarrierPlacement(self))
        # i = 1
        # if remainingBarriers:
        #     i = random.randint(0, 1)
        # if i:
        #     coordo = self.randomInArray(
        #         game.possibleMoves(self.getCoordinates()))
        #     game.movePlayer(self, coordo)
        # else:
        #     barriermove = self.randomInArray(
        #         game.possibleBarrierPlacement(self))
        #     game.placeWall(barriermove[0], barriermove[1], self)
        remainingBarriers = len(possibleBarrierPlacement)
        i = 1
        if remainingBarriers:
            i = random.randint(0, 1)
        if i:
            coordo = self.randomInArray(possibleMoves)
            return ("Move", coordo)
        else:
            barriermove = self.randomInArray(possibleBarrierPlacement)
            return ("Placement", barriermove)
