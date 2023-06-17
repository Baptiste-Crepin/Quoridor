from typing import TypeVar

import pygame

from graphical.barriers.barrier import Barrier
from graphical.barriers.horizontalBarrier import HorizontalBarrier
from graphical.barriers.intersection import Intersection
from graphical.barriers.verticalBarrier import VerticalBarrier
from graphical.menus.tablePlayer import TablePlayer
from graphical.widgets.displayInformation import displayInformation
from graphical.widgets.informationPlayer import informationPlayer
from graphical.widgets.menu import Menu
from player import Player


class Board(Menu):
    """Class that handles the display of the board"""
    BarrierOrCell = TypeVar('BarrierOrCell', Barrier, TablePlayer)

    def __init__(self, Width: int, score: list[int] = [0, 0, 0, 0], fullScreen: bool = False):
        """Initializes the board"""
        self.col = Width
        self.score = score

        super().__init__(fullScreen)
        self.clicked = False
        self.play = True
        pygame.display.set_caption("plateau")

    def calculateElements(self):
        self.rect = self.initializeObjectList(TablePlayer)
        self.verticalBarriers = self.initializeObjectList(
            VerticalBarrier, 1, 0)
        self.horizontalBarriers = self.initializeObjectList(
            HorizontalBarrier, 0, 1)
        self.intersection = self.initializeObjectList(Intersection, 1, 1)

    def initializeObjectList(self, objectType: type[BarrierOrCell], offsetRow: int = 0, offsetCol: int = 0) -> list[
            list[BarrierOrCell]]:
        return [[objectType(self.windowWidth, self.windowHeight, self.col, i, j)
                 for j in range(self.col - offsetCol)]
                for i in range(self.col - offsetRow)]

    def hoverCells(self, cellsList: list[list[TablePlayer]]) -> None | bool:
        for row in cellsList:
            for cell in row:
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
                    barrierList[i + offsetRow][j + offsetCol].hover = True
                    return True
                if not barrier.possiblePlacement:
                    continue

                self.clearHover(barrierList)
        return False

    def interactObject(self, listObject: list[list[BarrierOrCell]], pos: tuple[int, int]) -> None | tuple[str, int, int]:
        for i, row in enumerate(listObject):
            for j, element in enumerate(row):
                if element.collides(pos):
                    return (type(element).__name__, j, i)

    def hoverLogic(self) -> None:
        self.clearHover(self.rect)
        if self.hoverBarriers(self.horizontalBarriers, 1, 0):
            return
        if self.hoverBarriers(self.verticalBarriers, 0, 1):
            return
        self.hoverCells(self.rect)
        return

    def mouseLogic(self) -> None | tuple[str, int, int]:
        self.hoverLogic()

        if pygame.mouse.get_pressed()[0] and not self.clicked:
            self.clicked = True
            pos = pygame.mouse.get_pos()

            for array in [self.verticalBarriers, self.horizontalBarriers, self.rect]:
                if clickedElement := self.interactObject(array, pos):
                    return clickedElement

        if not pygame.mouse.get_pressed()[0] and self.clicked:
            self.clicked = False

    def quitWindow(self, event: pygame.event.Event) -> None:
        self.defaultEventHandler(event)

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
        self.clearPossiblePlacement(self.verticalBarriers)
        self.clearPossiblePlacement(self.horizontalBarriers)

    def clearHover(self, objectList: list[list[BarrierOrCell]]) -> None:
        for row in objectList:
            for element in row:
                element.hover = False

    def displayTable(self) -> None:
        for row in self.rect:
            for cell in row:
                cell.drawCase(self.window, self.white)

    def displayHighlightedCells(self):
        for row in self.rect:
            for cell in row:
                if cell.highlighted:
                    cell.drawCase(self.window, pygame.Color(255, 204, 255))
                if cell.hover:
                    cell.drawCase(self.window, pygame.Color(255, 0, 0))

    def displayPlayers(self) -> None:
        for row in self.rect:
            for cell in row:
                if cell.player.getNumber() != 0:
                    pygame.draw.circle(self.window,
                                       cell.player.getColor(),
                                       ((cell.x + cell.sizeCase() // 2),
                                        (cell.y + cell.sizeCase() // 2)),
                                       cell.sizeCase() // 3 - 5)

    def highlightPlayer(self, player: Player) -> None:
        for row in self.rect:
            for cell in row:
                if cell.player.getNumber() == player.getNumber():
                    pygame.draw.circle(self.window,
                                       (255, 255, 255),
                                       ((cell.x + cell.sizeCase() // 2),
                                        (cell.y + cell.sizeCase() // 2)),
                                       cell.sizeCase() // 6)

    def displayBarriers(self, barrierList: list[list[Barrier]]) -> None:
        for row in barrierList:
            for barrier in row:
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
                if ((self.verticalBarriers[i][j].placed and
                     self.verticalBarriers[i][j+1].placed) or
                    (self.horizontalBarriers[i][j].placed and
                     self.horizontalBarriers[i+1][j].placed)):

                    VnbBarriers = 0
                    if self.verticalBarriers[i][j].placed:
                        while j-VnbBarriers >= 0 and self.verticalBarriers[i][j-VnbBarriers].placed:
                            VnbBarriers += 1

                    HnbBarriers = 0
                    if self.horizontalBarriers[i][j].placed:
                        while i-HnbBarriers >= 0 and self.horizontalBarriers[i-HnbBarriers][j].placed:
                            HnbBarriers += 1

                    if VnbBarriers % 2 == 0 and HnbBarriers % 2 == 0:
                        continue

                    if i < len(self.verticalBarriers)-1 and i < len(self.horizontalBarriers)-1:
                        if self.verticalBarriers[i+1][j].placed:
                            self.intersection[i +
                                              1][j].draw(self.window, self.grey)
                    if j < len(self.verticalBarriers)-1 and j < len(self.horizontalBarriers)-1:
                        if self.horizontalBarriers[i][j+1].placed:
                            self.intersection[i][j +
                                                 1].draw(self.window, self.grey)

                    intersection.draw(self.window, self.purple)
                    continue

                intersection.draw(self.window, self.grey)
                if intersection.hover:
                    intersection.draw(self.window, pygame.Color(255, 0, 0))

    def displayPlayerGoal(self, playerList: list[Player]) -> None:
        for player in playerList:
            for i in range(len(self.rect)-2):
                goalLineMap = {1: (i+1, len(self.rect)-1), 2: (i+1, 0),
                               3: (len(self.rect)-1, i+1), 4: (0, i+1)}
                start = goalLineMap[player.getNumber()]
                self.rect[start[0]][start[1]].drawCase(
                    self.window, pygame.Color(player.getColor()))

            goalCornerMap = {1: ((0, len(self.rect)-1), (len(self.rect)-1, len(self.rect)-1)),
                             2: ((0, 0), (len(self.rect)-1, 0)),
                             3: ((len(self.rect)-1, len(self.rect)-1, 0), (len(self.rect)-1, 0)),
                             4: ((0, 0), (0, len(self.rect)-1))}
            for j in range(2):
                start = goalCornerMap[player.getNumber()]

                x = self.rect[start[j][0]][start[j][1]].x + \
                    self.rect[start[j][0]][start[j][1]].offsetCase()//2
                y = self.rect[start[j][0]][start[j][1]].y + \
                    self.rect[start[j][0]][start[j][1]].offsetCase()//2
                width = self.rect[start[j][0]][start[j][1]].width - + \
                    self.rect[start[j][0]][start[j][1]].offsetCase()

                sizeArrow = width
                upLeft = (x, y)
                upRight = (x + sizeArrow, y)
                downLeft = (x, y + sizeArrow)
                downRight = (x + sizeArrow, y + sizeArrow)

                dir_mapping = {
                    1: {
                        0: [downLeft, upRight, downRight],
                        1: [downLeft, upLeft, downRight]},
                    2: {
                        0: [upLeft, upRight, downRight],
                        1: [downLeft, upLeft, upRight]},
                    3: {
                        0: [upLeft, upRight, downRight],
                        1: [downLeft, downRight, upRight]},
                    4: {
                        0: [upLeft, downLeft, downRight],
                        1: [downLeft, upLeft, upRight]
                    }
                }

                Triangle_point = dir_mapping[player.getNumber()][j]

                pygame.draw.polygon(
                    self.window, player.getColor(), Triangle_point)

    def displayPlayerInformation(self, currentPlayer: Player, playerList: list[Player]) -> None:
        height = 330 if len(playerList) == 4 else 190
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
                                   self.black, pygame.Rect(
                                       760, 20 + offset + i * 70, 550, 50), i,
                                   self.score).displayNeutral()

    def newFrame(self, currentPlayer: Player, playerList: list[Player]) -> None:
        self.clearScreen()
        self.displayTable()
        self.displayPlayerGoal(playerList)
        self.displayHighlightedCells()
        self.displayPlayers()
        self.displayBarriers(self.horizontalBarriers)
        self.displayBarriers(self.verticalBarriers)
        self.displayIntersection()
        self.displayPlayerInformation(currentPlayer, playerList)
        self.highlightPlayer(currentPlayer)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    player1 = Player(1, 4)
    player2 = Player(2, 4)
    board = Board(5)
    while board.play:
        board.handleEvents()
        board.newFrame(player1, [player1, player2])
