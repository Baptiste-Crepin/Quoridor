import pygame
from pygame.locals import *
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
        self.blue=(138,201,244)
        self.white = (255,255,255)

    def Event(self)->None:
        from rules import Rules
        from type import Menutype
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posPlay, (400,120)).collidepoint(event.pos):
                        pygame.init()
                        board = Menutype()
                        while True:
                            board.setWindow()
                            pygame.display.update()
                        
                elif pygame.Rect(self.posRules, (400,120)).collidepoint(event.pos):
                        pygame.init()
                        board = Rules()
                        while True:
                            board.setWindow()
                            pygame.display.update()
                    
        pygame.display.flip()

    def setWindow(self)->None:
        backGround= pygame.image.load('pictures/backGroundMenu3.jpg')
        self.window.blit(backGround,(-80,-300))
        Button(self.window, (50,200,400,120), self.blue, "PLAY")
        Button(self.window, (50,370,400,120), self.blue, "RULES")
        self.Event()


if __name__ == "__main__":
    pygame.init()
    board = Menu()

    while True:
        board.setWindow()
        pygame.display.update()

