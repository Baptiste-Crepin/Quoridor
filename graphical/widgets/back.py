import pygame
from typing import Any


class Back():
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface

        self.darkBlue = pygame.Color(0, 0, 48)
        self.white = pygame.Color(255, 255, 255)

        self.coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                      (70, 60), (30, 60), (30, 70)]

    def drawButton(self):
        button = pygame.draw.polygon(self.surface, self.darkBlue, self.coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.surface.blit(text, buttonText)
        return button

    def Event(self, event: pygame.event.Event, oldMenu: object, newMenu: object, args: Any = None) -> None:
        from graphical.widgets.menu import Menu
        if not self.drawButton().collidepoint(event.pos):
            return
        if args:
            if isinstance(args, tuple):
                board = newMenu(*(args))  # type: ignore
            else:
                board = newMenu(args)  # type: ignore
        else:
            board = newMenu()  # type: ignore
        Menu.newMenu(oldMenu, board)  # type: ignore
