import pygame

from gameLogic.player import Player
from graphical.menus.choiceHost import ChoiceHost
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from multi.discoveryServer import SearchServer


class ChoiceServer(Menu):
    def __init__(self, fullScreen: bool = False) -> None:
        super().__init__(fullScreen)
        self.searchServer = SearchServer()
        self.startvars = list[int]()
        self.serverList = self.searchServer.discover()
        print(self.serverList)
        self.serverPosition = 0
        self.serverPositions = list[pygame.Rect]()

    def calculateElements(self) -> None:
        self.refreshWidth = self.buttonWidth//2
        self.refreshPos = (self.windowWidth*0.9 -
                           self.refreshWidth//2, self.windowHeight*0.05)
        self.refresh = pygame.Rect(
            self.refreshPos, (self.refreshWidth, self.buttonHeight))

    def coordYServer(self, i: int) -> int:
        return 220 * i + 70 + self.serverPosition

    def heightServerRect(self) -> int:
        return 220 * len(self.serverList) + 20

    def displayServer(self) -> None:
        self.serverPositions = list[pygame.Rect]()
        if len(self.serverList) == 0:
            font = pygame.font.SysFont(
                "Extra Bold Italic", 60, False, True)
            serverName = font.render(
                "No server found", True, self.white)
            self.window.blit(serverName, (70, 70 + self.serverPosition))
            return

        pygame.draw.rect(self.window, self.lighterBlue,
                         (50, 50 + self.serverPosition, 640, self.heightServerRect()), border_radius=5)
        for i in range(len(self.serverList)):
            dico = {2: 560, 3: 490, 4: 420}
            pygame.draw.rect(self.window, self.black, (70, self.coordYServer(i), 600, 200),
                             border_radius=10)
            font = pygame.font.SysFont(
                "Extra Bold Italic", 60, False, True)
            serverName = font.render(
                self.serverList[i]["lobbyName"], True, self.white)
            sizeGrid = font.render(
                str(self.serverList[i]["width"]) + "X" + str(self.serverList[i]["width"]), True, self.white)
            self.window.blit(serverName, (80, self.coordYServer(i) + 10))
            self.window.blit(sizeGrid, (80, self.coordYServer(i) + 150))

            for j in range(self.serverList[i]["players"]):
                if self.serverList[i]["connectedPlayers"] - 1 >= j:
                    # if j > (self.serverList[i]["players"] - self.serverList[i]["connectedPlayers"]):
                    pygame.draw.circle(self.window, Player(j + 1).getColor(),
                                       (70 * j + dico[self.serverList[i]["players"]], self.coordYServer(i) + 160), 25)
                else:
                    pygame.draw.circle(self.window, Player(j + 1).getColor(),
                                       (70 * j + dico[self.serverList[i]["players"]],
                                        self.coordYServer(i) + 160), 25,
                                       5)

            self.serverPositions.append(pygame.Rect(
                70, self.coordYServer(i), 600, 200))

    def Event(self):
        from graphical.menus.waitingRoom import WaitingRoom
        for event in pygame.event.get():
            self.defaultEventHandler(event)
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0 and self.serverPosition > -(self.heightServerRect() - 450):
                    self.serverPosition -= 50
                elif event.y > 0 and self.serverPosition < 0:
                    self.serverPosition += 50
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.refresh.collidepoint(event.pos):
                    self.serverList = self.searchServer.discover()
                for i, server in enumerate(self.serverPositions):
                    if server.collidepoint(event.pos):
                        self.startvars = self.searchServer.connect(self.serverList[i]["ip"],
                                                                   self.serverList[i]["port"])
                        board = WaitingRoom(self.startvars,
                                            self.serverList[i]["width"],
                                            self.serverList[i]["players"],
                                            self.serverList[i]["barriers"],
                                            self.serverList[i]["bots"],
                                            None,  # server_instances_queue is None for non-host client
                                            self.serverList[i]["lobbyName"],
                                            self.serverList[i]["connectedPlayers"],
                                            self.searchServer,
                                            False,
                                            self.fullScreen)
                        self.newMenu(self, board)
                self.back.Event(event, self, ChoiceHost, self.fullScreen)

    def mainLoop(self) -> None:
        self.window.fill(self.backGround, rect=None, special_flags=0)
        self.displayServer()
        Button(self.window, self.refresh, self.lighterBlue, "Refresh")
        self.back.drawButton()

        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    board = ChoiceServer()
    while True:
        board.mainLoop()
