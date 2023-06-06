import pygame
import socket
import threading

from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from player import Player
from multiplayerServer import createServer
from multiplayerClient import SearchServer


class WaitingRoom(Menu):
    def __init__(self, startvars: list, width: int, nbPlayer: int, nbBarrier: int, nbBot: int, serverName: str, serverConnection, Host: bool = False) -> None:
        super().__init__()
        self.width = width
        self.nbPlayer = nbPlayer
        self.nbBarrier = nbBarrier
        self.nbBot = nbBot
        self.serverName = serverName
        self.serverConnection = serverConnection
        self.host = Host
        self.start = False
        self.startvars = startvars
        self.serverConnection.connexion.setblocking(False)

        self.clientList = ["zrberve", 'ejdàej', 'roefijer']

    def displayPlayer(self) -> None:
        for i in range(4):
            if len(self.clientList)-1 >= i:
                pygame.draw.circle(self.window, Player(i+1).getColor(
                ), ((self.windowWidth//5)*i+self.windowWidth//5, self.windowHeight//3), 70)
                font = pygame.font.SysFont(
                    "Extra Bold Italic", 60, False, True)
                player = font.render(
                    "player "+str(i+1), True, self.white)
                self.window.blit(
                    player, ((self.windowWidth//5)*i+self.windowWidth//7, self.windowHeight//3+80))
            elif len(self.clientList)-1 < i:
                pygame.draw.circle(self.window, Player(i+1).getColor(
                ), ((self.windowWidth//5)*i+self.windowWidth//5, self.windowHeight//3), 70, 10)
                font = pygame.font.SysFont(
                    "Extra Bold Italic", 60, False, True)
                wait = font.render(
                    "waiting for", True, self.white)
                player = font.render(
                    "player "+str(i+1), True, self.white)
                self.window.blit(
                    wait, ((self.windowWidth//5)*i+self.windowWidth//8, self.windowHeight//3+80))
                self.window.blit(
                    player, ((self.windowWidth//5)*i+self.windowWidth//7, self.windowHeight//3+130))

    def Event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()

    def mainLoop(self) -> None:

        self.window.fill(self.backGround, rect=None, special_flags=0)

        self.displayPlayer()
        if self.host:
            Button(self.window, pygame.Rect(
                self.windowWidth//2-150, self.windowHeight*0.60, 300, 80), self.lighterBlue, "Start")
            Button(self.window, pygame.Rect(
                self.windowWidth//2-150, self.windowHeight*0.75, 300, 80), self.lighterBlue, "Refresh")
        self.Event()
        pygame.display.flip()
        if self.start == False:
            try:
                # This will now return immediately if there is no data to receive
                self.start = self.serverConnection.multiLaunch(self.startvars)
            except BlockingIOError:
                # No data to receive yet
                pass
            except Exception as e:
                # Handle other exceptions
                print("Unexpected error:", e)


if __name__ == "__main__":
    pygame.init()

    board = WaitingRoom(5, 4, 4, 0, "toto", True)
    while True:
        board.mainLoop()
