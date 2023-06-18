import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu


class Play(Menu):
    def __init__(self, fullScreen: bool = False) -> None:
        super().__init__(fullScreen)

    def calculateElements(self) -> None:
        self.posPlay = (self.buttonX, self.windowHeight *
                        0.25 - self.buttonHeight//2)
        self.posRules = (self.buttonX, self.windowHeight *
                         0.50 - self.buttonHeight//2)
        self.posQuit = (self.buttonX, self.windowHeight *
                        0.75 - self.buttonHeight//2)

        self.playButton = pygame.Rect(
            self.posPlay, (self.buttonWidth, self.buttonHeight))
        self.rulesButton = pygame.Rect(
            self.posRules, (self.buttonWidth, self.buttonHeight))
        self.quitButton = pygame.Rect(
            self.posQuit, (self.buttonWidth, self.buttonHeight))

    def Event(self) -> None:
        from graphical.menus.rules import Rules
        from graphical.menus.type import Menutype
        for event in pygame.event.get():
            self.defaultEventHandler(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posPlay, self.buttonSize).collidepoint(event.pos):
                    board = Menutype(self.fullScreen)
                    self.newMenu(self, board)
                elif pygame.Rect(self.posRules, self.buttonSize).collidepoint(event.pos):
                    board = Rules(self.fullScreen)
                    self.newMenu(self, board)
                elif pygame.Rect(self.posQuit, self.buttonSize).collidepoint(event.pos):
                    raise SystemExit

    def mainLoop(self) -> None:
        self.window.fill(self.backGround)

        Button(self.window, self.playButton, self.blue, "PLAY")
        Button(self.window, self.rulesButton, self.blue, "RULES")
        Button(self.window, self.quitButton, self.blue, "QUIT")
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Play()

    while True:
        board.mainLoop()
        pygame.display.update()
