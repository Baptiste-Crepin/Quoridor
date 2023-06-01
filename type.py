import pygame
from pygame.locals import *
from button import Button

class Menutype:
    def __init__(self):
        self.windowXmax = 500
        self.windowYmax = 700
        self.posSolo=(50,200)
        self.posMulti =(50,370)
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.blue=(138,201,244)
        self.white = (255,255,255)
        self.darkerBlue=(0,0,48)

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
        Button(self.window, (50,200,400,120), self.blue, "Solo")
        Button(self.window, (50,370,400,120), self.blue, "Muti")
        self.ButtonBack()
        self.Event()

    def Event(self):
        from choicePlayer import NumberPlayer
        from Play import Menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.posSolo, (400,120)).collidepoint(event.pos):
                    
                    pygame.init()
                    board = NumberPlayer()
                    while True:
                        board.setWindow()
                        pygame.display.update()
                    
                elif pygame.Rect(self.posMulti, (400,120)).collidepoint(event.pos):
                    pygame.quit()
                elif self.ButtonBack().collidepoint(event.pos)and event.button==1:
                    pygame.init()
                    board = Menu()
                    while True:
                        board.setWindow()
                        pygame.display.update()
                    
            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    board = Menutype()

    while True:
        board.setWindow()
        pygame.display.update()

    pygame.quit()
