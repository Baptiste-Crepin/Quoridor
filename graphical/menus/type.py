import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from graphical.menus.choiceHost import ChoiceHost
from Play import Play


class Menutype(Menu):
    def __init__(self):
        super().__init__()

        self.posSolo = (self.buttonX, 200)
        self.posMulti = (self.buttonX, 370)

        self.soloButton = pygame.Rect(
            self.buttonX, 200, self.buttonWidth, self.buttonHeight)
        self.multiButton = pygame.Rect(
            self.buttonX, 370, self.buttonWidth, self.buttonHeight)

    def mainLoop(self):
        self.window.fill(self.backGround)
        Button(self.window, self.soloButton, self.blue, "Solo")
        Button(self.window, self.multiButton, self.blue, "Multi")
        self.back.drawButton()
        self.Event()

    def Event(self):
        from graphical.menus.choicePlayer import NumberPlayer

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posSolo, self.buttonSize).collidepoint(event.pos):

                    board = NumberPlayer()
                    while True:
                        board.mainLoop()
                        pygame.display.update()

                elif pygame.Rect(self.posMulti, self.buttonSize).collidepoint(event.pos):
                    board = ChoiceHost()
                    while True:
                        board.mainLoop()
                        pygame.display.update()

                self.back.Event(event, Play)

            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Menutype()

    while True:
        board.mainLoop()
        pygame.display.update()
