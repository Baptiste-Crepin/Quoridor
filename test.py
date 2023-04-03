import socket
import threading
from client import Network
from game import Game
from Table import Board
from main import GraphicalGame
if __name__ == "__main__":
    # width = int(input('Width'))
    # nbPlayer = int(input('Nb Player'))
    # nbBarrier = int(input('Nb barrier'))
    width = 5
    nbBarrier = 4
    nbPlayer = 4
    G = GraphicalGame(width, nbPlayer, nbBarrier)
    G.mainLoop()