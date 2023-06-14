import pygame
from graphical.widgets.back import Back


class Menu():
    def __init__(self) -> None:
        pygame.display.set_caption("Quoridor")

        self.windowWidth = 1330
        self.windowHeight = 750
        self.window = pygame.display.set_mode(
            size=(self.windowWidth, self.windowHeight))
        self.center = (self.windowWidth//2, self.windowHeight//2)

        self.clock = pygame.time.Clock()
        self.fps = 30
        self.clock.tick(self.fps)

        self.backGround = pygame.Color(23, 43, 79)
        self.font = pygame.font.Font(None, 36)

        self.white = pygame.Color(255, 255, 255)
        self.grey = pygame.Color(217, 217, 217, 35)
        self.black = pygame.Color(0, 0, 0)
        self.lighterBlue = pygame.Color(138, 201, 244)
        self.lightBlue = pygame.Color(90, 173, 255)
        self.blue = pygame.Color(138, 201, 244)
        self.darkBlue = pygame.Color(0, 0, 48)
        self.purple = pygame.Color(204, 0, 204)

        self.buttonWidth = 400
        self.buttonHeight = 120
        self.buttonSize = (self.buttonWidth, self.buttonHeight)
        self.buttonX = self.windowWidth//2-self.buttonWidth//2
        self.back = Back(self.window)

    def defaultEventHandler(self, event: pygame.event.Event) -> None:
        if event.type in [pygame.QUIT, pygame.WINDOWCLOSE]:
            raise SystemExit

    def mainLoop(self):
        self.window.fill(self.darkBlue)
        for event in pygame.event.get():
            if event.type in [pygame.QUIT, pygame.WINDOWCLOSE]:
                raise SystemExit

    @staticmethod
    def newMenu(currentBoard: object, newBoard: object) -> None:
        del currentBoard
        while True:
            newBoard.mainLoop()  # type: ignore
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    board = Menu()

    while True:
        board.mainLoop()
        pygame.display.update()
