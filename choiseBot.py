import pygame
from pygame.locals import *
from sizeGrid import SizeGrid

class NumberBots():
    def __init__(self, nbPlayers:int)->None:
        self.nbPlayers = nbPlayers
        self.windowXmax = 500
        self.windowYmax = 700
        self.pos1=(50,200)
        self.pos2 =(50,370)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.choise = False
        self.blue=(138,201,244)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.font = pygame.font.Font(None, 36)  

    def createButtonOne(self)->None:
        button = pygame.draw.rect(self.window, self.blue, (50,200,400,70), width=0, border_radius=20)
        text = self.font.render("1", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)


    def createButtonThree(self)->None:
        button = pygame.draw.rect(self.window, self.blue, (50,370,400,70), width=0, border_radius=20)
        text = self.font.render("3", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def createButtonYes(self)->None:
        button = pygame.draw.rect(self.window, self.blue, (50,200,400,70), width=0, border_radius=20)
        text = self.font.render("Yes", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText) 


    def createButtonNo(self)->None:
        button = pygame.draw.rect(self.window, self.blue, (50,370,400,70), width=0, border_radius=20)
        text = self.font.render("No", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)


    def setWindow(self)->None:
            backGround = pygame.image.load('pictures/Foret.jpg')
            self.window.blit(backGround, (0,0))
            if self.nbPlayers==1:
                text_surface = self.font.render("How many bots?", True, self.white)
                text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 50))

                contour_surface = self.font.render("How many bots?", True, (0, 0, 0))
                contour_rect = contour_surface.get_rect(center=(self.windowXmax // 2, 50))
                contour_rect.move_ip(2, 2)  

                self.window.blit(contour_surface, contour_rect)
                self.window.blit(text_surface, text_rect)

            
                self.createButtonOne()
                self.createButtonThree()
                self.Event(1)

            elif self.nbPlayers==2:
                text_surface = self.font.render("Do you want to play with bots?", True, self.white)
                text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 50))

                contour_surface = self.font.render("Do you want to play with bots?", True, (0, 0, 0))
                contour_rect = contour_surface.get_rect(center=(self.windowXmax // 2, 50))
                contour_rect.move_ip(2, 2)  

                self.window.blit(contour_surface, contour_rect)
                self.window.blit(text_surface, text_rect)
                self.createButtonYes()
                self.createButtonNo()

                self.Event(2)

    def getChoise(self)->bool:
        return self.choise

    def Event(self,method:int)->None:
        for event in pygame.event.get():
            if method == 1 :
                if event.type == pygame.QUIT:
                    self.choise = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if pygame.Rect(self.pos1, (400,120)).collidepoint(event.pos):
                        pygame.init()
                        board = SizeGrid(self.nbPlayers,1)
                        while not self.getChoise():
                            board.setWindow()
                            pygame.display.update()
                        pygame.quit()
                    elif pygame.Rect(self.pos2, (400,120)).collidepoint(event.pos):
                        pygame.init()
                        board = SizeGrid(self.nbPlayers,3)
                        while not self.getChoise():
                            board.setWindow()
                            pygame.display.update()
                        pygame.quit()    
            if method == 2 :
                if event.type == pygame.QUIT:
                    self.choise = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if pygame.Rect(self.pos1, (400,120)).collidepoint(event.pos):
                        pygame.init()
                        board = SizeGrid(self.nbPlayers,2)
                        while not self.getChoise():
                            board.setWindow()
                            pygame.display.update()
                        pygame.quit()

                    elif pygame.Rect(self.pos2, (400,120)).collidepoint(event.pos):
                        pygame.init()
                        board = SizeGrid(self.nbPlayers,0)
                        while not self.getChoise():
                            board.setWindow()
                            pygame.display.update()
                        pygame.quit()

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    board = NumberBots(2)

    while not board.getChoise():
        board.setWindow()
        pygame.display.update()

    pygame.quit()
