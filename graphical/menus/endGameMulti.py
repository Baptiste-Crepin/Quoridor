import pygame

from Play import Play
from graphical.menus.endGame import End
from graphical.widgets.button import Button
from player import Player


class EndGameMulti(End):
    def __init__(self, curentPlayer: Player, width: int, nbPlayer: int, nbBarrier: int, nbBots: int,
                 searchserver: object, host: bool):
        super().__init__(curentPlayer, width, nbPlayer, nbBarrier, nbBots)
        self.searchserevr = searchserver
        self.host = host

    def Event(self):
        for event in pygame.event.get():
            self.defaultEventHandler(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.coordLobby).collidepoint(event.pos):
                    board = Play(self.fullScreen)
                    self.newMenu(self, board)
                elif pygame.Rect(self.coordReplay).collidepoint(event.pos):
                    if self.host:
                        print("host clicked on replay")
                        pass
                elif pygame.Rect(self.coordQuit).collidepoint(event.pos):
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
        if self.host:
            Button(self.window, self.coordReplay, self.blue, "REPLAY")
        self.Event()
        pygame.display.flip()
