
import pygame
from typing import TypeVar

from player import Player
from graphical.barriers.barrier import Barrier
from graphical.barriers.horizontalBarrier import HorrizontalBarrier
from graphical.widgets.informationPlayer import informationPlayer
from graphical.widgets.displayInformation import displayInformation
from graphical.menus.tablePlayer import TablePlayer
from graphical.barriers.verticalBarrier import VerticalBarrier
from graphical.barriers.intersection import Intersection


class Board:
    BarrierOrCell = TypeVar('BarrierOrCell', Barrier, TablePlayer)

    def __init__(self, Width):
        self.col = Width

        self.windowWidth = 1330
        self.windowHeight = 750
        self.window = pygame.display.set_mode(
            (self.windowWidth, self.windowHeight))

        self.clicked = False
        self.white = pygame.Color(255, 255, 255)
        self.grey = pygame.Color(217, 217, 217, 35)
        self.black = pygame.Color(0, 0, 0)
        self.darkBlue = pygame.Color(0, 0, 48)
        self.lightBlue = pygame.Color(90, 173, 255)
        self.purple = pygame.Color(204, 0, 204)
        self.rect = self.initializeObjectList(TablePlayer)
        self.Vbarriers = self.initializeObjectList(VerticalBarrier, 1, 0)
        self.Hbarriers = self.initializeObjectList(HorrizontalBarrier, 0, 1)
        self.intersection = self.initializeObjectList(Intersection, 1, 1)

        self.player = Player(0)

        pygame.display.set_caption("plateau")
        self.play = True

    def initializeObjectList(self, objectType: type[BarrierOrCell], offsetRow: int = 0, offsetCol: int = 0) -> list[list[BarrierOrCell]]:
        return [[objectType(self.windowWidth, self.windowHeight, self.col, i, j)
                for j in range(self.col - offsetCol)]
                for i in range(self.col - offsetRow)]

    def hoverCells(self, cellsList: list[list[TablePlayer]]) -> None | bool:
        for i, row in enumerate(cellsList):
            for j, cell in enumerate(row):
                if not cell.highlighted:
                    continue
                if cell.collides(pygame.mouse.get_pos()):
                    cell.hover = True
                    return True
                self.clearHover(self.rect)

    def hoverBarriers(self, barrierList: list[list[Barrier]], offsetRow: int, offsetCol: int) -> bool:
        for i, row in enumerate(barrierList):
            for j, barrier in enumerate(row):
                if barrier.collides(pygame.mouse.get_pos()):
                    if not barrier.possiblePlacement:
                        continue
                    barrier.hover = True
                    barrierList[i+offsetRow][j+offsetCol].hover = True
                    return True
                if not barrier.possiblePlacement:
                    continue

                self.clearHover(barrierList)
        return False

    def interactObject(self, listeObject: list[list[Barrier | TablePlayer]], pos: tuple[int, int]) -> None | tuple[str, int, int]:
        for i, row in enumerate(listeObject):
            for j, element in enumerate(row):
                colli = element.collides(pos)
                if colli:
                    return (type(element).__name__, j, i)

    def hoverLogic(self) -> None:
        self.clearHover(self.rect)
        if self.hoverBarriers(self.Hbarriers, 1, 0):
            return
        if self.hoverBarriers(self.Vbarriers, 0, 1):
            return
        self.hoverCells(self.rect)
        return

    def mouseLogic(self) -> None | tuple[str, int, int]:
        self.hoverLogic()

        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            pos = pygame.mouse.get_pos()

            for array in [self.Vbarriers, self.Hbarriers, self.rect]:
                clickedElement = self.interactObject(array, pos)
                if clickedElement:
                    return clickedElement

        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
            self.clicked = False

    def quitWindow(self, event) -> None:
        if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
            raise SystemExit

    def handleEvents(self) -> None | tuple[str, int, int]:
        for event in pygame.event.get():
            self.quitWindow(event)
            return self.mouseLogic()

    def clearScreen(self) -> None:
        self.window.fill(self.darkBlue)

    def clearHighlight(self, objectList: list[list[TablePlayer]]) -> None:
        for row in objectList:
            for element in row:
                element.highlighted = False

    def clearPossiblePlacement(self, barrierList: list[list[Barrier]]) -> None:
        for row in barrierList:
            for element in row:
                element.possiblePlacement = False

    def clearAllHighlight(self) -> None:
        self.clearHighlight(self.rect)
        self.clearPossiblePlacement(self.Vbarriers)
        self.clearPossiblePlacement(self.Hbarriers)

    def clearHover(self, objectList: list[list[BarrierOrCell]]) -> None:
        for row in objectList:
            for element in row:
                element.hover = False

    def displayTable(self) -> None:
        # self.window.fill((33, 73, 109))
        for i, row in enumerate(self.rect):

            for j, cell in enumerate(row):
                cell.drawCase(self.window, self.white)

                if cell.highlighted:
                    cell.drawCase(self.window, pygame.Color(255, 204, 255))
                if cell.hover:
                    cell.drawCase(self.window, pygame.Color(255, 0, 0))

                if cell.player.getNumber() != 0:
                    pygame.draw.circle(self.window,
                                       cell.player.getColor(),
                                       ((cell.x + cell.sizeCase()//2),
                                        (cell.y + cell.sizeCase()//2)),
                                       cell.sizeCase()//3-5)

    def higlightPlayer(self, player: Player) -> None:
        for i, row in enumerate(self.rect):
            for j, cell in enumerate(row):
                if cell.player.getNumber() == player.getNumber():
                    pygame.draw.circle(self.window,
                                       (255, 255, 255),
                                       ((cell.x + cell.sizeCase()//2),
                                        (cell.y + cell.sizeCase()//2)),
                                       cell.sizeCase()//6)

    def displayBarriers(self, barrierList: list[list[Barrier]]) -> None:
        for i, row in enumerate(barrierList):
            for j, barrier in enumerate(row):
                if barrier.placed:
                    barrier.draw(self.window, self.purple)

                    continue

                # TODO change the color
                barrier.draw(self.window, self.darkBlue)
                if barrier.hover:
                    barrier.draw(self.window, self.lightBlue)

    def displayIntersection(self) -> None:
        for i, row in enumerate(self.intersection):
            for j, intersection in enumerate(row):
                if ((self.Vbarriers[i][j].placed and
                     self.Vbarriers[i][j+1].placed) or
                    (self.Hbarriers[i][j].placed and
                     self.Hbarriers[i+1][j].placed)):

                    VnbBarriers = 0
                    if self.Vbarriers[i][j].placed:
                        while j-VnbBarriers >= 0 and self.Vbarriers[i][j-VnbBarriers].placed:
                            VnbBarriers += 1

                    HnbBarriers = 0
                    if self.Hbarriers[i][j].placed:
                        while i-HnbBarriers >= 0 and self.Hbarriers[i-HnbBarriers][j].placed:
                            HnbBarriers += 1

                    if VnbBarriers % 2 == 0 and HnbBarriers % 2 == 0:
                        continue

                    if i < len(self.Vbarriers)-1 and i < len(self.Hbarriers)-1:
                        if self.Vbarriers[i+1][j].placed:
                            self.intersection[i +
                                              1][j].draw(self.window, self.grey)
                    if j < len(self.Vbarriers)-1 and j < len(self.Hbarriers)-1:
                        if self.Hbarriers[i][j+1].placed:
                            self.intersection[i][j +
                                                 1].draw(self.window, self.grey)

                    intersection.draw(self.window, self.purple)
                    continue

                intersection.draw(self.window, self.grey)
                if intersection.hover:
                    intersection.draw(self.window, pygame.Color(255, 0, 0))

    def displayPlayerInformation(self, currentPlayer: Player, playerList: list[Player]) -> None:
        height = 190
        if len(playerList) == 4:
            height = 330
        pygame.draw.rect(self.window, self.lightBlue,
                         (750, 10, 570, height), border_radius=10)

        for i, player in enumerate(playerList):
            if player == currentPlayer:
                informationPlayer(
                    self.window, self.black, pygame.Rect(760, 20 + i * 70, 550, 100), player).createRectPlayer()

            else:
                offset = 0
                if player.getNumber() > currentPlayer.getNumber():
                    offset = 50

                displayInformation(player, playerList, self.window,
                                   self.black, pygame.Rect(760, 20 + offset + i * 70, 550, 50), i).displayNeutral()

    def newFrame(self, currentPlayer: Player, playerList: list[Player]) -> None:
        self.clearScreen()
        self.displayTable()
        self.displayBarriers(self.Hbarriers)
        self.displayBarriers(self.Vbarriers)
        self.displayIntersection()
        self.displayPlayerInformation(currentPlayer, playerList)
        self.higlightPlayer(currentPlayer)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    player1 = Player(1, 4)
    player2 = Player(2, 4)
    board = Board(5)
    while board.play:
        board.handleEvents()
        board.newFrame(player1, [player1, player2])
