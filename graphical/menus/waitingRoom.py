from typing import Any

import pygame

from gameLogic.player import Player
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from multi.discoveryServer import SearchServer


class WaitingRoom(Menu):

    def __init__(self, startVars: list[Any], width: int, nbPlayer: int, nbBarrier: int, nbBot: int,
                 server_instances_queue, serverName: str,
                 connectedPlayers: int,
                 serverConnection: SearchServer, Host: bool = False, fullScreen: bool = False) -> None:
        super().__init__(fullScreen)
        self.width = width
        self.nbPlayer = nbPlayer
        self.nbBarrier = nbBarrier
        self.nbBot = nbBot
        self.serverName = serverName
        self.serverConnection = serverConnection
        self.host = Host
        self.start = False
        self.startVars = startVars
        self.serverConnection.connection.setblocking(False)
        self.server_instances_queue = server_instances_queue
        self.clientListLen = connectedPlayers

    def playerCoordX(self, i: int) -> int:
        return (self.fullScreenWidth // (self.nbPlayer+1)) * (i) + (self.fullScreenWidth // (self.nbPlayer+1))

    def textPlayerCoordX(self, i: int) -> int:
        return self.playerCoordX(i)-70

    def displayPlayer(self) -> None:
        for i in range(self.nbPlayer):
            if self.clientListLen - 1 >= i:
                pygame.draw.circle(self.window, Player(i + 1).getColor(
                ), (self.playerCoordX(i), self.windowHeight // 3), 70)
                font = pygame.font.SysFont(
                    "Extra Bold Italic", 60, False, True)
                player = font.render(f"player {str(i + 1)}", True, self.white)
                self.window.blit(
                    player, (self.textPlayerCoordX(i), self.windowHeight // 3 + 80))
            else:
                pygame.draw.circle(self.window, Player(i + 1).getColor(
                ), (self.playerCoordX(i), self.windowHeight // 3), 70, 10)
                font = pygame.font.SysFont(
                    "Extra Bold Italic", 60, False, True)
                wait = font.render(
                    "waiting for", True, self.white)
                player = font.render(f"player {str(i + 1)}", True, self.white)
                self.window.blit(
                    wait, (self.textPlayerCoordX(i)-35, self.windowHeight // 3 + 80))
                self.window.blit(
                    player, (self.textPlayerCoordX(i), self.windowHeight // 3 + 130))

    def handle_start_button_press(self):
        # Check if this is a host and if the server instances are available in the queue
        if self.host and self.server_instances_queue is not None and not self.server_instances_queue.empty():
            # Get the server instances
            serverInstances = self.server_instances_queue.get()

            # Call the desired method on the server instance(s)
            if serverInstances:
                serverInstances[0].starter(serverInstances[0].connected)
        else:
            print("Waiting for server to be ready...")

    def Event(self) -> None:
        for event in pygame.event.get():
            self.defaultEventHandler(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                buttonX = self.windowWidth // 2 - 150
                buttonY = self.windowHeight * 0.60
                buttonWidth = 300
                buttonHeight = 80

                if buttonX <= mousePos[0] <= buttonX + buttonWidth and buttonY <= mousePos[
                        1] <= buttonY + buttonHeight:
                    self.handle_start_button_press()

    def mainLoop(self) -> None:
        self.window.fill(self.backGround, rect=None, special_flags=0)

        self.displayPlayer()
        if self.host:
            Button(self.window, pygame.Rect(
                self.windowWidth // 2 - 150, self.windowHeight * 0.60, 300, 80), self.lighterBlue, "Start")
        self.Event()
        pygame.display.flip()
        if self.start == False:
            try:
                # This will now return immediately if there is no data to receive
                self.start, self.clientListLen = self.serverConnection.multiLaunch(self.startVars, self.clientListLen,
                                                                                   self.host, self)
            except Exception as e:
                print("Unexpected error:", e)
            # Handle other exceptions
