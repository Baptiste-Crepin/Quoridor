import pygame
from pygame.locals import *
from Player import Player
from game import Game


class TablePlayer:
    def __init__(self, boardX: int, boardY: int, col: int, i: int = 0, j: int = 0) -> None:
        self.boardX = boardX
        self.boardY = boardY
        self.col = col
        self.player = Player(0)
        self.highlighted = False
        self.hover = False

        self.width = self.sizeCase()
        self.height = self.sizeCase()
        self.offset = self.offsetCase()

        self.x = 0
        self.y = 0
        self.setCoordFromIndex(i, j)

    def sizeCase(self) -> int:
        return (self.boardY // self.col)

    def offsetCase(self) -> int:
        totalMargin = 100
        return self.boardY // (self.width * self.col) + (totalMargin//self.col)

    def setCoordFromIndex(self, i: int, j: int) -> None:
        self.x = self.coord(i)
        self.y = self.coord(j)

    def coord(self, i: int) -> int:
        return i * (self.width)

    def drawCase(self, surface: pygame.Surface, color: pygame.Color) -> None:
        x = self.x + self.offset//2
        y = self.y + self.offset//2
        width = self.width - self.offset
        height = self.height - self.offset
        rectValues = (x, y, width, height)

        pygame.draw.rect(surface, color, rectValues)

    def collides(self, otherCoord: tuple[int, int]) -> bool:
        if otherCoord[1] < self.y or otherCoord[1] > self.y + self.width:
            return False
        if otherCoord[0] < self.x or otherCoord[0] > self.x + self.height:
            return False
        return True


class Barrier():
    def __init__(self, boardX: int, boardY: int, col: int, i: int = 0, j: int = 0) -> None:
        self.cellTemplate = TablePlayer(boardX, boardY, col)
        self.boardX = boardX
        self.boardY = boardY
        self.col = col
        self.x = self.coordX(i)
        self.y = self.coordY(j)
        self.height = self.setHeight()
        self.width = self.setWidth()
        self.possiblePlacement = False
        self.placed = False
        self.hover = False

    def draw(self, surface: pygame.Surface, color: pygame.Color) -> None:
        rectValues = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, color, rectValues)

    def collides(self, otherCoord: tuple[int, int]) -> bool:
        if otherCoord[1] < self.y or otherCoord[1] > self.y + self.height:
            return False
        if otherCoord[0] < self.x or otherCoord[0] > self.x + self.width:
            return False

        return True


class HorrizontalBarrier(Barrier):
    def __init__(self, boardX: int, boardY: int, col: int, i: int = 0, j: int = 0) -> None:
        super().__init__(boardX, boardY, col, i, j)

    def setWidth(self) -> int:
        return self.cellTemplate.width-self.cellTemplate.offset

    def setHeight(self) -> int:
        return self.cellTemplate.offset

    def coordX(self, i: int) -> float:
        return self.cellTemplate.coord(i) + self.cellTemplate.offset/2

    def coordY(self, j: int) -> float:
        return self.cellTemplate.width * (j+1)-self.cellTemplate.offset/2


class VerticalBarrier(Barrier):
    def __init__(self, boardX, boardY, col, i: int = 0, j: int = 0):
        super().__init__(boardX, boardY, col, i, j)

    def setWidth(self) -> int:
        return self.cellTemplate.offset

    def setHeight(self) -> int:
        return self.cellTemplate.width-self.cellTemplate.offset

    def coordX(self, i: int) -> float:
        return self.cellTemplate.height * (i+1)-self.cellTemplate.offset/2

    def coordY(self, j: int) -> float:
        return self.cellTemplate.coord(j)+self.cellTemplate.offset/2


class Intersection(Barrier):
    def __init__(self, boardX, boardY, col, i: int = 0, j: int = 0):
        super().__init__(boardX, boardY, col, i, j)
        self.grey = pygame.Color(217, 217, 217, 68)

    def setWidth(self) -> int:
        return self.cellTemplate.offset

    def setHeight(self) -> int:
        return self.cellTemplate.offset

    def coordX(self, i: int) -> float:
        return self.cellTemplate.height * (i)-self.cellTemplate.offset/2+self.cellTemplate.sizeCase()

    def coordY(self, j: int) -> float:
        return self.cellTemplate.width * (j)-self.cellTemplate.offset/2+self.cellTemplate.sizeCase()

class informationPlayer():
    def __init__(self,surface:pygame.Surface, color:pygame.Color,rect:pygame.Rect,player:Player) -> None:
        self.surface = surface
        self.color = color
        self.white=(255,255,255)
        self.purple = pygame.Color(204,0,204)
        self.rect = rect
        self.player=player
        

    def barrerCoordX(self)->int:
        x=self.rect[3]//2+self.rect[1]
        return x
    
    def barrerCoordY(self,i:int)->int:
        y=((self.rect[2])//self.player.getBarrier()*i+self.rect[0])+((self.rect[2]//self.player.getBarrier())//2-self.barrerWidth()//2)
        return y

    def barrerWidth(self)->int:
        width=20
        return width

    def barrerHeight(self)->int:
        height=self.rect[3]//2
        return height
    

    def createRectPlayer(self)->None:
        pygame.draw.rect(self.surface,self.color,self.rect,border_radius=10)
        coordPlayer=(self.rect[0]+self.rect[2]*0.05, self.rect[1]+self.rect[2]*0.05)
        pygame.draw.circle(self.surface,self.player.getColor(),coordPlayer,20)
        for i in range(self.player.getBarrier()):
            pygame.draw.rect(self.surface,self.purple,(self.barrerCoordY(i),self.barrerCoordX()
                                              ,self.barrerWidth(),self.barrerHeight()))
        

class displayInformation():
    def __init__(self,player:Player,playerlist:list[Player], surface:pygame.Surface,color:pygame.Color, rect:pygame.Rect,playerNumber:int) -> None:
        self.player = player
        self.playerList = playerlist
        self.surface = surface
        self.color=color
        self.rect=rect
        self.playerNumber = playerNumber


    def RectNeutral(self, )->None:
        pygame.draw.rect(self.surface,self.color, self.rect, border_radius=10)

    def playerCircles(self)->None:
        center=(self.rect[0]+self.rect[2]*0.05, self.rect[1]+self.rect[3]//2)
        pygame.draw.circle(self.surface,self.player.getColor(),center,20)

    def displayNeutral(self)->None:
        self.RectNeutral()
        self.playerCircles()



class Board:
    def __init__(self, Width):
        self.col = Width        

        self.windowXmax = 1330
        self.windowYmax = 750
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        
        self.clicked = False
        self.white = (255, 255, 255)
        self.grey = pygame.Color(217, 217, 217, 35)
        self.black = pygame.Color(0,0,0)
        self.darkBlue = pygame.Color(0,0,48)
        self.lightBlue = pygame.Color(90,173,255)
        self.purple = pygame.Color(204,0,204)
        self.rect = self.initializeObjectList(TablePlayer)
        self.Vbarriers = self.initializeObjectList(VerticalBarrier, 1, 0)
        self.Hbarriers = self.initializeObjectList(HorrizontalBarrier, 0, 1)
        self.intersection = self.initializeObjectList(Intersection, 1, 1)

        self.player = Player(0)

        pygame.display.set_caption("plateau")
        self.play = True

    def initializeObjectList(self, objectType: object, offsetRow: int = 0, offsetCol: int = 0) -> list[list[object]]:
        return [[objectType(self.windowXmax, self.windowYmax, self.col, i, j)
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

    def hoverBarriers(self, barrierList: list[list[Barrier]], offsetRow: int, offsetCol: int) -> None | bool:
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

    def interactObject(self, listeObject: list[object], pos: tuple[int, int]) -> None | tuple[str, int, int]:
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

    def mouseLogic(self, event: pygame.event) -> None | tuple[str, int, int] | bool:
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
            return False

    def quitWindow(self, event) -> None:
        if event.type == pygame.QUIT or event.type == 32787:
            pygame.quit()
            raise SystemExit

    def handleEvents(self) -> None | tuple[str, int, int] | bool:
        for event in pygame.event.get():
            self.quitWindow(event)
            return self.mouseLogic(event)

    def clearScreen(self) -> None:
        self.window.fill((240, 240, 240))

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

    def clearHover(self, objectList: list[list[object]]) -> None:
        for row in objectList:
            for element in row:
                element.hover = False

    def displayTable(self) -> None:
        self.window.fill(self.darkBlue)
        for i, row in enumerate(self.rect):

            for j, cell in enumerate(row):
                cell.drawCase(self.window, self.white)

                if cell.highlighted:
                    cell.drawCase(self.window, (255, 204, 255))
                if cell.hover:
                    cell.drawCase(self.window, (255, 0, 0))

                if cell.player.getNumber() != 0:
                    pygame.draw.circle(self.window,
                                       cell.player.getColor(),
                                       ((cell.x + cell.sizeCase()//2),
                                        (cell.y + cell.sizeCase()//2)),
                                       cell.sizeCase()//3-5)

    def higlightPlayer(self, player: Player) -> None:
        for i, row in enumerate(self.rect):
            for j, cell in enumerate(row):
                if cell.player == player:
                    pygame.draw.circle(self.window,
                                       (255, 255, 255),
                                       ((cell.x + cell.sizeCase()//2),
                                        (cell.y + cell.sizeCase()//2)),
                                       cell.sizeCase()//6)

    def displayBarriers(self, barrierList: list[list[object]]) -> None:
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
                    intersection.draw(self.window, (255, 0, 0))


    def displayPlayerInformation(self, currentPlayer: Player, playerList: list[Player]) -> None:
        height=190
        if len(playerList) == 4:
            height=330
        pygame.draw.rect(self.window, self.lightBlue,
                        (750, 10, 570, height), border_radius=10)

        for i, player in enumerate(playerList):
            if player == currentPlayer:
                informationPlayer(
                    self.window, self.black, (760, 20 + i * 70, 550, 100), player).createRectPlayer()

            else:
                offset = 0
                if player.getNumber() > currentPlayer.getNumber():
                    offset = 50

                displayInformation(player, playerList, self.window,
                                   self.black, (760, 20 + offset + i * 70, 550, 50), i).displayNeutral()



    def newFrame(self, currentPlayer:Player,playerList:list[Player]) -> None:
        self.clearScreen()
        self.displayTable()
        self.displayBarriers(self.Hbarriers)
        self.displayBarriers(self.Vbarriers)
        self.displayIntersection()
        self.displayPlayerInformation(currentPlayer,playerList)
        self.higlightPlayer(self.player)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    player = Player(1,4)
    board = Board(5)
    while board.play:
        board.handleEvents()
        board.newFrame(player)

    pygame.quit()
