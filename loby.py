import pygame
from pygame.locals import *
from type import Menutype
from button import Button

class Menu:
    def __init__(self)-> None:
        self.windowXmax = 500
        self.windowYmax = 700
        self.posPlay=(50,200)
        self.posRules =(50,370)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.choise = False
        self.blue=(138,201,244)
        self.white = (255,255,255)
        self.play=Button(self.playButtonLogic,50,200,400,120,self.window,self.blue,'Play')
        

    def soloButtonLogic(self):
        button = Button(self.SoloButtonLogic, 50, 200, 400, 120, self.window, self.blue, 'Solo')
        button.createButton()
        return button

    def playButtonLogic(self):
        print("hey")





    def Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.getchoise = True

            if self.play.buttonLogic(event):
                self.play.buttonAction()

    def setWindow(self):
        background = pygame.image.load('pictures/Foret.jpg')
        self.window.blit(background, (0, 0))
        self.play.createButton()

        self.Event()
        pygame.display.flip()

    def getChoise(self):
        return self.choise
    
if __name__ == "__main__":
    pygame.init()
    board = Menu()

    while not board.getChoise():
        board.setWindow()
        pygame.display.update()

    pygame.quit() 
