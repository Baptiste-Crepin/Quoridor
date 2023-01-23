import pygame
import sys
from pygame.locals import *






class Game:
    def __init__(self):

        self.grid = [
                    ((0,152),(800,152)),
                    ((0,162),(800,162)),
                    ((0,314),(800,314)),
                    ((0,324),(800,324)),
                    ((0,476),(800,476)),
                    ((0,486),(800,486)),
                    ((0,638),(800,638)),
                    ((0,648),(800,648)),
                    ((152,0),(152,800)),
                    ((162,0),(162,800)),
                    ((314,0),(314,800)),
                    ((324,0),(324,800)),
                    ((476,0),(476,800)),
                    ((486,0),(486,800)),
                    ((638,0),(638,800)),
                    ((648,0),(648,800))
        ]
        self.window= pygame.display.set_mode((800, 800))
        pygame.display.set_caption("plateau")
        self.play = True

    def displayGrid(self):
        while self.play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self.window.fill((240,240,240))

            for line in self.grid:
                pygame.draw.line(self.window,(0,0,0),line[0],line[1],2)
            pygame.display.flip()

if __name__ == "__plateau__":
    pygame.init()
    Game().displayGrid()
    pygame.quit()