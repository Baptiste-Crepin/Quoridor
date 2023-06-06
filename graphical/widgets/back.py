import pygame


class Back():
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface

        self.darkBlue = pygame.Color(0, 0, 48)
        self.white = pygame.Color(255, 255, 255)

    def drawButton(self):
        coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                 (70, 60), (30, 60), (30, 70)]
        button = pygame.draw.polygon(self.surface, self.darkBlue, coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.surface.blit(text, buttonText)
        return button

    def Event(self, event, file, args=None) -> None:
        if self.drawButton().collidepoint(event.pos):
            if args:
                if type(args) == tuple:
                    board = file(*(args))
                else:
                    board = file(args)
            else:
                board = file()
            while True:
                board.mainLoop()
                pygame.display.update()
