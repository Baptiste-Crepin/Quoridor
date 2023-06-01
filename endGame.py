import pygame
from pygame.locals import *
from Player import Player
from Play import Menu

class End:
    def __init__(self,curentPlayer:Player):
        self.curentplayer=curentPlayer
        self.windowXmax = 1330
        self.windowYmax = 750
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.choise = False
        self.blue=(138,201,244)
        self.white = (255,255,255)
        self.darkBlue = pygame.Color(0,0,48)
        self.center=(self.windowXmax//2, self.windowYmax//2)
        self.coordReplay=(self.windowXmax//2+20, self.windowYmax//2+150,200,80)
        self.coordQuit=(self.windowXmax//2-220, self.windowYmax//2+150,200,80)
        self.font = pygame.font.Font(None, 36) 

    def winnerNumber(self)->int:
        return self.curentplayer.getNumber()


    def WinnerColor(self)->pygame.Color:
        return Player(self.winnerNumber()).getColor()
    
    def Winner(self)->str:
        if self.winnerNumber()==1:
            return "Well played Red! You win!"
        if self.winnerNumber()==2:
            return "Well played Yellow! You win!"        
        if self.winnerNumber()==3:
            return "Well played Green! You win!"
        if self.winnerNumber()==4:
            return "Well played Blue! You win!"
        
    def displayWinner(self)->None:
        pygame.draw.circle(self.window,self.WinnerColor(),self.center,100)

    def createButtonReplay(self):
        button=pygame.draw.rect(self.window, self.blue, self.coordReplay, width=0, border_radius=20)
        font=pygame.font.SysFont("Extra Bold Italic",40,False,True)
        text=font.render("REPLAY",True,self.white)
        buttonText= text.get_rect(center=button.center)
        self.window.blit(text,buttonText)

    def createButtonQuit(self):
        button=pygame.draw.rect(self.window, self.blue, self.coordQuit, width=0, border_radius=20)
        font=pygame.font.SysFont("Extra Bold Italic",40,False,True)
        text=font.render("QUIT",True,self.white)
        buttonText= text.get_rect(center=button.center)
        self.window.blit(text,buttonText)


    def Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.choise=True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.coordReplay).collidepoint(event.pos):
                        pygame.init()
                        board = Menu()
                        while not self.getChoise():
                            board.setWindow()
                            pygame.display.update()
                        pygame.quit()
                elif pygame.Rect(self.coordQuit).collidepoint(event.pos):
                        pygame.quit()
                    
        pygame.display.flip()

    def setWindow(self):
        self.window.fill(self.darkBlue)
        text_surface = self.font.render(self.Winner(), True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 100))
        self.window.blit(text_surface, text_rect)
        
        
        self.displayWinner()
        self.createButtonReplay()
        self.createButtonQuit()
        self.Event()

    def getChoise(self):
        return self.choise
    
if __name__ == "__main__":
    pygame.init()
    board = End()

    while not board.getChoise():
        board.setWindow()
        pygame.display.update()

    pygame.quit() 
