import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from multiplayerServer import createServer
from multiplayerServer import acceptConnexions


class WaitingRoom(Menu):
    def __init__(self, width: int, nbPlayer: int, nbBarrier: int, nbBot: int, serverName: str) -> None:
        super().__init__()
        self.width = width
        self.nbPlayer = nbPlayer
        self.nbBarrier = nbBarrier
        self.nbBot = nbBot
        self.serverName = serverName
        self.server = createServer(
            width, nbBarrier, nbPlayer, nbBot, serverName)
        # self.clientList = acceptConnexions(self.server.clientList)
        self.serverPosition = 0

    def displayPlayer(self) -> None:
        pygame.draw.rect(self.window, self.lighterBlue,
                         (50, 50, 640, 650), border_radius=5)

    def Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()

    def setWindow(self) -> None:
        self.window.fill(self.darkBlue, rect=None, special_flags=0)
        self.displayPlayer()
        Button(self.window, pygame.Rect(
            900, 50, 300, 100), self.lighterBlue, "Refresh")

        self.Event()
        pygame.display.flip()
