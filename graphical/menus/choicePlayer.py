import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu


class NumberPlayer(Menu):
    def __init__(self, multi: bool = False):
        super().__init__()
        self.multi = multi

        self.pos1 = (self.buttonX - (self.buttonWidth*0.7), 250)
        self.pos2 = (self.buttonX + (self.buttonWidth*0.7), 250)
        self.pos3 = (self.buttonX - (self.buttonWidth*0.7), 420)
        self.pos4 = (self.buttonX + (self.buttonWidth*0.7), 420)

        self.Rect1 = pygame.Rect(
            self.pos1, self.buttonSize)
        self.Rect2 = pygame.Rect(
            self.pos2, self.buttonSize)
        self.Rect3 = pygame.Rect(
            self.pos3, self.buttonSize)
        self.Rect4 = pygame.Rect(
            self.pos4, self.buttonSize)

    def ButtonBack(self) -> pygame.Rect:
        coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                 (70, 60), (30, 60), (30, 70)]
        button = pygame.draw.polygon(self.window, self.darkBlue, coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)
        return button

    def Event(self):
        from graphical.menus.choiceBot import NumberBots
        from graphical.menus.sizeGrid import SizeGrid
        from graphical.menus.type import Menutype

        PlayersFromPos = {self.pos1: [NumberBots, 1], self.pos2: [NumberBots, 2],
                          self.pos3: [SizeGrid, (3, 1, 1)], self.pos4: [SizeGrid, (4, 0, 1)]}
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                raise SystemExit
            elif not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                return

            for pos in PlayersFromPos.keys():
                if pygame.Rect(pos, self.buttonSize).collidepoint(event.pos):
                    pygame.init()
                    if type(PlayersFromPos[pos][1]) == tuple:
                        board = PlayersFromPos[pos][0](*PlayersFromPos[pos][1])
                    else:
                        board = PlayersFromPos[pos][0](PlayersFromPos[pos][1])
                    while True:
                        board.setWindow()
                        pygame.display.update()
            if self.ButtonBack().collidepoint(event.pos) and event.button == 1:
                pygame.init()
                board = Menutype()
                while True:
                    board.setWindow()
                    pygame.display.update()

    def setWindow(self):
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
        Button(self.window, self.Rect1, self.blue, "1")
        Button(self.window, self.Rect2, self.blue, "2")
        Button(self.window, self.Rect3, self.blue, "3")
        Button(self.window, self.Rect4, self.blue, "4")
        self.ButtonBack()
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = NumberPlayer()

    while True:
        board.setWindow()
        pygame.display.update()
