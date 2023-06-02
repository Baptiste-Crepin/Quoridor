import pygame
from button import Button


class Menutype:
    def __init__(self):
        self.windowXmax = 500
        self.windowYmax = 700
        self.posSolo = (50, 200)
        self.posMulti = (50, 370)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.blue = pygame.Color(138, 201, 244)
        self.white = pygame.Color(255, 255, 255)
        self.darkerBlue = pygame.Color(0, 0, 48)
        self.soloButton = pygame.Rect(50, 200, 400, 120)
        self.multiButton = pygame.Rect(50, 370, 400, 120)

    def createButtonSolo(self):
        button = pygame.draw.rect(
            self.window, self.blue, (50, 200, 400, 120), width=0, border_radius=20)
        font = pygame.font.SysFont("Extra Bold Italic", 60, False, True)
        text = font.render("SOLO", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def createButtonMulti(self):
        button = pygame.draw.rect(
            self.window, self.blue, (50, 370, 400, 120), width=0, border_radius=20)
        font = pygame.font.SysFont("Extra Bold Italic", 60, False, True)
        text = font.render("MULTI", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def ButtonBack(self) -> pygame.Rect:
        coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                 (70, 60), (30, 60), (30, 70)]
        button = pygame.draw.polygon(self.window, self.darkerBlue, coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)
        return button

    def setWindow(self):
        backGround = pygame.image.load('pictures/backGroundMenu3.jpg')
        self.window.blit(backGround, (-80, -300))
        Button(self.window, self.soloButton, self.blue, "Solo")
        Button(self.window, self.multiButton, self.blue, "Muti")
        self.ButtonBack()
        self.Event()

    def Event(self):
        from choicePlayer import NumberPlayer
        from Play import Menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posSolo, (400, 120)).collidepoint(event.pos):

                    pygame.init()
                    board = NumberPlayer()
                    while True:
                        board.setWindow()
                        pygame.display.update()

                elif pygame.Rect(self.posMulti, (400, 120)).collidepoint(event.pos):
                    pygame.quit()
                elif self.ButtonBack().collidepoint(event.pos) and event.button == 1:
                    pygame.init()
                    board = Menu()
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

    pygame.quit()
