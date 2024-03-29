import pygame

from gameLogic.player import Player


class displayInformation():
    def __init__(self, player: Player, playerList: list[Player], surface: pygame.Surface, color: pygame.Color, rect: pygame.Rect, playerNumber: int, score: list[int] = [0, 0, 0, 0]) -> None:
        self.player = player
        self.playerList = playerList
        self.surface = surface
        self.color = color
        self.rect = rect
        self.playerNumber = playerNumber
        self.score = score
        self.purple = pygame.Color(204, 0, 204)
        self.white = pygame.Color(255, 255, 255)
        self.font = pygame.font.Font(None, 36)

    def RectNeutral(self, ) -> None:
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=10)

    def playerCircles(self) -> None:
        center = (self.rect[0] + self.rect[2] * 0.05,
                  self.rect[1] + self.rect[3] // 2)
        pygame.draw.circle(self.surface, self.player.getColor(), center, 20)

    def playerBarrier(self) -> None:
        pygame.draw.rect(self.surface, self.purple, pygame.Rect(
            self.rect[0] + self.rect[2] // 2, self.rect[1], 15, self.rect[3]))
        textBarrier = self.font.render(
            f"x{str(self.player.getBarrier())}", True, self.white
        )
        self.surface.blit(
            textBarrier, (self.rect[0] + self.rect[2] // 2 + 20, self.rect[1] + 10))

    def displayScore(self):
        textBarrier = self.font.render(
            f"win:{str(self.score[self.playerNumber])}", True, self.white)
        self.surface.blit(
            textBarrier, (self.rect[0] + self.rect[2] - 100, self.rect[1] + 10))

    def displayNeutral(self) -> None:
        self.RectNeutral()
        self.playerCircles()
        self.playerBarrier()
        self.displayScore()
