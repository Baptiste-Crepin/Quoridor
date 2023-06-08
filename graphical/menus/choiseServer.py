import pygame
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu
from player import Player


class choiseServer(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.server = []
        self.serverList = [
            {"serverName": "toto", "ip": "193.98.55",
                "port": 332, "players": 2, "remining": 1},
            {"serverName": "titi", "ip": "193.98.55",
                "port": 332, "players": 4, "remining": 3},
            {"serverName": "on s'en fou", "ip": "193.98.55",
                "port": 332, "players": 2, "remining": 1},
            {"serverName": "titi", "ip": "193.98.55",
                "port": 332, "players": 4, "remining": 3},
            {"serverName": "titi", "ip": "193.98.55",
                "port": 332, "players": 4, "remining": 3},
            {"serverName": "titi", "ip": "193.98.55",
                "port": 332, "players": 4, "remining": 3},
            {"serverName": "tutu", "ip": "193.98.55",
                "port": 332, "players": 4, "remining": 2},
        ]
        self.serverPosition = 0

    def coordYServer(self, i: int) -> int:
        return 220*i+70+self.serverPosition

    def heightServerRect(self) -> int:
        return 220*len(self.serverList)+20

    def displayServer(self) -> None:
        pygame.draw.rect(self.window, self.lighterBlue,
                         (50, 50+self.serverPosition, 640, self.heightServerRect()), border_radius=5)

        for i in range(len(self.serverList)):
            dico = {2: 630, 4: 420}
            pygame.draw.rect(self.window, self.black, (70, self.coordYServer(i), 600, 200),
                             border_radius=10)
            font = pygame.font.SysFont(
                "Extra Bold Italic", 60, False, True)
            serverName = font.render(
                self.serverList[i]["serverName"], True, self.white)
            # textSlot = "Slots remining : "+str(self.serverList[i]["player"])
            # reminingSlots = font.render(textSlot, True, self.white)
            self.window.blit(serverName, (70, self.coordYServer(i)+10))
            # self.window.blit(reminingSlots, (230, self.coordYServer(i)+80))
            for j in range(self.serverList[i]["players"]):
                if j < self.serverList[i]["players"]-self.serverList[i]["remining"]:
                    pygame.draw.circle(self.window, Player(j+1).getColor(),
                                       (70*j+dico[self.serverList[i]["players"]], self.coordYServer(i)+160), 25)
                elif j >= self.serverList[i]["players"]-self.serverList[i]["remining"]:
                    pygame.draw.circle(self.window, Player(j+1).getColor(),
                                       (70*j+dico[self.serverList[i]["players"]], self.coordYServer(i)+160), 25, 5)

    def Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()

            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0 and self.serverPosition > -(self.heightServerRect()-450):
                    self.serverPosition -= 50
                elif event.y > 0 and self.serverPosition < 0:
                    self.serverPosition += 50

    def setwindow(self) -> None:
        self.window.fill(self.darkBlue, rect=None, special_flags=0)
        self.displayServer()
        Button(self.window, pygame.Rect(
            900, 50, 300, 100), self.lighterBlue, "Refresh")

        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    board = choiseServer()
    while True:
        board.setwindow()  # type: ignore