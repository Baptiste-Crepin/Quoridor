import pygame
from gameLogic.player import Player


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

    def barrierCoordX(self) -> int:
        return self.rect[3]//2+self.rect[1]

    def barrierCoordY(self, i: int) -> int:
        return ((self.rect[2])//self.player.getBarrier()*i+self.rect[0]) + \
            ((self.rect[2]//self.player.getBarrier()) //
             2-self.barrierWidth()//2)

    def barrierWidth(self) -> int:
        return 20

    def barrierHeight(self) -> int:
        return self.rect[3]//2

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
            pygame.draw.rect(self.surface, self.purple, (self.barrierCoordY(
                i), self.barrierCoordX(), self.barrierWidth(), self.barrierHeight()))
