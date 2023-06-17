import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from graphical.menus.choicePlayer import NumberPlayer


class SizeGrid(Menu):
    def __init__(self, nbPlayer: int, nbBot: int, method: int, multi: bool = False, fullScreen: bool = False) -> None:
        super().__init__(fullScreen)
        self.nbPlayers = nbPlayer
        self.method = method
        self.nbBot = nbBot
        self.multi = multi

        self.initializeButton()

    def initializeButton(self):
        yPos = self.windowHeight // 3
        self.posButton1 = (self.buttonX - (self.buttonWidth*0.7), yPos)
        self.posButton2 = (self.buttonX + (self.buttonWidth*0.7), yPos)
        self.posButton3 = (self.buttonX - (self.buttonWidth*0.7), yPos * 2)
        self.posButton4 = (self.buttonX + (self.buttonWidth*0.7), yPos * 2)

    def Event(self):
        from graphical.menus.choiceBarrier import selectBarrier
        sizeFromPos = {self.posButton1: 5, self.posButton3: 9,
                       self.posButton2: 7, self.posButton4: 11}

        for event in pygame.event.get():
            self.defaultEventHandler(event)
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                return

            for pos in sizeFromPos:
                if pygame.Rect(pos, self.buttonSize).collidepoint(event.pos):
                    board = selectBarrier(
                        self.nbPlayers, self.nbBot, sizeFromPos[pos], self.method, self.multi, self.fullScreen)
                    self.newMenu(self, board)

            self.back.Event(event, self, NumberPlayer, (self.multi))

    def mainLoop(self) -> None:
        self.window.fill(self.backGround)

        text_surface = self.font.render(
            "Choise the size of the grid", True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowWidth // 2, 50))

        contour_surface = self.font.render(
            "Choise the size of the grid", True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(
            center=(self.windowWidth // 2, 50))
        contour_rect.move_ip(2, 2)

        self.window.blit(contour_surface, contour_rect)
        self.window.blit(text_surface, text_rect)

        Button(self.window, pygame.Rect(
            self.posButton1, self.buttonSize), self.blue, "5X5")
        Button(self.window, pygame.Rect(
            self.posButton2, self.buttonSize), self.blue, "7X7")
        Button(self.window, pygame.Rect(
            self.posButton3, self.buttonSize), self.blue, "9X9")
        Button(self.window, pygame.Rect(
            self.posButton4, self.buttonSize), self.blue, "11X11")

        self.back.drawButton()
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = SizeGrid(2, 0, 1)

    while True:
        board.mainLoop()
        pygame.display.update()
