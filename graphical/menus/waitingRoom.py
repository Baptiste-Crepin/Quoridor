import pygame
from graphical.widgets.button import Button


class waitingRoom():
    def __init__(self) -> None:
        self.height = 700
        self.width = 500
        self.window = pygame.display.set_mode((self.height, self.width))
        pygame.display.set_caption("Quoridor")
        self.white = pygame.Color(255, 255, 255)
        self.grey = pygame.Color(217, 217, 217, 35)
        self.black = pygame.Color(0, 0, 0)
        self.darkBlue = pygame.Color(0, 0, 48)
        self.lightBlue = pygame.Color(90, 173, 255)
        self.purple = pygame.Color(204, 0, 204)
