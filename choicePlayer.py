import pygame
from pygame.locals import *
from button import Button


class NumberPlayer:
    def __init__(self):
        self.windowXmax = 500
        self.windowYmax = 700
        self.pos1 = (100, 250)
        self.pos2 = (300, 250)
        self.pos3 = (100, 420)
        self.pos4 = (300, 420)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.blue = (138, 201, 244)
        self.white = (255, 255, 255)
        self.darkerBlue = (0, 0, 48)
        self.black = (0, 0, 0)
        self.font = pygame.font.Font(None, 36)
        self.Rect1 = (100, 230, 100, 100)
        self.Rect2 = (300, 230, 100, 100)
        self.Rect3 = (100, 420, 100, 100)
        self.Rect4 = (300, 420, 100, 100)

    def ButtonBack(self) -> object:
        coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                 (70, 60), (30, 60), (30, 70)]
        button = pygame.draw.polygon(self.window, self.darkerBlue, coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)
        return button

    def Event(self):
        from choiseBot import NumberBots
        from sizeGrid import SizeGrid
        from type import Menutype

        PlayersFromPos = {self.pos1: [NumberBots, 1], self.pos2: [NumberBots, 2],
                          self.pos3: [SizeGrid, (3, 1, 1)], self.pos4: [SizeGrid, (4, 0, 1)]}
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
            elif not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                return

            for pos in PlayersFromPos.keys():
                if pygame.Rect(pos, (70, 100)).collidepoint(event.pos):
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
        backGround = pygame.image.load('pictures/backGroundMenu3.jpg')
        self.window.blit(backGround, (-80, -300))

        text_surface = self.font.render("How many players?", True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 50))

        contour_surface = self.font.render(
            "How many players?", True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(
            center=(self.windowXmax // 2, 50))
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
