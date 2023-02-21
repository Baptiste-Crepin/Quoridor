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

        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 0, 255)
        self.player = Player(0)

        self.x = 0
        self.y = 0
        self.sizeX = 0
        self.sizeY = 0

    def numberCase(self):
        n = self.col
        return n

    def sizeCaseX(self):
        sizeX = (self.boardX//self.numberCase())-10
        self.sizeX = sizeX
        return sizeX

    def sizeCaseY(self):
        sizeY = (self.boardY//self.numberCase())-10
        self.sizeY = sizeY
        return sizeY

    def coordX(self, i):
        x = ((self.boardX//self.numberCase()))*i+5
        self.x = x
        return x

    def coordY(self, j):
        y = ((self.boardY//self.numberCase()))*j
        self.y = y
        return y

    def drawCase(self, surface, i, j):
        x = self.coordX(i)
        y = self.coordY(j)
        width = self.sizeCaseX()
        height = self.sizeCaseY()
        casePlayer = pygame.draw.rect(
            surface, self.black, (x, y, width, height), 2)
        return casePlayer

    def collides(self, otherCoord):
        if otherCoord[0] < self.x or otherCoord[0] > self.x + self.sizeX:
            return False
        if otherCoord[1] < self.y or otherCoord[1] > self.y + self.sizeY:
            return False

        return True


class VerticalBarrer():
    def __init__(self, boardX, boardY, Col, Row):
        self.boardX = boardX
        self.boardY = boardY
        self.col = Col
        self.row = Row
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.placed = 0
        self.x = 0
        self.y = 0
        self.sizeX = 0
        self.sizeY = 0

    def numberCase(self):
        n = self.col
        return n

    def sizeVBarrerX(self):
        sizeX = 10
        self.sizeX = sizeX
        return sizeX

    def sizeVBarrerY(self):
        sizeY = (self.boardY//self.numberCase())
        self.sizeY = sizeY
        return sizeY

    def coordX(self, i):
        x = ((self.boardX//self.numberCase())) * \
            i+(self.boardX//self.numberCase())-5
        self.x = x
        return x

    def coordY(self, j):
        y = (self.boardX//self.numberCase())*j
        self.y = y
        return y

    def drawVBarrer(self, surface, i, j):
        x = self.coordX(i)
        y = self.coordY(j)
        width = self.sizeVBarrerX()
        height = self.sizeVBarrerY()
        if self.placed == 0:
            Vbarrer = pygame.draw.rect(
                surface, self.white, (x, y, width, height))
        else:
            Vbarrer = pygame.draw.rect(
                surface, self.black, (x, y, width, height))
        return Vbarrer

    def collides(self, otherCoord):
        if otherCoord[0] < self.x or otherCoord[0] > self.x + self.sizeX:
            return False
        if otherCoord[1] < self.y or otherCoord[1] > self.y + self.sizeY:
            return False

        return True


class HorrizontalBarrer():
    def __init__(self, boardX, boardY, Col, Row):
        self.boardX = boardX
        self.boardY = boardY
        self.col = Col
        self.row = Row
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.placed = 0
        self.x = 0
        self.y = 0
        self.sizeX = 0
        self.sizeY = 0

    def numberCase(self):
        n = self.col
        return n

    def sizeHBarrerX(self):
        sizeX = (self.boardY//self.numberCase())
        self.sizeX = sizeX
        return sizeX

    def sizeHBarrerY(self):
        sizeY = 10
        self.sizeY = sizeY
        return sizeY

    def coordX(self, i):
        x = ((self.boardX//self.numberCase()))*i+5
        self.x = x
        return x

    def coordY(self, j):
        y = (self.boardX//self.numberCase())*j + \
            (self.boardX//self.numberCase())-10
        self.y = y
        return y

    def drawHBarrer(self, surface, i, j):
        x = self.coordX(i)
        y = self.coordY(j)
        width = self.sizeHBarrerX()
        height = self.sizeHBarrerY()
        Hbarrer = pygame.draw.rect(surface, self.white, (x, y, width, height))

        if self.placed == 0:
            Hbarrer = pygame.draw.rect(
                surface, self.white, (x, y, width, height))
        else:
            Hbarrer = pygame.draw.rect(
                surface, self.black, (x, y, width, height))
        return Hbarrer

    def collides(self, otherCoord):
        if otherCoord[0] < self.x or otherCoord[0] > self.x + self.sizeX:
            return False
        if otherCoord[1] < self.y or otherCoord[1] > self.y + self.sizeY:
            return False

        return True


class Board:
    def __init__(self, Width):
        self.col = Width
        self.row = Width
        self.windowXmax = 800
        self.windowYmax = 800
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        self.clicked = False

        self.rect = self.initializeGrid()
        self.Vbarrers = self.initializeVBarrers()
        self.Hbarrers = self.initializeHBarrers()

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

    def initializeVBarrers(self):
        rectArray = []
        for i in range(self.col-1):
            row = []
            for j in range(self.row):
                barrer = VerticalBarrer(
                    self.windowXmax,
                    self.windowYmax,
                    self.col,
                    self.row)
                row.append(barrer)
            rectArray.append(row)
        return rectArray

    def initializeHBarrers(self):
        rectArray = []
        for i in range(self.col):
            row = []
            for j in range(self.row-1):
                barrer = HorrizontalBarrer(self.windowXmax,
                                           self.windowYmax,
                                           self.col,
                                           self.row)
                row.append(barrer)
            rectArray.append(row)
        return rectArray

    def mouseLogic(self, event):
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            pos = pygame.mouse.get_pos()
            for i, row in enumerate(self.rect):
                for j, cell in enumerate(row):
                    colli = cell.collides(pos)
                    if colli:
                        return ('move', j, i)
            for i, row in enumerate(self.Vbarrers):
                for j, barrer in enumerate(row):
                    colli = barrer.collides(pos)
                    if colli:
                        return ('placeV', j, i)
            for i, row in enumerate(self.Hbarrers):
                for j, barrer in enumerate(row):
                    colli = barrer.collides(pos)
                    if colli:
                        return ('placeH', j, i)

            return pos
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
            self.clicked = False
            return False

    def quitWindow(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    def handleEvents(self):
        for event in pygame.event.get():
            self.quitWindow(event)
            return self.mouseLogic(event)

    def clearScreen(self):
        self.window.fill((240, 240, 240))

    def displayTable(self):
        for i, row in enumerate(self.rect):
            for j, cell in enumerate(row):
                cell.drawCase(self.window, i, j)

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
                    # pygame.display.flip()

    def displayBarrers(self):
        for i, row in enumerate(self.Vbarrers):
            for j, barrer in enumerate(row):
                barrer.drawVBarrer(self.window, i, j)

        for i, row in enumerate(self.Hbarrers):
            for j, barrer in enumerate(row):
                barrer.drawHBarrer(self.window, i, j)


    def newFrame(self):
        self.clearScreen()

        self.displayBarrers()
        self.displayTable()
        self.higlightPlayer(self.player)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = Board(7)

    while board.play:
        board.handleEvents()
        board.newFrame()

    pygame.quit()
