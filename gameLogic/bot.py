from gameLogic.player import Player
import random
import time


class Bot(Player):
    def __init__(self, number: int, barriers: int):
        super().__init__(number, barriers)

    def randomMove(self, possibleMoves: list[tuple[int, int]]) -> tuple[int, int]:
        return possibleMoves[random.randint(0, len(possibleMoves)-1)]

    def randomBarrier(self, possibleBarrierPlacement: list[tuple[tuple[int, int], str]]) -> tuple[tuple[int, int], str]:
        return possibleBarrierPlacement[random.randint(0, len(possibleBarrierPlacement)-1)]

    def randomAction(self, possibleBarrierPlacement: list[tuple[tuple[int, int], str]]) -> int:
        """
        return 1 if the bot wants to place a barrier, 0 if it wants to move
        sleeps for 0.4 seconds for the player to see the bot's move
        """
        time.sleep(0.4)
        return random.randint(0, 1) if possibleBarrierPlacement else 0
