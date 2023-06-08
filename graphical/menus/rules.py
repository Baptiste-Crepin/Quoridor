import pygame
from graphical.widgets.menu import Menu


class Rules(Menu):
    def __init__(self) -> None:
        super().__init__()

    def ButtonBack(self) -> pygame.Rect:
        coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                 (70, 60), (30, 60), (30, 70)]
        button = pygame.draw.polygon(self.window, self.darkBlue, coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)
        return button

    def Event(self) -> None:
        from Play import Play
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.ButtonBack().collidepoint(event.pos) and event.button == 1:
                    pygame.init()
                    board = Play()
                    while True:
                        board.setWindow()
                        pygame.display.update()

    def setWindow(self) -> None:
        backGround = pygame.image.load('assets/pictures/Rule.png')
        self.window.blit(backGround, (-5, -20))
        self.ButtonBack()
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Rules()

    while True:
        board.setWindow()
        pygame.display.update()
