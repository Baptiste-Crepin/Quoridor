import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu


class NumberPlayer(Menu):
    def __init__(self, multi: bool = False, fullScreen: bool = False):
        super().__init__(fullScreen)
        self.multi = multi
        self.initializeButton()

    def button2pos(self, yOffset: float, yPos: float) -> tuple[float, float]:
        if self.multi:
            return ((self.windowWidth//2) - (self.buttonWidth//2), yPos)
        return (self.buttonX + yOffset, yPos)

    def initializeButton(self):
        offset = self.buttonWidth*0.7
        yPos = self.windowHeight // 3
        self.posRect1 = (self.buttonX - offset, yPos)
        self.posRect2 = self.button2pos(offset, yPos)
        self.posRect3 = (self.buttonX - offset, yPos * 2)
        self.posRect4 = (self.buttonX + offset, yPos * 2)

        self.Rect1 = pygame.Rect(self.posRect1, self.buttonSize)
        self.Rect2 = pygame.Rect(self.posRect2, self.buttonSize)
        self.Rect3 = pygame.Rect(self.posRect3, self.buttonSize)
        self.Rect4 = pygame.Rect(self.posRect4, self.buttonSize)

    def Event(self):
        from graphical.menus.choiceBot import NumberBots
        from graphical.menus.sizeGrid import SizeGrid
        from graphical.menus.type import Menutype

        PlayersFromPos = {self.posRect1: [NumberBots, (1, self.multi)],
                          self.posRect2: [NumberBots, (2, self.multi)],
                          self.posRect3: [SizeGrid, (3, 1, 1, self.multi)],
                          self.posRect4: [SizeGrid, (4, 0, 1, self.multi)]}
        if self.multi:
            PlayersFromPos = {self.posRect2: [SizeGrid, (2, 0, 1, self.multi)],
                              self.posRect3: [SizeGrid, (3, 1, 1, self.multi)],
                              self.posRect4: [SizeGrid, (4, 0, 1, self.multi)]}

        for event in pygame.event.get():
            self.defaultEventHandler(event)
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                return

            for pos in PlayersFromPos:
                if pygame.Rect(pos, self.buttonSize).collidepoint(event.pos):
                    args = PlayersFromPos[pos][1]
                    if not isinstance(args, tuple):
                        continue
                    # calls the constructor of the class in PlayersFromPos[pos][0] with the arguments in PlayersFromPos[pos][1]
                    board = PlayersFromPos[pos][0](
                        *args, self.fullScreen)  # type: ignore
                    if isinstance(board, object):
                        self.newMenu(self, board)

            self.back.Event(event, self, Menutype)

    def mainLoop(self):
        self.window.fill(self.backGround)

        text_surface = self.font.render("How many players?", True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowWidth // 2, 50))

        contour_surface = self.font.render(
            "How many players?", True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(
            center=(self.windowWidth // 2, 50))
        contour_rect.move_ip(2, 2)

        self.window.blit(contour_surface, contour_rect)
        self.window.blit(text_surface, text_rect)
        if not self.multi:
            Button(self.window, self.Rect1, self.blue, "1")
        Button(self.window, self.Rect2, self.blue, "2")
        Button(self.window, self.Rect3, self.blue, "3")
        Button(self.window, self.Rect4, self.blue, "4")
        self.back.drawButton()
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = NumberPlayer()

    while True:
        board.mainLoop()
        pygame.display.update()
