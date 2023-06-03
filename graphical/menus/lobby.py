import pygame
from graphical.widgets.input import Input
from graphical.widgets.button import Button


class Menu:
    def __init__(self) -> None:
        self.windowWidth = 500
        self.windowYmax = 700
        self.posPlay = (50, 200)
        self.posRules = (50, 370)
        self.window = pygame.display.set_mode(
            (self.windowWidth, self.windowYmax))
        pygame.display.set_caption("Quoridor")

        self.white = pygame.Color(255, 255, 255)
        self.grey = pygame.Color(217, 217, 217, 35)
        self.black = pygame.Color(0, 0, 0)
        self.darkBlue = pygame.Color(0, 0, 48)
        self.lightBlue = pygame.Color(90, 173, 255)
        self.purple = pygame.Color(204, 0, 204)
        self.input = Input(self.window, pygame.Rect(
            140, 325, 220, 50), self.white)

    def Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
            self.input.Event(event)

    def setWindow(self):
        self.window.fill(self.darkBlue, rect=None, special_flags=0)
        font = pygame.font.SysFont(
            "Extra Bold Italic", 60, False, True)
        text = font.render(
            "chose the name of", True, self.white)
        secondtext = font.render(
            "the server", True, self.white)
        self.input.createInput()
        self.window.blit(text, (70, 230))
        self.window.blit(secondtext, (150, 270))

        Button(self.window, pygame.Rect(
            175, 400, 150, 50), self.lightBlue, "send", 40, 10)

        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Menu()

    while True:
        board.setWindow()
        pygame.display.update()
