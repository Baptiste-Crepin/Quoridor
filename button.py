from pygame.locals import *
import pygame 

class Button():
    def __init__(self, function, x:int, y:int, width:int, height:int, surface,color,text:str) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.function = function
        self.surface = surface
        self.color = color
        self.text = text
        self.white = (255,255,255)

    def createButton(self) :
        button_rect = pygame.draw.rect(self.surface, self.color, self.rect,border_radius=20)
        font = pygame.font.SysFont("Extra Bold Italic", 60, False, True)
        text = font.render(self.text, True, self.white)
        buttonText = text.get_rect(center=button_rect.center)
        self.surface.blit(text, buttonText)
        pygame.display.flip()
        


    def buttonLogic(self,event)-> bool:
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(self.rect).collidepoint(event.pos):
                self.is_clicked = True


            if self.rect.collidepoint(event.pos):
                return True


    def buttonAction(self)-> None:
        if self.buttonLogic==True:
            self.function