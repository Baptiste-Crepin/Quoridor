import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu


class NumberBots(Menu):
    def __init__(self, nbPlayers: int) -> None:
        super().__init__()
        self.nbPlayers = nbPlayers

        self.pos1 = (self.buttonX, 200)
        self.pos2 = (self.buttonX, 370)

        self.firstRect = (self.buttonX, 200,
                          self.buttonWidth, self.buttonHeight)
        self.secondRect = (self.buttonX, 370,
                           self.buttonWidth, self.buttonHeight)

    def ButtonBack(self) -> pygame.Rect:
        coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                 (70, 60), (30, 60), (30, 70)]
        button = pygame.draw.polygon(self.window, self.darkBlue, coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)
        return button

    def Event(self, method: int) -> None:
        from graphical.menus.sizeGrid import SizeGrid
        from graphical.menus.choicePlayer import NumberPlayer

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                raise SystemExit
            if not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                return

            if method == 1:
                nbBotsFromPos = {self.firstRect: 1, self.secondRect: 3}
            else:
                nbBotsFromPos = {self.firstRect: 2, self.secondRect: 0}

            for pos in nbBotsFromPos.keys():
                if pygame.Rect(pos).collidepoint(event.pos):
                    pygame.init()
                    board = SizeGrid(self.nbPlayers,
                                     nbBotsFromPos[pos], method)
                    while True:
                        board.setWindow()
                        pygame.display.update()

            if self.ButtonBack().collidepoint(event.pos) and event.button == 1:
                pygame.init()
                board = NumberPlayer()
                while True:
                    board.setWindow()
                    pygame.display.update()

    def setWindow(self) -> None:
        self.window.fill(self.backGround)
        if self.nbPlayers == 1:
            text_surface = self.font.render("How many bots?", True, self.white)
            text_rect = text_surface.get_rect(
                center=(self.windowWidth // 2, 50))

            contour_surface = self.font.render(
                "How many bots?", True, (0, 0, 0))
            contour_rect = contour_surface.get_rect(
                center=(self.windowWidth // 2, 50))
            contour_rect.move_ip(2, 2)

            self.window.blit(contour_surface, contour_rect)
            self.window.blit(text_surface, text_rect)

            Button(self.window, pygame.Rect(self.firstRect), self.blue, "1")
            Button(self.window, pygame.Rect(self.secondRect), self.blue, "3")
            self.ButtonBack()
            self.Event(1)

        elif self.nbPlayers == 2:
            text_surface = self.font.render(
                "Do you want to play with bots?", True, self.white)
            text_rect = text_surface.get_rect(
                center=(self.windowWidth // 2, 50))

            contour_surface = self.font.render(
                "Do you want to play with bots?", True, (0, 0, 0))
            contour_rect = contour_surface.get_rect(
                center=(self.windowWidth // 2, 50))
            contour_rect.move_ip(2, 2)

            self.window.blit(contour_surface, contour_rect)
            self.window.blit(text_surface, text_rect)
            Button(self.window, pygame.Rect(self.firstRect), self.blue, "Yes")
            Button(self.window, pygame.Rect(self.secondRect), self.blue, "No")
            self.ButtonBack()
            self.Event(2)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = NumberBots(2)

    while True:
        board.setWindow()
        pygame.display.update()
