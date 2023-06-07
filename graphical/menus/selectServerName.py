import pygame
import time
import threading
from graphical.widgets.input import Input
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu

from multi.multiplayerServer import createServer
from multi.multiplayerClient import SearchServer


class ServerName(Menu):
    def __init__(self, width: int, nbPlayer: int, nbBarrier: int, nbBot: int, method: int) -> None:
        super().__init__()
        self.startVars = []
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

    def launch_server(self):

        server_thread = threading.Thread(target=self.run_server)

        server_thread.start()
        # wait for server to start before connecting the client
        time.sleep(0.5)

    def Event(self):
        from graphical.menus.choiceBarrier import selectBarrier
        for event in pygame.event.get():
            self.defaultEventHandler(event)
            self.input.Event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.sendRect.collidepoint(event.pos) and self.input.text != "":
                    from graphical.menus.waitingRoom import WaitingRoom
                    self.launch_server()
                    time.sleep(2)
                    serverList = self.searchServer.discover()
                    self.startVars = self.searchServer.connect(serverList[0]["ip"],
                                                               serverList[0]["port"])
                    print("Self connect to", serverList[0]["lobbyName"])

                    board = WaitingRoom(self.startVars,
                                        self.width,
                                        self.nbPlayer,
                                        self.nbBarrier,
                                        self.nbBot,
                                        self.input.text,
                                        self.searchServer,
                                        True)
                    self.newMenu(self, board)

                self.back.Event(event, self, selectBarrier, (self.nbPlayer,
                                                             self.nbBot,
                                                             self.width,
                                                             self.method,
                                                             True))

    def mainLoop(self):
        self.window.fill(self.backGround, rect=None, special_flags=0)
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
