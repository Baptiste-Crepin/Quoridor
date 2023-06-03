from graphical.menus.tablePlayer import TablePlayer
import pygame


class Barrier():
    def __init__(self, boardX: int, boardY: int, col: int, i: int = 0, j: int = 0) -> None:
        self.cellTemplate = TablePlayer(boardX, boardY, col)
        self.boardX = boardX
        self.boardY = boardY
        self.col = col
        self.x = self.coordX(i)
        self.y = self.coordY(j)
        self.height = self.setHeight()
        self.width = self.setWidth()
        self.possiblePlacement = False
        self.placed = False
        self.hover = False

    def draw(self, surface: pygame.Surface, color: pygame.Color) -> None:
        rectValues = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, color, rectValues)

    def collides(self, otherCoord: tuple[int, int]) -> bool:
        if otherCoord[1] < self.y or otherCoord[1] > self.y + self.height:
            return False
        if otherCoord[0] < self.x or otherCoord[0] > self.x + self.width:
            return False

        return True

    def setWidth(self) -> int:
        raise NotImplementedError("setWidth implemented in subclass")

    def setHeight(self) -> int:
        raise NotImplementedError("setHeight implemented in subclass")

    def coordX(self, i: int) -> float:
        raise NotImplementedError("coordX implemented in subclass")

    def coordY(self, j: int) -> float:
        raise NotImplementedError("coordY implemented in subclass")
