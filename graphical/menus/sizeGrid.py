import pygame
from graphical.widgets.button import Button


class SizeGrid:
    def __init__(self, nbPlayer: int, nbBot: int, method: int) -> None:
        self.nbPlayers = nbPlayer
        self.method = method
        self.nbBot = nbBot
        self.windowXmax = 500
        self.windowYmax = 700
        self.pos1 = (50, 100)
        self.pos2 = (50, 240)
        self.pos3 = (50, 380)
        self.pos4 = (50, 520)
        self.sizeButton = (400, 100)
        self.window = pygame.display.set_mode(
            size=(self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.blue = pygame.Color(138, 201, 244)
        self.white = pygame.Color(255, 255, 255)
        self.black = pygame.Color(0, 0, 0)
        self.darkerBlue = pygame.Color(0, 0, 48)
        self.font = pygame.font.Font(None, 36)

    def ButtonBack(self) -> pygame.Rect:
        coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                 (70, 60), (30, 60), (30, 70)]
        button = pygame.draw.polygon(self.window, self.darkerBlue, coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)
        return button

    def Event(self):
        from barrier import selectBarrier
        from graphical.menus.choicePlayer import NumberPlayer
        from graphical.menus.choiseBot import NumberBots

        sizeFromPos = {self.pos1: 5, self.pos3: 9,
                       self.pos2: 7, self.pos4: 11}

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
            elif not (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                return

            for pos in sizeFromPos.keys():
                if pygame.Rect(pos, self.sizeButton).collidepoint(event.pos):
                    pygame.init()
                    board = selectBarrier(
                        self.nbPlayers, self.nbBot, sizeFromPos[pos], self.method)
                    while True:
                        board.setWindow()
                        pygame.display.update()

            if self.ButtonBack().collidepoint(event.pos) and event.button == 1:
                pygame.init()
                if self.method == 1:
                    board = NumberPlayer()
                else:
                    board = NumberBots(self.nbPlayers)
                while True:
                    board.setWindow()
                    pygame.display.update()

    def setWindow(self):
        backGround = pygame.image.load('pictures/backGroundMenu3.jpg')
        self.window.blit(backGround, (-80, -300))

        text_surface = self.font.render(
            "Choise the size of the grid", True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 50))

        contour_surface = self.font.render(
            "Choise the size of the grid", True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(
            center=(self.windowXmax // 2, 50))
        contour_rect.move_ip(2, 2)

        self.window.blit(contour_surface, contour_rect)
        self.window.blit(text_surface, text_rect)

        Button(self.window, pygame.Rect(
            self.pos1, self.sizeButton), self.blue, "5X5")
        Button(self.window, pygame.Rect(
            self.pos2, self.sizeButton), self.blue, "7X7")
        Button(self.window, pygame.Rect(
            self.pos3, self.sizeButton), self.blue, "9X9")
        Button(self.window, pygame.Rect(
            self.pos4, self.sizeButton), self.blue, "11X11")

        self.ButtonBack()
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = SizeGrid(2, 0, 1)

    while True:
        board.setWindow()
        pygame.display.update()
