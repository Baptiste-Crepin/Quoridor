import pygame
from graphical.widgets.menu import Menu


class Rules(Menu):
    def __init__(self, fullScreen: bool = False) -> None:
        super().__init__(fullScreen)

    def calculateElements(self) -> None:
        self.imagePos = 0

    def coordYRules(self) -> int:
        return 10+self.imagePos

    def coordYPictureRules(self) -> int:
        return 918+self.imagePos

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
        from main import Play
        for event in pygame.event.get():
            self.defaultEventHandler(event)
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0 and self.imagePos > -1500:
                    self.imagePos -= 50
                elif event.y > 0 and self.imagePos < 0:
                    self.imagePos += 50
            elif (event.type == pygame.MOUSEBUTTONDOWN and
                  event.button == 1 and
                  self.ButtonBack().collidepoint(event.pos)):
                board = Play(self.fullScreen)
                while True:
                    board.mainLoop()
                    pygame.display.update()

    def mainLoop(self) -> None:
        self.window.fill(self.backGround)
        rules = pygame.image.load("./assets/pictures/rules.png")
        picture = pygame.image.load("./assets/pictures/rulesPicture.jpg")
        self.window.blit(rules, (265, self.coordYRules()))
        self.window.blit(picture, (265, self.coordYPictureRules()))
        self.ButtonBack()
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Rules()

    while True:
        board.mainLoop()
        pygame.display.update()
