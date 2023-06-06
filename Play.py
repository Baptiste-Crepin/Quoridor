import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu


class Play(Menu):
    def __init__(self) -> None:
        super().__init__()

        self.posPlay = (self.buttonX, 200)
        self.posRules = (self.buttonX, 370)

        self.playButton = pygame.Rect(
            self.buttonX, 200, self.buttonWidth, self.buttonHeight)
        self.rulesButton = pygame.Rect(
            self.buttonX, 370, self.buttonWidth, self.buttonHeight)

    def Event(self) -> None:
        from graphical.menus.rules import Rules
        from graphical.menus.type import Menutype
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posPlay, self.buttonSize).collidepoint(event.pos):
                    # pygame.init()
                    board = Menutype()
                    while True:
                        board.mainLoop()
                        pygame.display.update()

                elif pygame.Rect(self.posRules, self.buttonSize).collidepoint(event.pos):
                    # pygame.init()
                    board = Rules()
                    while True:
                        board.mainLoop()
                        pygame.display.update()

    def mainLoop(self) -> None:
        self.window.fill(self.backGround)

        Button(self.window, self.playButton, self.blue, "PLAY")
        Button(self.window, self.rulesButton, self.blue, "RULES")
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Play()

    while True:
        board.mainLoop()
        pygame.display.update()
