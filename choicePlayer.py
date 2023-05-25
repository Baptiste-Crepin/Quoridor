import pygame
from pygame.locals import *


class NumberPlayer:
    def __init__(self):
        self.windowXmax = 500
        self.windowYmax = 700
        self.pos1=(100,250)
        self.pos2 =(300,250)
        self.pos3 =(100,420)
        self.pos4 =(300,420)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.choise = False
        self.blue=(138,201,244)
        self.white = (255,255,255)
        self.darkerBlue=(0,0,48)
        self.black = (0,0,0)
        self.font = pygame.font.Font(None, 36)  

    def createButtonOne(self):
        button = pygame.draw.rect(self.window, self.blue, (100,230,100,100), width=0, border_radius=20)
        text = self.font.render("1", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def createButtonTwo(self):
        button = pygame.draw.rect(self.window, self.blue, (300,230,100,100), width=0, border_radius=20)
        text = self.font.render("2", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def createButtonThree(self):
        button = pygame.draw.rect(self.window, self.blue, (100,420,100,100), width=0, border_radius=20)
        text = self.font.render("3", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def createButtonFour(self):
        button = pygame.draw.rect(self.window, self.blue, (300,420,100,100), width=0, border_radius=20)
        text = self.font.render("4", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def ButtonBack(self)->object:
        coord=[(5,40),(30,10),(30,20),(70,20),(70,60),(30,60),(30,70)]
        button= pygame.draw.polygon(self.window,self.darkerBlue,coord)
        font=pygame.font.SysFont("Extra Bold Italic",20,False,True)
        text=font.render("Back",True,self.white)
        buttonText= text.get_rect(center=button.center)
        self.window.blit(text,buttonText)
        return button

    def setWindow(self):
        backGround= pygame.image.load('pictures/backGroundMenu3.jpg')
        self.window.blit(backGround,(-80,-300))

        text_surface = self.font.render("How many players?", True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 50))

        contour_surface = self.font.render("How many players?", True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(center=(self.windowXmax // 2, 50))
        contour_rect.move_ip(2, 2)  

        self.window.blit(contour_surface, contour_rect)
        self.window.blit(text_surface, text_rect)

        self.createButtonOne()
        self.createButtonThree()
        self.createButtonTwo()
        self.createButtonFour()
        self.ButtonBack()
        self.Event()

    def getChoise(self):
        return self.choise

    def Event(self):
        from choiseBot import NumberBots
        from sizeGrid import SizeGrid
        from type import Menutype

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.choise = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.pos1, (70,100)).collidepoint(event.pos):
                    pygame.init()
                    board = NumberBots(1)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()
                elif pygame.Rect(self.pos2, (100,100)).collidepoint(event.pos):
                    pygame.init()
                    board = NumberBots(2)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()

                elif pygame.Rect(self.pos3, (100,100)).collidepoint(event.pos):
                    pygame.init()
                    board = SizeGrid(3,1,1)
                    while not self.getChoise():
                            board.setWindow()
                            pygame.display.update()
                    pygame.quit()

                elif pygame.Rect(self.pos4, (100,100)).collidepoint(event.pos):
                    pygame.init()
                    board = SizeGrid(4,0,1)
                    while not self.getChoise():
                            board.setWindow()
                            pygame.display.update()
                    pygame.quit()
                elif self.ButtonBack().collidepoint(event.pos)and event.button==1:
                    pygame.init()
                    board = Menutype()
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    board = NumberPlayer()

    while not board.getChoise():
        board.setWindow()
        pygame.display.update()

    pygame.quit()
