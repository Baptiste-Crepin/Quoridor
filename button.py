from pygame.locals import *
import pygame


class Button():
    def __init__(self, surface: pygame.Surface, rect: pygame.Rect, color: pygame.Color, text: str, fontSize: int = 60) -> None:
        self.surface = surface
        self.rect = rect
        self.color = color
        self.text = text
        self.fontSize = fontSize
        self.white = (255, 255, 255)
        self.createButton()

    def createButton(self):
        button_rect = pygame.draw.rect(
            self.surface, self.color, self.rect, border_radius=20)
        font = pygame.font.SysFont(
            "Extra Bold Italic", self.fontSize, False, True)
        text = font.render(self.text, True, self.white)
        buttonText = text.get_rect(center=button_rect.center)
        self.surface.blit(text, buttonText)
