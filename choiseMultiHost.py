import pygame
from pygame.locals import *
from type import Menutype


class Menu:
    def __init__(self) -> None:
        self.windowXmax = 500
        self.windowYmax = 700
        self.posPlay = (50, 200)
        self.posRules = (50, 370)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.choise = False
        self.blue = (138, 201, 244)
        self.white = (255, 255, 255)

    def createButtonHost(self) -> None:
        button = pygame.draw.rect(
            self.window, self.blue, (50, 200, 400, 120), width=0, border_radius=20)
        font = pygame.font.SysFont("Extra Bold Italic", 60, False, True)
        text = font.render("HOST", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def createButtonJoin(self) -> None:
        button = pygame.draw.rect(
            self.window, self.blue, (50, 370, 400, 120), width=0, border_radius=20)
        font = pygame.font.SysFont("Extra Bold Italic", 60, False, True)
        text = font.render("JOIN", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def Event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.choise = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posPlay, (400, 120)).collidepoint(event.pos):
                    pygame.quit()
                elif pygame.Rect(self.posRules, (400, 120)).collidepoint(event.pos):
                    pygame.quit()

        pygame.display.flip()

    def mainLoop(self) -> None:
        backGround = pygame.image.load('pictures/Foret.jpg')
        self.window.blit(backGround, (0, 0))
        self.createButtonHost()
        self.createButtonJoin()
        self.Event()

    def getChoise(self) -> bool:
        return self.choise


if __name__ == "__main__":
    pygame.init()
    board = Menu()

    while not board.getChoise():
        board.mainLoop()
        pygame.display.update()

    pygame.quit()
