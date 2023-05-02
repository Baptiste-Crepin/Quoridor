import pygame
from pygame.locals import *

class Menu:
    def __init__(self):
        self.windowXmax = 500
        self.windowYmax = 700
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.choise = False
        self.blue=(138,201,244)
        self.white = (255,255,255)
        

    def createButtonSolo(self):
        button=pygame.draw.rect(self.window, self.blue, (50,200,400,120), width=0, border_radius=20)
        font=pygame.font.SysFont("Extra Bold Italic",60,False,True)
        text=font.render("SOLO",True,self.white)
        buttonText= text.get_rect(center=button.center)
        self.window.blit(text,buttonText)

    def createButtonMulti(self):
        button=pygame.draw.rect(self.window, self.blue, (50,370,400,120), width=0, border_radius=20)
        font=pygame.font.SysFont("Extra Bold Italic",60,False,True)
        text=font.render("MULTI",True,self.white)
        buttonText= text.get_rect(center=button.center)
        self.window.blit(text,buttonText)

    def setWindow(self):
        backGround= pygame.image.load('pictures/Foret.jpg')
        self.window.blit(backGround,(0,0))
        self.createButtonSolo()
        self.createButtonMulti()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.choise=True
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
