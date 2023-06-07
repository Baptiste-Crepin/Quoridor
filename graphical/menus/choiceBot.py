import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from graphical.menus.choicePlayer import NumberPlayer


class NumberBots(Menu):
    def __init__(self, nbPlayers: int, multi: bool = False) -> None:
        super().__init__()
        self.nbPlayers = nbPlayers
        self.multi = multi

        self.initializeButton()

    def initializeButton(self) -> None:
        self.ypos = self.windowHeight // 3
        self.firstRect = (self.buttonX,
                          self.ypos,
                          self.buttonWidth,
                          self.buttonHeight)
        self.secondRect = (self.buttonX,
                           self.ypos*2,
                           self.buttonWidth,
                           self.buttonHeight)

    def Event(self, method: int) -> None:
        from graphical.menus.sizeGrid import SizeGrid
        nbBotsFromPos = {
            1: {
                self.firstRect: 1,
                self.secondRect: 3},
            2: {
                self.firstRect: 2,
                self.secondRect: 0}
        }

        for event in pygame.event.get():
            self.defaultEventHandler(event)
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                return

            for pos in nbBotsFromPos[method]:
                if pygame.Rect(pos).collidepoint(event.pos):
                    board = SizeGrid(self.nbPlayers,
                                     nbBotsFromPos[method][pos], method, self.multi)
                    self.newMenu(self, board)

            self.back.Event(event, self, NumberPlayer, (self.multi))

    def displayChoice(self, message: str, button1Txt: str, button2Txt: str, method: int) -> None:
        text_surface = self.font.render(message, True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowWidth // 2, 50))

        contour_surface = self.font.render(message, True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(center=(self.windowWidth // 2, 50))
        contour_rect.move_ip(2, 2)

        self.window.blit(contour_surface, contour_rect)
        self.window.blit(text_surface, text_rect)

        Button(self.window, pygame.Rect(self.firstRect), self.blue, button1Txt)
        Button(self.window, pygame.Rect(self.secondRect), self.blue, button2Txt)
        self.back.drawButton()
        self.Event(method)

    def mainLoop(self) -> None:
        self.window.fill(self.backGround)
        if self.nbPlayers == 1:
            self.displayChoice("How many bots?", "1", "3", 1)
        elif self.nbPlayers == 2:
            self.displayChoice(
                "Do you want to play with bots?", "Yes", "No", 2)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = NumberBots(2)

    while True:
        board.mainLoop()
        pygame.display.update()
