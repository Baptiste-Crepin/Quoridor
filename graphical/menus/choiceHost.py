import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from graphical.menus.choicePlayer import NumberPlayer


class ChoiceHost(Menu):
    def __init__(self):
        super().__init__()

        self.posHost = (self.buttonX, 200)
        self.posJoin = (self.buttonX, 370)

        self.soloButton = pygame.Rect(
            self.buttonX, 200, self.buttonWidth, self.buttonHeight)
        self.multiButton = pygame.Rect(
            self.buttonX, 370, self.buttonWidth, self.buttonHeight)

    def mainLoop(self):
        self.window.fill(self.backGround)
        Button(self.window, self.soloButton, self.blue, "Host")
        Button(self.window, self.multiButton, self.blue, "Join")
        self.back.drawButton()
        self.Event()

    def Event(self):
        from graphical.menus.type import Menutype
        from graphical.menus.choiceServer import ChoiceServer

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posHost, self.buttonSize).collidepoint(event.pos):
                    board = NumberPlayer(True)
                    while True:
                        board.mainLoop()
                        pygame.display.update()

                elif pygame.Rect(self.posJoin, self.buttonSize).collidepoint(event.pos):
                    board = ChoiceServer()
                    while True:
                        board.mainLoop()
                        pygame.display.update()

                self.back.Event(event, Menutype)
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = ChoiceHost()

    while True:
        board.mainLoop()
        pygame.display.update()
