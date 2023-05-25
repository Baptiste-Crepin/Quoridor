import pygame
from pygame.locals import *


class SizeGrid:
    def __init__(self, nbPlayer:int, nbBot:int,method:int):
        self.nbPlayers = nbPlayer
        self.method = method
        self.nbBot = nbBot
        self.windowXmax = 500
        self.windowYmax = 700
        self.pos1=(150,200)
        self.pos2 =(150,370)
        self.pos3 =(300,200)
        self.pos4 =(300,370)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.choise = False
        self.blue=(138,201,244)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.darkerBlue=(0,0,48)
        self.font = pygame.font.Font(None, 36)  

    def createButtonFiveToFive(self):
        button = pygame.draw.rect(self.window, self.blue, (150,200,70,70), width=0, border_radius=20)
        text = self.font.render("5x5", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def createButtonSevenToSeven(self):
        button = pygame.draw.rect(self.window, self.blue, (150,370,70,70), width=0, border_radius=20)
        text = self.font.render("7x7", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def createButtonNineToNine(self):
        button = pygame.draw.rect(self.window, self.blue, (300,200,70,70), width=0, border_radius=20)
        text = self.font.render("9x9", True, self.white)
        buttonText = text.get_rect(center=button.center)
        self.window.blit(text, buttonText)

    def createButtonElevenToEleven(self):
        button = pygame.draw.rect(self.window, self.blue, (300,370,70,70), width=0, border_radius=20)
        text = self.font.render("11x11", True, self.white)
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

        text_surface = self.font.render("Choise the size of the grid", True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 50))

        contour_surface = self.font.render("Choise the size of the grid", True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(center=(self.windowXmax // 2, 50))
        contour_rect.move_ip(2, 2)  

        self.window.blit(contour_surface, contour_rect)
        self.window.blit(text_surface, text_rect)

        self.createButtonFiveToFive()
        self.createButtonNineToNine()
        self.createButtonSevenToSeven()
        self.createButtonElevenToEleven()
        self.ButtonBack()
        self.Event()

    def getChoise(self):
        return self.choise

    def Event(self):
        from barrer import selectBarrer
        from choicePlayer import NumberPlayer
        from choiseBot import NumberBots


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.choise = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.method ==1:
                if pygame.Rect(self.pos1, (70,70)).collidepoint(event.pos):
                    pygame.init()
                    board = selectBarrer(self.nbPlayers,self.nbBot,5,1)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()
                elif pygame.Rect(self.pos2, (70,70)).collidepoint(event.pos):
                    pygame.init()
                    board = selectBarrer(self.nbPlayers,self.nbBot,7,1)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()

                elif pygame.Rect(self.pos3, (70,70)).collidepoint(event.pos):
                    pygame.init()
                    board = selectBarrer(self.nbPlayers,self.nbBot,9,1)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()
                elif pygame.Rect(self.pos4, (70,70)).collidepoint(event.pos):
                    pygame.init()
                    board = selectBarrer(self.nbPlayers,self.nbBot,11,1)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                elif self.ButtonBack().collidepoint(event.pos)and event.button==1 :
                    pygame.init()
                    board = NumberPlayer()
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.method ==2:
                if pygame.Rect(self.pos1, (70,70)).collidepoint(event.pos):
                    pygame.init()
                    board = selectBarrer(self.nbPlayers,self.nbBot,5,2)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()
                elif pygame.Rect(self.pos2, (70,70)).collidepoint(event.pos):
                    pygame.init()
                    board = selectBarrer(self.nbPlayers,self.nbBot,7,2)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()

                elif pygame.Rect(self.pos3, (70,70)).collidepoint(event.pos):
                    pygame.init()
                    board = selectBarrer(self.nbPlayers,self.nbBot,9,2)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()
                elif pygame.Rect(self.pos4, (70,70)).collidepoint(event.pos):
                    pygame.init()
                    board = selectBarrer(self.nbPlayers,self.nbBot,11,2)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                elif self.ButtonBack().collidepoint(event.pos)and event.button==1 :
                    pygame.init()
                    board = NumberBots(self.nbPlayers)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    board = SizeGrid()

    while not board.getChoise():
        board.setWindow()
        pygame.display.update()

    pygame.quit()
