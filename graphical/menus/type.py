import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu


class Menutype(Menu):
    def __init__(self):
        super().__init__()

        self.posSolo = (self.buttonX, 200)
        self.posMulti = (self.buttonX, 370)

        self.soloButton = pygame.Rect(
            self.buttonX, 200, self.buttonWidth, self.buttonHeight)
        self.multiButton = pygame.Rect(
            self.buttonX, 370, self.buttonWidth, self.buttonHeight)

    def ButtonBack(self) -> pygame.Rect:
        coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                 (70, 60), (30, 60), (30, 70)]
        button = pygame.draw.polygon(self.window, self.darkBlue, coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)
        return button

    def setWindow(self):
        self.window.fill(self.backGround)
        Button(self.window, self.soloButton, self.blue, "Solo")
        Button(self.window, self.multiButton, self.blue, "Muti")
        self.ButtonBack()
        self.Event()

    def Event(self):
        from graphical.menus.choicePlayer import NumberPlayer

        from Play import Play
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posSolo, self.buttonSize).collidepoint(event.pos):

                    # pygame.init()
                    board = NumberPlayer()
                    while True:
                        board.setWindow()
                        pygame.display.update()

                elif pygame.Rect(self.posMulti, self.buttonSize).collidepoint(event.pos):
                    raise SystemExit
                elif self.ButtonBack().collidepoint(event.pos) and event.button == 1:
                    # pygame.init()
                    board = Play()
                    while True:
                        board.setWindow()
                        pygame.display.update()

            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Menutype()

    while True:
        board.setWindow()
        pygame.display.update()
