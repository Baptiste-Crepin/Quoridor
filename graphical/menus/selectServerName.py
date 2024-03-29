import queue
import random
import socket
import threading
import time

import pygame

from graphical.widgets.button import Button
from graphical.widgets.input import Input
from graphical.widgets.menu import Menu
from multi.discoveryServer import SearchServer
from multi.multiplayerServer import createServer


class ServerName(Menu):
    def __init__(self, width: int, nbPlayer: int, nbBarrier: int, nbBot: int, method: int, fullScreen: bool = False) -> None:
        super().__init__(fullScreen)
        self.startVars = []
        self.width = width
        self.nbPlayer = nbPlayer
        self.nbBarrier = nbBarrier
        self.nbBot = nbBot
        self.method = method
        self.server_instances_queue = queue.Queue()

    def calculateElements(self):
        self.sendPos = (self.buttonX, 500)
        self.sendRect = pygame.Rect(self.sendPos, self.buttonSize)
        self.inputPos = (self.buttonX, 400)
        self.input = Input(self.window, pygame.Rect(self.inputPos, self.inputSize), self.white)

        self.searchServer = SearchServer()

    def run_server(self, startingPlayer: int):
        serverInstances = createServer(self.width,
                                       self.nbBarrier,
                                       self.nbPlayer,
                                       self.nbBot,
                                       self.input.text,
                                       startingPlayer
                                       )
        # Put the serverInstances in the Queue
        self.server_instances_queue.put(serverInstances)

    def launch_server(self):
        startingPlayer = random.randint(0, self.nbPlayer - 1)

        threading.Thread(target=self.run_server,
                         args=(startingPlayer,)).start()
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
                    host = SearchServer.getSelfHost()

                    self.startVars = self.searchServer.connect(host, 45678)
                    print("Self connect to", socket.gethostbyname(
                        socket.gethostname()))

                    board = WaitingRoom(self.startVars,
                                        self.width,
                                        self.nbPlayer,
                                        self.nbBarrier,
                                        self.nbBot,
                                        self.server_instances_queue,
                                        self.input.text,
                                        0,
                                        self.searchServer,
                                        True,
                                        self.fullScreen)
                    self.newMenu(self, board)
                    print("D")

                self.back.Event(event, self, selectBarrier, (self.nbPlayer,
                                                             self.nbBot,
                                                             self.width,
                                                             self.method,
                                                             True, self.fullScreen))
                print("E")

    def mainLoop(self):
        self.window.fill(self.backGround, rect=None, special_flags=0)
        font = pygame.font.SysFont(
            "Extra Bold Italic", 60, False, True)
        text = font.render(
            "chose the name of", True, self.white)
        secondText = font.render(
            "the server", True, self.white)
        self.input.createInput()
        self.window.blit(text, (self.buttonWidth, 230))
        self.window.blit(secondText, (self.buttonWidth, 270))

        Button(self.window, self.sendRect, self.lighterBlue, "send", 40, 10)

        self.Event()
        pygame.display.flip()
