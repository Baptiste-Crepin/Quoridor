import pickle
import socket
import sys

from Bot import Bot
from Player import Player
from Table import Board
from localGame import LocalGame
from threadClient import Thread_client

DISCOVERY_MSG = b"SERVER_DISCOVERY_REQUEST"

def discovery():
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    discoSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discoSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    serveurs = discover(discoSock)
    print("Available servers:")
    print(serveurs)
    choix = int(input("pick a server"))
    try:
        connexion.connect((serveurs[choix]['ip'], serveurs[choix]['port']))
        print("Connexion active")
    except socket.error:
        print("Erreur sur la connection")
        sys.exit()
    start = False
    while start == False:

        serverMessage = connexion.recv(4096)
        startVars = pickle.loads(serverMessage)

        serverMessage = connexion.recv(4096)
        unpickeled_message = pickle.loads(serverMessage)

        print(unpickeled_message)
        if unpickeled_message == True:
            print("starting game")
            createGame(connexion,startVars)
        else:
            print("waiting for server start")






def discover(discoSock):
    discoSock.sendto(DISCOVERY_MSG, ('<broadcast>', 5555))
    discoSock.settimeout(5.0)  # Set a timeout of 5 seconds for waiting for responses
    result = list()
    serverList = list()

    try:
        data, _ = discoSock.recvfrom(1024)
        try:
            server_info = pickle.loads(data)
        except pickle.UnpicklingError:
            print("Received a non-Python object.")

        serverList.append(server_info)
        print("Server info:", server_info)
    except socket.timeout:
        print('request timed out / no server found')
    for server in serverList:
        result.append(server)
    return result
class MultiplayerGame(LocalGame):
    def __init__(self, connexion, width, nbBarrier, nbPlayer, nbBots=0, num=-1) -> None:
        super().__init__(width, nbPlayer, nbBarrier, nbBots)
        self.board = Board(self.game.getSquareWidth(), num)
        self.num = num
        self.thread = Thread_client(connexion, self)

    def displayPossibleMoves(self, player: Player):
        self.board.clearAllHighlight()
        if ((not isinstance(player, Bot) or player.getNumber() == self.num + 1) and
                (self.game.getCurrentPlayer().getNumber() == self.num + 1)):
            self.highlightPlayer(player)
            self.highlightBarrier()

    def placement(self, currentPlayer: Player):
        if isinstance(currentPlayer, Bot) and self.num == 0:
            self.board.newFrame(currentPlayer)
            currentPlayer.randomMoves(self.game)
            print("Bot played")
            self.thread.emet()
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
        self.highlightPlayer(currentPlayer)
        self.highlightBarrier()
        ("tour fini pour " + str(self.num))
        self.thread.emet()

def createGame(connexion, startVars):
    
    print("Game infos:", startVars)
    num = int(startVars[0])
    width = startVars[1]
    nbBarrier = startVars[2]
    nbPlayer = startVars[3]
    nbBots = startVars[4]

    Game = MultiplayerGame(connexion, width, nbBarrier, nbPlayer, nbBots, num)
    Game.mainLoop()

if __name__ == "__main__":
    # TODO: remove this when cleaning up for final version
    # temporary localhost for testing purposes
    #hostname = socket.gethostname()
    #host = socket.gethostbyname(hostname)
    # host = '192.168.1.10'
    #port = 45678

    connexion = discovery()


