import pygame
from player import Player


class displayInformation():
    def __init__(self, player: Player, playerlist: list[Player], surface: pygame.Surface, color: pygame.Color, rect: pygame.Rect, playerNumber: int) -> None:
        self.player = player
        self.playerList = playerlist
        self.surface = surface
        self.color = color
        self.rect = rect
        self.playerNumber = playerNumber

    def RectNeutral(self, ) -> None:
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=10)

    def playerCircles(self) -> None:
        center = (self.rect[0]+self.rect[2]*0.05, self.rect[1]+self.rect[3]//2)
        pygame.draw.circle(self.surface, self.player.getColor(), center, 20)

    def displayNeutral(self) -> None:
        self.RectNeutral()
        self.playerCircles()
