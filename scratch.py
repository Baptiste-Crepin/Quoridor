from game import Game
from Table import Board
from Bot import Bot
from Player import Player
import socket, sys, threading, pickle


class GraphicalGame():
    def __init__(self, width, nbPlayer, nbBarrier, nbBots=0, num=0) -> None:
        self.game = Game(width, nbPlayer, nbBarrier, nbBots, num)
        self.board = Board(self.game.getSquareWidth(),num)
        self.num = num
        print("NUM",num)

    def highlightPlayer(self, player: Player):
        for PossibleMoveCoordo in self.game.possibleMoves(player.getCoordinates()):
            self.board.rect[PossibleMoveCoordo[1]
                            ][PossibleMoveCoordo[0]].highlighted = True

    def highlightBarrier(self):
        for (possibleBarrierCoordo, direction) in self.game.possibleBarrierPlacement(self.game.getCurrentPlayer()):
            if direction == 'Right':
                self.board.Vbarriers[possibleBarrierCoordo[1]
                                     ][possibleBarrierCoordo[0]].possiblePlacement = True

            if direction == 'Down':
                self.board.Hbarriers[possibleBarrierCoordo[1]
                                     ][possibleBarrierCoordo[0]].possiblePlacement = True

    def displayPossibleMoves(self, player: Player):
        self.board.clearAllHighlight()
        if ((not isinstance(player, Bot) or player.getNumber() == self.num+1) and
            (self.game.getCurrentPlayer().getNumber() == self.num+1)):
            self.highlightPlayer(player)
            self.highlightBarrier()
    def actualizeGame(self):
        for i, row in enumerate(self.game.getGrid()):
            for j, cell in enumerate(row):

                self.board.rect[j][i].player = cell.getPlayer()

                if i < len(self.game.getGrid()) - 1:
                    self.board.Hbarriers[j][i].placed = cell.getWalls()['Down']

                if j < len(row) - 1:
                    self.board.Vbarriers[j][i].placed = cell.getWalls()[
                        'Right']

    def placement(self, currentPlayer: Player):
        if isinstance(currentPlayer, Bot) and self.num == 0:
            print(type ( currentPlayer))
            self.board.newFrame(currentPlayer)
            currentPlayer.randomMoves(self.game)
            print(" bot play")
            th.emet()
            return
        event = self.board.handleEvents(currentPlayer)
        if not event:
            return

        (action, x, y) = event
        clickCoordo = (x, y)


        if action == 'TablePlayer':
            if clickCoordo not in self.game.possibleMoves(currentPlayer.getCoordinates()):
                return
            self.board.clearHover(self.board.rect)
            self.game.movePlayer(currentPlayer, clickCoordo)

        if action == 'VerticalBarrier':
            if (clickCoordo, 'Right') not in self.game.possibleBarrierPlacement(currentPlayer):
                return
            self.game.placeWall(clickCoordo, 'Right', currentPlayer, place=True)

        if action == 'HorrizontalBarrier':
            if (clickCoordo, 'Down') not in self.game.possibleBarrierPlacement(currentPlayer):
                return
            self.game.placeWall(clickCoordo, 'Down', currentPlayer)

        self.board.clearAllHighlight()
        #self.game.nextPlayer()
        self.highlightPlayer(currentPlayer)
        self.highlightBarrier()

        print("tour fini pour " + str(num))
        th.emet()

    def mainLoop(self) -> None:
        self.highlightPlayer(self.game.getCurrentPlayer())
        self.highlightBarrier()
        while self.board.play:
            while not self.game.checkGameOver():
                self.displayPossibleMoves(G.game.getCurrentPlayer())
                self.placement(G.game.getCurrentPlayer())
                self.actualizeGame()
                self.board.newFrame(G.game.getCurrentPlayer())
            # TODO: Game has ended. display the end screen
            self.board.newFrame()

# --------------------------------------------------------


class Thread_client(threading.Thread):
    def __init__(self, c):
        threading.Thread.__init__(self)
        self.connexion = c
        self.start()

    def run(self):
        while 1:
            data = self.reco()
            print("R")
            #print( type(data))
            if type(data) is list:
                print("reciev:",data)
                G.game.setGrid(data)
                #G.actualizeGame()
                #G.board.newFrame()
                #G.nextPlayer
            else:

                G.game.setCurrentPlayerN(data)
                G.game.setCurrentPlayer(G.game.getPlayerList()[data])
                print("reciev:",data)

        #self.connexion.close()

    def emet(self):
        gr = G.game.getGrid()
        data = pickle.dumps(gr)
        self.connexion.send(data)
        #self.connexion.send(msg.encode("Utf8"))
        #self.connexion.close()
    def reco(self):
        dump = self.connexion.recv(4096)
        message = pickle.loads(dump)
        return message


if __name__ == "__main__":
    # width = int(input('Width'))
    # nbPlayer = int(input('Nb Player'))
    # nbBarrier = int(input('Nb barrier'))
    #width = 5
    #nbBarrier = 4
    #nbPlayer = 2
    # client avec Thread


    # ============================================================
    hostname = socket.gethostname()

    host = socket.gethostbyname(hostname)
    #host = '10.128.173.35'
    port = 45678

    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((host, port))
        print("Connexion active")
    except socket.error:
        print("Erreur sur la connection")
        sys.exit()

    msg = connexion.recv(4096)
    msg = pickle.loads(msg)
    print("reccu:",msg)
    width = msg[1]
    nbBarrier = msg[2]
    nbPlayer = msg[3]
    nbBots = msg[4]


    num = int(msg[0])

    th = Thread_client(connexion)


    # =========================================================

    G = GraphicalGame(width, nbPlayer, nbBarrier, nbBots, num)
    G.mainLoop()
