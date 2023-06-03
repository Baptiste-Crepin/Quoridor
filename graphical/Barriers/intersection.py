import pygame
from .barrier import Barrier


class Intersection(Barrier):
    def __init__(self, boardX, boardY, col, i: int = 0, j: int = 0):
        super().__init__(boardX, boardY, col, i, j)
        self.grey = pygame.Color(217, 217, 217, 68)

    def setWidth(self) -> int:
        return self.cellTemplate.offset

    def setHeight(self) -> int:
        return self.cellTemplate.offset

    def coordX(self, i: int) -> float:
        return self.cellTemplate.height * (i)-self.cellTemplate.offset/2+self.cellTemplate.sizeCase()

    def coordY(self, j: int) -> float:
        return self.cellTemplate.width * (j)-self.cellTemplate.offset/2+self.cellTemplate.sizeCase()
