import pygame
from graphical.widgets.input import Input
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu


class ServerName(Menu):
    def __init__(self, width: int, nbPlayer: int, nbBarrier: int, nbBot: int) -> None:
        super().__init__()
        self.width = width
        self.nbPlayer = nbPlayer
        self.nbBarrier = nbBarrier
        self.nbBot = nbBot

        self.posPlay = (50, 200)
        self.posRules = (50, 370)
        # self.purple = pygame.Color(204, 0, 204)
        self.input = Input(self.window, pygame.Rect(
            140, 325, 220, 50), self.white)

    def Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
            self.input.Event(event)

    def mainLoop(self):
        self.window.fill(self.darkBlue, rect=None, special_flags=0)
        font = pygame.font.SysFont(
            "Extra Bold Italic", 60, False, True)
        text = font.render(
            "chose the name of", True, self.white)
        secondtext = font.render(
            "the server", True, self.white)
        self.input.createInput()
        self.window.blit(text, (70, 230))
        self.window.blit(secondtext, (150, 270))

        Button(self.window, pygame.Rect(
            175, 400, 150, 50), self.lighterBlue, "send", 40, 10)

        self.Event()
        pygame.display.flip()
