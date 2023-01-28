import pygame
import sys
from pygame.locals import *

class TablePlayer:
    def __init__(self,boardX,boardY,Col,Row):
        self.boardX = boardX
        self.boardY = boardY
        self.col = Col
        self.row = Row
        self.black =(0,0,0)

    def numberCase(self):
        n= self.col
        return n

    def sizeCaseX(self):
        sizeX=(self.boardX//self.numberCase())-10
        return sizeX

    def sizeCaseY(self):
        sizeY = (self.boardY//self.numberCase())-10
        return sizeY

    def coordX(self,i):
        x = ((self.boardX//self.numberCase()))*i+2
        return x
    
    def coordY(self,j):
        y=((self.boardY//self.numberCase()))*j
        return y
    
    def drawCase(self, surface, i, j):
        x = self.coordX(i)
        y = self.coordY(j)
        width = self.sizeCaseX()
        height = self.sizeCaseY()
        casePlayer = pygame.draw.rect(surface, self.black, (x, y, width, height),2)
        
        for i in range(self.col):
            for j in range(self.row):
                casePlayer 

class VerticalBarrer():
    def __init__(self,boardX,boardY,Col,Row):
        self.boardX = boardX
        self.boardY = boardY
        self.col = Col
        self.row = Row
        self.black =(0,0,0)

    def numberCase(self):
        n = self.col
        return n

    def sizeVBarrerX(self):
        sizeX=12
        return sizeX

    def sizeVBarrerY(self):
        sizeY=(self.boardY//self.numberCase())-10
        return sizeY

    def coordX(self,i):
        x = ((self.boardX//self.numberCase()))*i+(self.boardX//self.numberCase())-10
        return x

    def coordY(self,j):
        y=(self.boardX//self.numberCase())*j
        return y

    def drawVBarrer(self,surface,i,j):
        x = self.coordX(i)
        y = self.coordY(j)
        width = self.sizeVBarrerX()
        height = self.sizeVBarrerY()
        Vbarrer = pygame.draw.rect(surface, self.black, (x, y, width, height))
        
        for i in range(self.col):
            for j in range(self.row):
                Vbarrer

class HorrizontalBarrer():
    def __init__(self,boardX,boardY,Col,Row):
        self.boardX = boardX
        self.boardY = boardY
        self.col = Col
        self.row = Row
        self.black =(0,0,0)

    def numberCase(self):
        n = self.col
        return n

    def sizeHBarrerX(self):
        sizeX=(self.boardY//self.numberCase())-10
        return sizeX

    def sizeHBarrerY(self):
        sizeY=10
        return sizeY

    def coordX(self,i):
        x = ((self.boardX//self.numberCase()))*i
        return x

    def coordY(self,j):
        y=(self.boardX//self.numberCase())*j+(self.boardX//self.numberCase())-10
        return y

    def drawHBarrer(self,surface,i,j):
        x = self.coordX(i)
        y = self.coordY(j)
        width = self.sizeHBarrerX()
        height = self.sizeHBarrerY()
        Hbarrer = pygame.draw.rect(surface, self.black, (x, y, width, height))
        
        for i in range(self.col):
            for j in range(self.row):
                Hbarrer

class Game:
    def __init__(self, Col, Row):
        self.col = Col
        self.row = Row
        self.windowXmax = 800
        self.windowYmax = 800
        self.window= pygame.display.set_mode((self.windowXmax, self.windowYmax))

        

        pygame.display.set_caption("plateau")
        self.play = True

    def displayBoard(self):
        while self.play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.window.fill((240,240,240))
            for i in range(self.col):
                for j in range(self.row):
                    TablePlayer(self.windowXmax, self.windowYmax,self.col,self.row).drawCase(self.window,i,j)
            for i in range(self.col-1):
                for j in range(self.row):
                    VerticalBarrer(self.windowXmax, self.windowYmax,self.col,self.row).drawVBarrer(self.window,i,j)
            for i in range(self.col):
                for j in range(self.row-1):
                    HorrizontalBarrer(self.windowXmax, self.windowYmax,self.col,self.row).drawHBarrer(self.window,i,j)
            

            pygame.display.flip()


pygame.init()
Game(7,7).displayBoard()
pygame.quit()