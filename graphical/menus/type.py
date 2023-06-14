import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from graphical.menus.choiceHost import ChoiceHost
from main import Play


class MenuType(Menu):
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
            self.defaultEventHandler(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posSolo, self.buttonSize).collidepoint(event.pos):

                    board = NumberPlayer()
                    self.newMenu(self, board)

                elif pygame.Rect(self.posMulti, self.buttonSize).collidepoint(event.pos):
                    board = ChoiceHost()
                    self.newMenu(self, board)

                self.back.Event(event, self, Play)

            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = MenuType()

    while True:
        board.mainLoop()
        pygame.display.update()
