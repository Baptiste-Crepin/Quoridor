from player import Player
import random
import time


class Bot(Player):
    def __init__(self, number: int, barriers):
        super().__init__(number, barriers)

    def randomInArray(self, Array: list) -> tuple:
        return Array[random.randint(0, len(Array)-1)]

    def randomMoves(self, possibleBarrierPlacement: list[tuple[tuple[int, int], str]], possibleMoves: list[tuple[int, int]]) -> tuple[int, int] or tuple[tuple[int, int], str]:
        time.sleep(0.5)
        remainingBarriers = len(possibleBarrierPlacement)
        i = 1
        if remainingBarriers:
            i = random.randint(0, 1)
        if i:
            return self.randomInArray(possibleMoves)
        else:
            return self.randomInArray(possibleBarrierPlacement)
