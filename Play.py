import pygame
from graphical.widgets.button import Button


class Menu:
    def __init__(self) -> None:
        self.windowXmax = 500
        self.windowYmax = 700
        self.posPlay = (50, 200)
        self.posRules = (50, 370)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.blue = pygame.Color(138, 201, 244)
        self.white = pygame.Color(255, 255, 255)
        self.playButton = pygame.Rect(50, 200, 400, 120)
        self.rulesButton = pygame.Rect(50, 370, 400, 120)

    def Event(self) -> None:
        from graphical.menus.rules import Rules
        from graphical.menus.type import Menutype
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posPlay, (400, 120)).collidepoint(event.pos):
                    pygame.init()
                    board = Menutype()
                    while True:
                        board.setWindow()
                        pygame.display.update()

                elif pygame.Rect(self.posRules, (400, 120)).collidepoint(event.pos):
                    pygame.init()
                    board = Rules()
                    while True:
                        board.setWindow()
                        pygame.display.update()

        pygame.display.flip()

    def setWindow(self) -> None:
        backGround = pygame.image.load('./pictures/backGroundMenu3.jpg')
        self.window.blit(backGround, (-80, -300))
        Button(self.window, self.playButton, self.blue, "PLAY")
        Button(self.window, self.rulesButton, self.blue, "RULES")
        self.Event()


if __name__ == "__main__":
    pygame.init()
    board = Menu()

    while True:
        board.setWindow()
        pygame.display.update()
