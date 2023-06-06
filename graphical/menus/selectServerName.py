import pygame
import time
import sys
import threading
from graphical.widgets.input import Input
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu

from multiplayerServer import createServer
from multiplayerClient import SearchServer


class ServerName(Menu):
    def __init__(self, width: int, nbPlayer: int, nbBarrier: int, nbBot: int, method: int) -> None:
        super().__init__()
        self.width = width
        self.nbPlayer = nbPlayer
        self.nbBarrier = nbBarrier
        self.nbBot = nbBot
        self.method = method

        self.sendPos = (self.buttonX, 500)
        self.buttonSize = (self.buttonWidth, 50)

        self.sendRect = pygame.Rect(
            self.sendPos, self.buttonSize)

        self.inputPos = (self.buttonX, 400)
        self.input = Input(self.window, pygame.Rect(
            self.inputPos, self.buttonSize), self.white)

        self.searchServer = SearchServer()

    def run_server(self):
        createServer(self.width,
                     self.nbBarrier,
                     self.nbPlayer,
                     self.nbBot,
                     self.input.text)

    def run_client(self):
        serverList = self.searchServer.discover()
        self.searchServer.connect(serverList[0]["ip"], serverList[0]["port"])
        print("Self connect to", serverList[0]["lobbyName"])

    def launch_server(self):

        server_thread = threading.Thread(target=self.run_server)
        client_thread = threading.Thread(target=self.run_client)

        server_thread.start()
        # wait for server to start before connecting the client
        time.sleep(0.5)
        client_thread.start()

    def Event(self):
        from graphical.menus.choiceBarrier import selectBarrier
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
            self.input.Event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.sendRect.collidepoint(event.pos):
                    if self.input.text != "":
                        from multiplayerServer import createServer
                        from graphical.menus.waitingRoom import WaitingRoom
                        self.launch_server()
                        time.sleep(2)
                        board = WaitingRoom(self.width, self.nbPlayer, self.nbBarrier,
                                            self.nbBot, self.input.text, self.searchServer, True)
                        while True:
                            board.mainLoop()
                            pygame.display.update()
                self.back.Event(event, selectBarrier, (self.nbPlayer,
                                self.nbBot, self.width, self.method, True))

    def mainLoop(self):
        self.window.fill(self.blue, rect=None, special_flags=0)
        font = pygame.font.SysFont(
            "Extra Bold Italic", 60, False, True)
        text = font.render(
            "chose the name of", True, self.white)
        secondtext = font.render(
            "the server", True, self.white)
        self.input.createInput()
        self.window.blit(text, (self.buttonWidth, 230))
        self.window.blit(secondtext, (self.buttonWidth, 270))

        Button(self.window, self.sendRect, self.lighterBlue, "send", 40, 10)

        self.Event()
        pygame.display.flip()
