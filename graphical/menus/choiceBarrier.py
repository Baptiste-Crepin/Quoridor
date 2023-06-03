import pygame
import time
from main import GraphicalGame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu


class selectBarrier(Menu):

    def __init__(self, NumberPlayers: int, NumberBots: int, GridSize: int, method: int) -> None:
        super().__init__()
        self.NumberPlayers = NumberPlayers
        self.NumberBots = NumberBots
        self.GridSize = GridSize
        self.method = method

        self.barrier = 1
        self.circleWidth = 100

        self.doneButton = pygame.Rect(
            self.buttonX, 560, self.buttonWidth, self.buttonHeight)

        self.upTriangleColor = self.white
        self.downTriangleColor = self.lighterBlue

    def drawCircleOutline(self) -> object:
        return pygame.draw.circle(self.window, self.black, self.center, self.circleWidth + 15, width=0)

    def drawSecondCircle(self) -> None:
        circle = pygame.draw.circle(
            self.window, self.lighterBlue, self.center, self.circleWidth, width=0)
        font = pygame.font.SysFont("Roboto", 110, False, True)
        text = font.render(str(self.barrier), True, self.white)
        buttonText = text.get_rect(center=circle.center)
        self.window.blit(text, buttonText)

    def drawDownTriangle(self) -> pygame.Rect:
        offset = 55
        sizeArrow = 30
        leftPoint = (self.center[0] - sizeArrow, self.center[1] + offset - 5)
        rightPoint = (self.center[0] + sizeArrow, self.center[1] + offset - 5)
        downPoint = (self.center[0], self.center[1] + sizeArrow + offset + 5)
        Triangle_point = [leftPoint, rightPoint, downPoint]
        return pygame.draw.polygon(self.window, self.downTriangleColor, Triangle_point)

    def drawUpTriangle(self) -> pygame.Rect:
        offset = -55
        sizeArrow = 30
        point1 = (self.center[0] + sizeArrow, self.center[1] + offset + 5)
        point2 = (self.center[0] - sizeArrow, self.center[1] + offset + 5)
        point3 = (self.center[0], self.center[1] - sizeArrow + offset - 5)
        Triangle_point = [point1, point2, point3]
        return pygame.draw.polygon(self.window, self.upTriangleColor, Triangle_point)

    def ButtonBack(self) -> pygame.Rect:
        coord = [(5, 40), (30, 10), (30, 20), (70, 20),
                 (70, 60), (30, 60), (30, 70)]
        button = pygame.draw.polygon(self.window, self.black, coord)
        font = pygame.font.SysFont("Extra Bold Italic", 20, False, True)
        text = font.render("Back", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)
        return button

    def Event(self) -> None:
        from graphical.menus.sizeGrid import SizeGrid

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.drawDownTriangle().collidepoint(event.pos):
                    if self.barrier > 1:
                        self.barrier -= 1
                        self.upTriangleColor = self.white
                    if self.barrier < 2:
                        self.downTriangleColor = self.lighterBlue
                elif self.drawUpTriangle().collidepoint(event.pos):
                    maxBarrierMap = {5: 2, 7: 4, 9: 7, 11: 10}
                    if self.barrier < maxBarrierMap[self.GridSize]:
                        self.barrier += 1
                        self.downTriangleColor = self.white
                    if self.barrier == maxBarrierMap[self.GridSize]:
                        self.upTriangleColor = self.lighterBlue
                elif self.doneButton.collidepoint(event.pos):
                    pygame.init()
                    board = GraphicalGame(
                        self.GridSize, self.NumberPlayers, self.barrier, self.NumberBots)
                    time.sleep(0.2)
                    while True:
                        board.mainLoop()
                        pygame.display.update()

                elif self.ButtonBack().collidepoint(event.pos) and event.button == 1:
                    pygame.init()
                    board = SizeGrid(self.NumberPlayers,
                                     self.NumberBots, self.method)
                    while True:
                        board.setWindow()
                        pygame.display.update()

    def setWindow(self) -> None:
        self.window.fill(self.backGround)

        text_surface = self.font.render(
            "Choise the number of barrier", True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowWidth // 2, 50))

        contour_surface = self.font.render(
            "Choise the number of barrier", True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(
            center=(self.windowWidth // 2, 50))
        contour_rect.move_ip(2, 2)
        self.window.blit(contour_surface, contour_rect)
        self.window.blit(text_surface, text_rect)

        self.drawCircleOutline()
        self.drawSecondCircle()
        self.drawDownTriangle()
        self.drawUpTriangle()

        Button(self.window, self.doneButton, self.lighterBlue, "Done")
        self.Event()
        self.ButtonBack()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = selectBarrier(1, 1, 11, 0)

    while True:
        board.setWindow()
        pygame.display.update()
