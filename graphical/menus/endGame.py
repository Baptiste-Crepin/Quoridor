import pygame
from player import Player
from Play import Play
from graphical.widgets.button import Button
from graphical.widgets.menu import Menu


class End(Menu):
    def __init__(self, curentPlayer: Player, width: int, nbPlayer: int, nbBarrier: int, nbBots: int, score: list[int] = [0, 0, 0, 0]):
        super().__init__()
        self.curentplayer = curentPlayer
        self.width = width
        self.nbPlayer = nbPlayer
        self.nbBarrier = nbBarrier
        self.nbBots = nbBots
        self.windowWidth = 1330
        self.windowHeight = 750
        self.window = pygame.display.set_mode(
            size=(self.windowWidth, self.windowHeight))
        self.center = (self.windowWidth//2, self.windowHeight//2)
        self.countPlayers1 = score[0]
        self.countPlayers2 = score[1]
        self.countPlayers3 = score[2]
        self.countPlayers4 = score[3]
        self.score = score
        self.actualizeScore()
        self.coordQuit = pygame.Rect(self.windowWidth//2-110,
                                     self.windowHeight//2+250, 200, 80)
        self.coordReplay = pygame.Rect(self.windowWidth//2-220,
                                       self.windowHeight//2+150, 200, 80)
        self.coordLobby = pygame.Rect(self.windowWidth//2+20,
                                      self.windowHeight//2+150, 200, 80)

    def Winner(self) -> str:
        return f"{self.curentplayer.stringColor()} Player won ! {self.score[self.curentplayer.getNumber()-1]} win(s)"

    def actualizeScore(self):
        self.score[self.curentplayer.getNumber()-1] += 1
        return self.score

    def displayWinner(self) -> None:
        pygame.draw.circle(
            self.window, self.curentplayer.getColor(), self.center, 100)

    def Event(self):
        for event in pygame.event.get():
            from localGame import LocalGame
            self.defaultEventHandler(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(self.coordLobby).collidepoint(event.pos):
                    board = Play()
                    self.newMenu(self, board)
                elif pygame.Rect(self.coordReplay).collidepoint(event.pos):
                    board = LocalGame(
                        self.width, self.nbPlayer, self.nbBarrier, self.nbBots, self.score)
                    self.newMenu(self, board)
                elif pygame.Rect(self.coordQuit).collidepoint(event.pos):
                    raise SystemExit

    def mainLoop(self):

        self.window.fill(self.backGround)
        text_surface = self.font.render(self.Winner(), True, self.white)
        text_rect = text_surface.get_rect(center=(self.windowWidth // 2, 100))
        self.window.blit(text_surface, text_rect)
        self.displayWinner()
        Button(self.window, self.coordLobby, self.blue, "LOBBY")
        Button(self.window, self.coordQuit, self.blue, "QUIT")
        Button(self.window, self.coordReplay, self.blue, "REPLAY")
        self.Event()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    board = End(Player(0, 4), 5, 2, 10, 0, [0, 0, 0, 0])

    while True:
        board.mainLoop()
        pygame.display.update()
