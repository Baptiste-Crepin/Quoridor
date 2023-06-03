import pygame
from button import Button


class choiseServer():
    def __init__(self) -> None:
        self.server = []
        self.serverList = [
            {"serverName": "toto", "ip": "193.98.55", "port": 332, "player": 4},
            {"serverName": "titi", "ip": "193.98.55", "port": 332, "player": 3},
            {"serverName": "on s'en fou", "ip": "193.98.55", "port": 332, "player": 3},
            {"serverName": "titi", "ip": "193.98.55", "port": 332, "player": 3},
            {"serverName": "titi", "ip": "193.98.55", "port": 332, "player": 3},
            {"serverName": "titi", "ip": "193.98.55", "port": 332, "player": 3},
            {"serverName": "tutu", "ip": "193.98.55", "port": 332, "player": 2}
        ]
        self.width = 500
        self.height = 700
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Quoridor")
        self.white = pygame.Color(255, 255, 255)
        self.grey = pygame.Color(217, 217, 217, 35)
        self.black = pygame.Color(0, 0, 0)
        self.darkBlue = pygame.Color(0, 0, 48)
        self.lightBlue = pygame.Color(90, 173, 255)
        self.purple = pygame.Color(204, 0, 204)
        self.font = pygame.font.Font(None, 36)
        self.serverPosition = 0

    def coordYServer(self, i: int) -> int:
        return 120*i+70+self.serverPosition

    def heightServerRect(self) -> int:
        return 120*len(self.serverList)+20

    def displayServer(self) -> None:
        pygame.draw.rect(self.window, self.lightBlue,
                         (50, 50+self.serverPosition, 400, self.heightServerRect()), border_radius=5)

        for i in range(len(self.serverList)):

            pygame.draw.rect(self.window, self.black, (70, self.coordYServer(i), 360, 100),
                             border_radius=10)
            font = pygame.font.SysFont(
                "Extra Bold Italic", 30, False, True)
            serverName = font.render(
                self.serverList[i]["serverName"], True, self.white)
            textSlot = "Slots remining : "+str(self.serverList[i]["player"])
            reminingSlots = font.render(textSlot, True, self.white)
            self.window.blit(serverName, (70, self.coordYServer(i)+10))
            self.window.blit(reminingSlots, (230, self.coordYServer(i)+80))

        pygame.draw.rect(self.window, self.darkBlue, (0, 500, 500, 200))

    def Event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and self.serverPosition > -(self.heightServerRect()-450):
                    self.serverPosition -= 50
                elif event.y < 0 and self.serverPosition < 0:
                    self.serverPosition += 50

    def setwindow(self) -> None:
        self.window.fill(self.darkBlue, rect=None, special_flags=0)
        self.displayServer()
        Button(self.window, pygame.Rect(
            100, 550, 300, 100), self.lightBlue, "Refresh")

        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    board = choiseServer()
    while True:
        board.setwindow()
