import pygame
from pygame.locals import *
from Player import Player


class TablePlayer:
    def __init__(self, boardX, boardY, Col, Row):
        self.boardX = boardX
        self.boardY = boardY
        self.col = Col
        self.row = Row
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.brown= (59,39,28)
        self.player = Player(0)
        self.highlighted = False
        self.hover = False

        self.x = 0
        self.y = 0
        self.sizeX = 0
        self.sizeY = 0

    def numberCase(self):
        n = self.col
        return n

    def sizeCaseX(self):
        self.sizeX = (((self.boardY//2)-10)//self.numberCase())
        return self.sizeX

    def sizeCaseY(self):
        self.sizeY = (((self.boardY//2)-10)//self.numberCase())
        return self.sizeY

    def coordX(self, i):
        self.x = (self.boardX*0.10)*i
        return self.x

    def coordY(self, j):
        self.y = (self.boardY*0.10)*j
        return self.y

    def drawCase(self, surface, i, j, color):
        x = self.coordX(i)
        y = self.coordY(j)
        width = self.sizeCaseX()
        height = self.sizeCaseY()
        casePlayer = pygame.draw.rect(
            surface, color, (x, y, width, height))
        return casePlayer

    def collides(self, otherCoord):
        if otherCoord[0] < self.x or otherCoord[0] > self.x + self.sizeX:
            return False
        if otherCoord[1] < self.y or otherCoord[1] > self.y + self.sizeY:
            return False

        return True


class barrer():
    def __init__(self,boardX,boardY,col,row):
        self.boardX = boardX
        self.boardY = boardY
        self.col = col
        self.row = row
        self.placed = 0
        self.x = 0
        self.y = 0
        self.height = 0
        self.width = 0
        self.possiblePlacement = False
        self.hover = False

    def numberCase(self):
        n = self.col
        return n

    def draw(self, surface, i, j, color):
        x = self.coordX(i)
        y = self.coordY(j)
        width = self.sizeX()
        height = self.sizeY()
        barrier = pygame.draw.rect(
            surface, color, (x, y, width, height)) 
        
        return barrier

    def collides(self, otherCoord):
        if otherCoord[0] < self.x or otherCoord[0] > self.x + self.height:
            return False
        if otherCoord[1] < self.y or otherCoord[1] > self.y + self.width:
            return False

        return True

class VerticalBarrier(barrer):
    def __init__(self, boardX, boardY,col,row):
        super().__init__(boardX,boardY,col,row)
    def sizeX(self):
        sizeX = 10
        self.height = sizeX
        return sizeX

    def sizeY(self):
        self.width = (((self.boardY//2)-10)//self.numberCase())
        return self.width

    def coordX(self, i):
        x = ((self.boardX-900)//self.numberCase())*i+(self.boardX*0.33)+ \
            (((self.boardX-900)//self.numberCase())-10)
        self.x = x
        return x

    def coordY(self, j):
        y =  (((self.boardY-330)//self.numberCase()))*j+(self.boardY*0.25)
        self.y = y
        return y




class HorrizontalBarrier(barrer):
    def __init__(self, boardX, boardY,col,row):
        super().__init__(boardX,boardY,col,row)

    def sizeX(self):
        self.height =(((self.boardY//2)-10)//self.numberCase())
        return self.height

    def sizeY(self):
        self.width  = 10
        return  self.width

    def coordX(self, i):
        x = (((self.boardX-900)//self.numberCase()))*i+(self.boardX*0.33)
        self.x = x
        return x

    def coordY(self, j):
        y = (((self.boardY-330)//self.numberCase()))*j+(self.boardY*0.25)+ \
        (((self.boardY-330)//self.numberCase())-10)
        self.y = y
        return y




class Intersection(barrer):
    def __init__(self, boardX, boardY, col, row):
        super().__init__(boardX, boardY, col, row)
        self.grey= pygame.Color(217,217,217,68)


    def coordX(self, i):
        x = ((self.boardX-900)//self.numberCase())*i+(self.boardX*0.33)+ \
            (((self.boardX-900)//self.numberCase())-10)
        self.x = x
        return x

    def coordY(self, j):
        y = (((self.boardY-330)//self.numberCase()))*j+(self.boardY*0.25)+ \
        (((self.boardY-330)//self.numberCase())-10)
        self.y = y
        return y

    def sizeX(self):
        self.height = 10
        return self.height

    def sizeY(self):
        self.width= 10
        return self.width




class Board:
    def __init__(self, Width):
        self.col = Width
        self.row = Width
        self.windowXmax = 1330
        self.windowYmax = 748
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        self.clicked = False
        self.grey= pygame.Color(217, 217, 217,35)
        self.rect = self.initializeGrid()
        self.Vbarriers = self.initializeVBarriers()
        self.Hbarriers = self.initializeHBarriers()
        self.intersection = self.initializeIntersection()

        self.player = Player(0)

        pygame.display.set_caption("plateau")
        self.play = True
        

    def initializeGrid(self):
        rectArray = []
        for i in range(self.col):
            row = []
            for j in range(self.row):
                cell = TablePlayer(self.windowXmax,
                                   self.windowYmax,
                                   self.col,
                                   self.row)
                row.append(cell)
            rectArray.append(row)
        return rectArray

    def initializeVBarriers(self):
        rectArray = []
        for i in range(self.col-1):
            row = []
            for j in range(self.row):
                barrier = VerticalBarrier(
                    self.windowXmax,
                    self.windowYmax,
                    self.col,
                    self.row)
                row.append(barrier)
            rectArray.append(row)
        return rectArray

    def initializeHBarriers(self):
        rectArray = []
        for i in range(self.col):
            row = []
            for j in range(self.row-1):
                barrier = HorrizontalBarrier(self.windowXmax,
                                             self.windowYmax,
                                             self.col,
                                             self.row)
                row.append(barrier)
            rectArray.append(row)
        return rectArray

    def initializeIntersection(self):
        rectArray = []
        for i in range(self.col-1):
            row = []
            for j in range(self.row-1):
                barrier = Intersection(self.windowXmax,
                                       self.windowYmax,
                                       self.col,
                                       self.row)
                row.append(barrier)
            rectArray.append(row)
        return rectArray

    def hoverCells(self):
        for i, row in enumerate(self.rect):
            for j, cell in enumerate(row):
                if not cell.highlighted:
                    continue
                if cell.collides(pygame.mouse.get_pos()):
                    cell.hover = True
                    return
                self.clearHover(self.rect)

    def hoverVbarriers(self):
        for i, row in enumerate(self.Vbarriers):
            for j, barrier in enumerate(row):
                if barrier.collides(pygame.mouse.get_pos()):
                    if not barrier.possiblePlacement:
                        continue
                    barrier.hover = True
                    self.Vbarriers[i][j+1].hover = True
                    return
                if not barrier.possiblePlacement:
                    continue
                self.clearHover(self.Vbarriers)

    def hoverHbarriers(self):
        for i, row in enumerate(self.Hbarriers):
            for j, barrier in enumerate(row):
                if barrier.collides(pygame.mouse.get_pos()):
                    if not barrier.possiblePlacement:
                        continue
                    barrier.hover = True
                    self.Hbarriers[i+1][j].hover = True
                    return
                if not barrier.possiblePlacement:
                    continue

                self.clearHover(self.Hbarriers)

    def interactObject(self, listeObject: list[object], pos):
        for i, row in enumerate(listeObject):
            for j, element in enumerate(row):

                colli = element.collides(pos)
                if colli:
                    return (type(element).__name__, j, i)

    def mouseLogic(self, event):
        self.hoverCells()
        self.hoverVbarriers()
        self.hoverHbarriers()

        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            pos = pygame.mouse.get_pos()

            for array in [self.rect, self.Vbarriers, self.Hbarriers]:
                clickedElement = self.interactObject(array, pos)
                if clickedElement:
                    return clickedElement

        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
            self.clicked = False
            return False

    def quitWindow(self, event):
        if event.type == pygame.QUIT or event.type == 32787:
            pygame.quit()
            raise SystemExit

    def handleEvents(self):
        for event in pygame.event.get():
            self.quitWindow(event)
            return self.mouseLogic(event)

    def clearScreen(self):
        self.window.fill((240, 240, 240))

    def clearHighlight(self, objectList: list[object]):
        for row in objectList:
            for element in row:
                element.highlighted = False

    def clearPossiblePlacement(self, barrierList: list[object]):
        for row in barrierList:
            for element in row:
                element.possiblePlacement = False

    def clearAllHighlight(self):
        self.clearHighlight(self.rect)
        self.clearPossiblePlacement(self.Vbarriers)
        self.clearPossiblePlacement(self.Hbarriers)

    def clearHover(self, objectList: list[object]):
        for row in objectList:
            for element in row:
                element.hover = False
    



    def displayTable(self):
        backGround= pygame.image.load('pictures/backGround.jpg')
        self.window.blit(backGround,(0,0))
        for i, row in enumerate(self.rect):
            
            for j, cell in enumerate(row):
                cell.drawCase(self.window, i, j, cell.white)
                
                
                if cell.highlighted:
                    pygame.draw.rect(self.window, (255, 204, 255),
                                     (cell.x+2, cell.y+2, cell.sizeX-4, cell.sizeY-4))
                if cell.hover:
                    pygame.draw.rect(self.window, (255, 0, 0),
                                     (cell.x+2, cell.y+2, cell.sizeX-4, cell.sizeY-4))

                if cell.player.getNumber() != 0:
                    pygame.draw.circle(self.window,
                                       cell.player.getColor(),
                                       ((cell.x + cell.sizeCaseX()//2),
                                        (cell.y + cell.sizeCaseY()//2)),
                                       cell.sizeCaseX()//2-5)
                    

    def higlightPlayer(self, player):
        for i, row in enumerate(self.rect):
            for j, cell in enumerate(row):
                if cell.player == player:
                    pygame.draw.circle(self.window,
                                       (255, 255, 255),
                                       ((cell.x + cell.sizeCaseX()//2),
                                        (cell.y + cell.sizeCaseY()//2)),
                                       cell.sizeCaseX()//4)

    def displayBarriers(self, barrierList: list[object]):
        for i, row in enumerate(barrierList):
            for j, barrier in enumerate(row):
                if barrier.placed:
                    barrier.draw(self.window, i, j, self.grey)

                    continue

                barrier.draw(self.window, i, j, (255,0,0,128))
                if barrier.hover:
                    barrier.draw(self.window, i, j, self.grey)

    def displayIntersection(self):
        for i, row in enumerate(self.intersection):
            for j, intersection in enumerate(row):
                if ((self.Vbarriers[i][j].placed and
                     self.Vbarriers[i][j+1].placed) or
                    (self.Hbarriers[i][j].placed and
                     self.Hbarriers[i+1][j].placed)):

                    VnbBarriers = 0
                    if self.Vbarriers[i][j].placed == 1:
                        while j-VnbBarriers >= 0 and self.Vbarriers[i][j-VnbBarriers].placed:
                            VnbBarriers += 1

                    HnbBarriers = 0
                    if self.Hbarriers[i][j].placed == 1:
                        while i-HnbBarriers >= 0 and self.Hbarriers[i-HnbBarriers][j].placed:
                            HnbBarriers += 1

                    if VnbBarriers % 2 == 0 and HnbBarriers % 2 == 0:
                        continue

                    if i < len(self.Vbarriers)-1 and i < len(self.Hbarriers)-1:
                        if self.Vbarriers[i+1][j].placed:
                            intersection.draw(
                                self.window, i+1, j, self.grey)
                    if j < len(self.Vbarriers)-1 and j < len(self.Hbarriers)-1:
                        if self.Hbarriers[i][j+1].placed:
                            intersection.draw(
                                self.window, i, j+1, self.grey)

                    intersection.draw(self.window, i, j, self.grey)
                    continue

                intersection.draw(self.window, i, j, self.grey)
                if intersection.hover:
                    intersection.draw(self.window, i, j, (255, 0, 0))

    def newFrame(self):  
        self.clearScreen()
        self.displayTable()
        self.displayBarriers(self.Hbarriers)
        self.displayBarriers(self.Vbarriers)
        self.displayIntersection()
        
        self.higlightPlayer(self.player)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Board(7)

    while board.play:
        board.handleEvents()
        board.newFrame()

    pygame.quit()
