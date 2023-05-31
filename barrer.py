import pygame
from pygame.locals import *
from main import GraphicalGame

class selectBarrer():
    def __init__(self, NumberPlayers:int, NumberBots:int, GridSize:int,method:int) -> None:
        self.windowXmax = 500
        self.windowYmax = 700
        self.method = method
        self.NumberPlayers = NumberPlayers
        self.NumberBots = NumberBots
        self.GridSize = GridSize
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.center=(self.windowXmax//2, self.windowYmax//2)
        self.lighterBlue=(138,201,244)
        self.darkerBlue=(0,0,48)
        self.white=(255,255,255)
        self.choise=False
        self.font = pygame.font.Font(None, 36) 
        self.barrer=1
    


    def drawFirstCircle(self)->object:
        circle=pygame.draw.circle(self.window, self.darkerBlue, self.center, 120, width=0)
        return circle

    def drawSecondCircle(self)->None:
        circle=pygame.draw.circle(self.window, self.lighterBlue, self.center, 100, width=0)
        font=pygame.font.SysFont("Extra Bold Italic",90,False,True)
        text=font.render(str(self.barrer),True,self.white)
        buttonText= text.get_rect(center=circle.center)
        self.window.blit(text,buttonText)

    def drawfirstTriangle(self)->object:
        Triangle_point=[(295,365),(285,355),(305,355)]
        triangle=pygame.draw.polygon(self.window, self.white, Triangle_point)
        return triangle

    def drawSecondTriangle(self)->object:
        Triangle_point=[(295,335),(285,345),(305,345)]
        triangle=pygame.draw.polygon(self.window, self.white, Triangle_point)
        return triangle

    def ButtonBack(self)->object:
        coord=[(5,40),(30,10),(30,20),(70,20),(70,60),(30,60),(30,70)]
        button= pygame.draw.polygon(self.window,self.darkerBlue,coord)
        font=pygame.font.SysFont("Extra Bold Italic",20,False,True)
        text=font.render("Back",True,self.white)
        buttonText= text.get_rect(center=button.center)
        self.window.blit(text,buttonText)
        return button

    def drawButonDone(self)->None:
        button=pygame.draw.rect(self.window, self.lighterBlue, (50,560,400,120), width=0, border_radius=20)
        font=pygame.font.SysFont("Extra Bold Italic",60,False,True)
        text=font.render("Done",True,self.white)
        buttonText= text.get_rect(center=button.center)
        self.window.blit(text,buttonText)

    def Event(self)->None:
        from sizeGrid import SizeGrid

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.drawfirstTriangle().collidepoint(event.pos):
                    if self.barrer>1:
                        self.barrer -= 1
                elif self.drawSecondTriangle().collidepoint(event.pos)  :
                    if self.barrer < 3 and self.GridSize==5:
                        self.barrer += 1
                    elif self.barrer < 5 and self.GridSize==7:
                        self.barrer +=1
                    elif self.barrer<7 and self.GridSize==9:
                        self.barrer +=1
                    elif self.barrer < 10 and self.GridSize==11:
                        self.barrer +=1
                elif pygame.Rect(50,560,400,120).collidepoint(event.pos):
                    pygame.init()
                    board = GraphicalGame(self.GridSize,self.NumberPlayers,self.barrer,self.NumberBots)
                    while not self.getChoise():
                        board.mainLoop()
                        pygame.display.update()
                    pygame.quit()

                elif self.ButtonBack().collidepoint(event.pos)and event.button==1 :
                    pygame.init()
                    board = SizeGrid(self.NumberPlayers,self.NumberBots,self.method)
                    while not self.getChoise():
                        board.setWindow()
                        pygame.display.update()
                    pygame.quit()



    def setWindow(self)->None:
        backGround= pygame.image.load('pictures/backGroundMenu3.jpg')
        self.window.blit(backGround,(-80,-300))

        text_surface = self.font.render("Choise the number of barrer", True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 50))

        contour_surface = self.font.render("Choise the number of barrer", True, (0, 0, 0))
        contour_rect = contour_surface.get_rect(center=(self.windowXmax // 2, 50))
        contour_rect.move_ip(2, 2)  
        self.window.blit(contour_surface, contour_rect)
        self.window.blit(text_surface, text_rect)

        self.drawFirstCircle()
        self.drawSecondCircle()
        self.drawfirstTriangle()
        self.drawSecondTriangle()
        self.drawButonDone()
        self.Event()
        self.ButtonBack()
        pygame.display.flip()




    def getChoise(self):
        return self.choise


if __name__ == "__main__":
    pygame.init()
    board = selectBarrer(1,1,5)

    while not board.getChoise():
        board.setWindow()
        pygame.display.update()

    pygame.quit()



