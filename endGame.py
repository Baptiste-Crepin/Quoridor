import pygame
from pygame.locals import *
from Player import Player
from Play import Menu
from button import Button


class End:
    def __init__(self, curentPlayer: Player, width: int, nbPlayer: int, nbBarrier: int, nbBots: int):
        self.curentplayer = curentPlayer
        self.width = width
        self.nbPlayer = nbPlayer
        self.nbBarrier = nbBarrier
        self.nbBots = nbBots
        self.windowXmax = 1330
        self.windowYmax = 750
        self.window = pygame.display.set_mode(
            (self.windowXmax, self.windowYmax))
        pygame.display.set_caption("Quoridor")
        self.blue = (138, 201, 244)
        self.white = (255, 255, 255)
        self.darkBlue = pygame.Color(0, 0, 48)
        self.center = (self.windowXmax//2, self.windowYmax//2)
        self.coordQuit = (self.windowXmax//2-110,
                          self.windowYmax//2+250, 200, 80)
        self.coordReplay = (self.windowXmax//2-220,
                            self.windowYmax//2+150, 200, 80)
        self.coordLobby = (self.windowXmax//2+20,
                           self.windowYmax//2+150, 200, 80)
        self.font = pygame.font.Font(None, 36)

    def Winner(self) -> str:
        return self.curentplayer.stringColor() + " Player won !"

    def displayWinner(self) -> None:
        pygame.draw.circle(
            self.window, self.curentplayer.getColor(), self.center, 100)

    def Event(self):
        for event in pygame.event.get():
            from main import GraphicalGame
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.coordLobby).collidepoint(event.pos):
                    pygame.init()
                    board = Menu()
                    while True:
                        board.setWindow()
                        pygame.display.update()
                elif pygame.Rect(self.coordReplay).collidepoint(event.pos):
                    pygame.init()
                    board = GraphicalGame(
                        self.width, self.nbPlayer, self.nbBarrier, self.nbBots)
                    while True:
                        board.mainLoop()
                        pygame.display.update()
                elif pygame.Rect(self.coordQuit).collidepoint(event.pos):
                    pygame.quit()

    def setWindow(self):
        self.window.fill(self.darkBlue)
        text_surface = self.font.render(self.Winner(), True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowXmax // 2, 100))
        self.window.blit(text_surface, text_rect)
        self.displayWinner()
        Button(self.window, self.coordLobby, self.blue, "LOBBY")
        Button(self.window, self.coordQuit, self.blue, "QUIT")
        Button(self.window, self.coordReplay, self.blue, "REPLAY")
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = End()

    while True:
        board.setWindow()
        pygame.display.update()
