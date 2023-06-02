import pygame
from player import Player


class TablePlayer:
    def __init__(self, boardX: int, boardY: int, col: int, i: int = 0, j: int = 0) -> None:
        self.boardX = boardX
        self.boardY = boardY
        self.col = col
        self.player = Player(0)
        self.highlighted = False
        self.hover = False

        self.width = self.sizeCase()
        self.height = self.sizeCase()
        self.offset = self.offsetCase()

        self.x = 0
        self.y = 0
        self.setCoordFromIndex(i, j)

    def sizeCase(self) -> int:
        return (self.boardY // self.col)

    def offsetCase(self) -> int:
        totalMargin = 100
        return self.boardY // (self.width * self.col) + (totalMargin//self.col)

    def setCoordFromIndex(self, i: int, j: int) -> None:
        self.x = self.coord(i)
        self.y = self.coord(j)

    def coord(self, i: int) -> int:
        return i * (self.width)

    def drawCase(self, surface: pygame.Surface, color: pygame.Color) -> None:
        x = self.x + self.offset//2
        y = self.y + self.offset//2
        width = self.width - self.offset
        height = self.height - self.offset
        rectValues = (x, y, width, height)

        pygame.draw.rect(surface, color, rectValues)

    def collides(self, otherCoord: tuple[int, int]) -> bool:
        if otherCoord[1] < self.y or otherCoord[1] > self.y + self.width:
            return False
        if otherCoord[0] < self.x or otherCoord[0] > self.x + self.height:
            return False
        return True
