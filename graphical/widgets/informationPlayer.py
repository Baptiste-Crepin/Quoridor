import pygame
from player import Player


class informationPlayer():
    def __init__(self, surface: pygame.Surface, color: pygame.Color, rect: pygame.Rect, player: Player, score: list[int] = [0, 0, 0, 0]) -> None:
        self.surface = surface
        self.color = color
        self.white = (255, 255, 255)
        self.purple = pygame.Color(204, 0, 204)
        self.rect = rect
        self.player = player
        self.score = score
        self.font = pygame.font.Font(None, 36)

    def barrerCoordX(self) -> int:
        x = self.rect[3]//2+self.rect[1]
        return x

    def barrerCoordY(self, i: int) -> int:
        y = ((self.rect[2])//self.player.getBarrier()*i+self.rect[0]) + \
            ((self.rect[2]//self.player.getBarrier())//2-self.barrerWidth()//2)
        return y

    def barrerWidth(self) -> int:
        width = 20
        return width

    def barrerHeight(self) -> int:
        height = self.rect[3]//2
        return height

    def createRectPlayer(self) -> None:
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=10)
        textbarrer = self.font.render(
            "win:" + str(self.score[self.player.getNumber()-1]), True, self.white)
        self.surface.blit(
            textbarrer, (self.rect[0] + self.rect[2] - 100, self.rect[1] + 10))
        coordPlayer = (self.rect[0]+self.rect[2]*0.05,
                       self.rect[1]+self.rect[2]*0.05)
        pygame.draw.circle(
            self.surface, self.player.getColor(), coordPlayer, 20)
        for i in range(self.player.getBarrier()):
            pygame.draw.rect(self.surface, self.purple, (self.barrerCoordY(
                i), self.barrerCoordX(), self.barrerWidth(), self.barrerHeight()))
