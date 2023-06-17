import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from graphical.menus.choiceHost import ChoiceHost
from Play import Play


class Menutype(Menu):
    def __init__(self, fullScreen: bool = False):
        super().__init__(fullScreen)


    def calculateElements(self) -> None:
        self.posSolo = (self.buttonX, self.windowHeight *
                        0.40 - self.buttonHeight//2)
        self.posMulti = (self.buttonX, self.windowHeight *
                         0.60 - self.buttonHeight//2)

        self.soloButton = pygame.Rect(
            self.posSolo, (self.buttonWidth, self.buttonHeight))
        self.multiButton = pygame.Rect(
            self.posMulti, (self.buttonWidth, self.buttonHeight))

    def mainLoop(self):
        self.window.fill(self.backGround)
        Button(self.window, self.soloButton, self.blue, "Solo")
        Button(self.window, self.multiButton, self.blue, "Multi")
        self.back.drawButton()
        self.Event()

    def Event(self):
        from graphical.menus.choicePlayer import NumberPlayer

        for event in pygame.event.get():
            self.defaultEventHandler(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posSolo, self.buttonSize).collidepoint(event.pos):

                    board = NumberPlayer(
                        multi=False, fullScreen=self.fullScreen)
                    self.newMenu(self, board)

                elif pygame.Rect(self.posMulti, self.buttonSize).collidepoint(event.pos):
                    board = ChoiceHost(self.fullScreen)
                    self.newMenu(self, board)

                self.back.Event(event, self, Play, self.fullScreen)

            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Menutype()

    while True:
        board.mainLoop()
        pygame.display.update()
