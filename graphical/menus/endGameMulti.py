import pygame

from main import Play
from graphical.menus.endGame import End
from graphical.widgets.button import Button
from gameLogic.player import Player


class EndGameMulti(End):
    def __init__(self, currentPlayer: Player, width: int, nbPlayer: int, nbBarrier: int, nbBots: int,
                 searchServer: object, host: bool):
        super().__init__(currentPlayer, width, nbPlayer, nbBarrier, nbBots)
        self.searchServer = searchServer
        self.host = host
        self.coordLobby = pygame.Rect(self.windowWidth//2-100 - 150,
                                      self.windowHeight//2 + 250, 200, 80)
        self.coordQuit = pygame.Rect(self.windowWidth//2 - 100 + 150,
                                     self.windowHeight//2+250, 200, 80)

    def Event(self):
        for event in pygame.event.get():
            self.defaultEventHandler(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.coordLobby).collidepoint(event.pos):
                    board = Play()
                    self.newMenu(self, board)
                elif pygame.Rect(self.coordQuit).collidepoint(event.pos):
                    print("a")
                    raise SystemExit

    def mainLoop(self):
        """end game display loop"""
        self.window.fill(self.backGround)
        text_surface = self.font.render(self.Winner(), True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowWidth // 2, 100))
        self.window.blit(text_surface, text_rect)
        self.displayWinner()
        Button(self.window, self.coordLobby, self.blue, "LOBBY")
        Button(self.window, self.coordQuit, self.blue, "QUIT")
        self.Event()
        pygame.display.flip()
