import random
from Player import Player
from Case import Case
from Bot import Bot


class Jeu():
    def __init__(self, width: int, nbPlayers: int) -> None:
        self.__squareWidth = self.validWidth(width)
        self.__grid = self.createGrid()
        self.__NumberOfPlayers = self.validNumberOfPlayers(nbPlayers)
        self.__PlayerList = self.createPlayerList()
        self.__currentPlayerN = random.randint(0, self.getNumberOfPlayers()-1)
        self.__currentPlayer = self.getPlayerList()[self.getCurrentPlayerN()]

        self.initializePawns()

    def validWidth(self, n: int, min: int = 5, max: int = 11) -> int:
        if n % 2 == 0:
            print("You mush set an odd width")
            n += 1
        if n < min:
            print(
                f"The minimal width is {min}, the width has been increased")
            n = min
        if n > max:
            print(
                f"The maximal width is {max}, the width has been decreased")
            n = max
        return n

    def validNumberOfPlayers(self, n: int, min: int = 2, max: int = 4) -> int:
        if n % 2 == 1:
            print("You mush set an even amount of players")
            n -= 1
        if n < min:
            print(
                f"The amount of players must not be greater than {min}, it has automatically been increased")
            n = min
        if n > max:
            print(
                f"The amount of players must exceed {max}, it has automatically been increased")
            n = max
        return n

    def getSquareWidth(self) -> int:
        return self.__squareWidth

    def getGrid(self) -> list:
        return self.__grid

    def getNumberOfPlayers(self) -> int:
        return self.__NumberOfPlayers

    def getNumberOfBots(self) -> int:
        return self.__NumberOfBots

    def getPlayerList(self) -> int:
        return self.__PlayerList

    def getCurrentPlayerN(self) -> int:
        return self.__currentPlayerN

    def getCurrentPlayer(self) -> Player:
        return self.__currentPlayer

    def setSquareWidth(self, value: int) -> None:
        self.__squareWidth = value

    def setGrid(self, value: list) -> None:
        self.__grid = value

    def setNumberOfPlayers(self, value: int) -> None:
        self.__NumberOfPlayers = value

    def setNumberOfBots(self, value: int) -> None:
        self.__NumberOfBots = value

    def setPlayerList(self, value: list) -> None:
        self.__PlayerList = value

    def setCurrentPlayerN(self, value: int) -> None:
        self.__currentPlayerN = value

    def setCurrentPlayer(self, value: Player) -> None:
        self.__currentPlayer = value

    def createGrid(self) -> list:
        return [[Case(0, (y, x), Player(0)) for x in range(self.getSquareWidth())]
                for y in range(self.getSquareWidth())]

    def placePlayer(self, player: Player, coordinates: tuple) -> None:
        self.getGrid()[coordinates[0]][coordinates[1]].setPlayer(player)
        player.setCoordinates((coordinates[0], coordinates[1]))

    def initializePawns(self) -> None:
        grid = self.getGrid()

        self.placePlayer(self.getPlayerList()[
                         0], (0, self.getSquareWidth()//2))
        self.placePlayer(self.getPlayerList()[
                         1], (self.getSquareWidth()-1, self.getSquareWidth()//2))

        if self.getNumberOfPlayers() == 4:
            self.placePlayer(self.getPlayerList()[
                             2], (self.getSquareWidth()//2, 0))
            self.placePlayer(self.getPlayerList()[
                             3], (self.getSquareWidth()//2, self.getSquareWidth()-1))

        self.setGrid(grid)

    def createPlayerList(self) -> list[Player]:
        return [Player(x+1) for x in range(self.getNumberOfPlayers())]

    def display(self) -> None:
        for r, row in enumerate(self.getGrid()):
            for i in range(3):
                for c, cell in enumerate(row):
                    if i == 0:
                        if self.getGrid()[r][c].getWalls()["Up"] == 0:
                            print("   ", end="")
                        else:
                            print(" - ", end="")
                    elif i == 1:
                        if cell.getWalls()["Left"] == 0:
                            print(" ", end="")
                        else:
                            print("|", end="")
                        print(cell, end="")
                        if cell.getWalls()["Right"] == 0:
                            print(" ", end="")
                        else:
                            print("|", end="")
                    elif i == 2:
                        if self.getGrid()[r][c].getWalls()["Down"] == 0:
                            print("   ", end="")
                        else:
                            print(" - ", end="")
                print()

    def inGrid(self, coord: tuple) -> bool:
        return not (coord[0] < 0 or
                    coord[1] < 0 or
                    coord[0] >= self.getSquareWidth() or
                    coord[1] >= self.getSquareWidth())

    def getNeighbours(self, coord: tuple) -> list[Case]:
        neighbours = []

        if coord[0]-1 >= 0:
            neighbours.append(self.getCell((coord[0]-1, coord[1])))

        if coord[1]-1 >= 0:
            neighbours.append(self.getCell((coord[0], coord[1]-1)))

        if coord[0]+1 < self.getSquareWidth():
            neighbours.append(self.getCell((coord[0]+1, coord[1])))

        if coord[1]+1 < self.getSquareWidth():
            neighbours.append(self.getCell((coord[0], coord[1]+1)))

        return neighbours

    def numberOfNeighbours(self, coord: tuple) -> int:
        return len(self.getNeighbours(coord))

    def getCell(self, coord: tuple) -> Case:
        return self.getGrid()[coord[0]][coord[1]]

    def playerInGrid(self, player: Player) -> bool:
        for row in self.getGrid():
            for cell in row:
                if cell.getPlayer().getNumber() == player.getNumber():
                    return True

        return False

    def NextPlayer(self) -> None:
        if self.getCurrentPlayerN() < len(self.getPlayerList())-1:
            self.setCurrentPlayerN(self.getCurrentPlayerN() + 1)
        else:
            self.setCurrentPlayerN(0)

        self.setCurrentPlayer(self.getPlayerList()[self.getCurrentPlayerN()])

    def movePawn(self, coordo: tuple, player: Player):
        for neighbour in self.getNeighbours(player.getCoordinates()):
            if coordo != neighbour.getCoordinates():
                continue

            if self.WallColide(player, coordo):
                return

            self.placePlayer(Player(0), player.getCoordinates())
            self.placePlayer(player, coordo)

    def getDirection(self, player: Player, coordo: tuple, reverse: bool = False) -> str:
        playerCoord = player.getCoordinates()
        if reverse:
            coordo, playerCoord = playerCoord, coordo
        if coordo[0] - playerCoord[0] == -1:
            return "Up"
        if coordo[1] - playerCoord[1] == -1:
            return "Left"
        if coordo[0] - playerCoord[0] == 1:
            return "Down"
        if coordo[1] - playerCoord[1] == 1:
            return "Right"

    def WallColide(self, player: Player, coordo: tuple,):
        if (self.getCell(coordo).getWalls()[self.getDirection(player, coordo)] or
                self.getCell(player.getCoordinates()).getWalls()[self.getDirection(player, coordo, True)]):
            return True
        return False


def intInput(message: str) -> int:
    try:
        return int(input("\n" + message + ":  "))
    except ValueError:
        return intInput("\nIncorect Value, please enter a number")


def yesNoInput(message: str) -> bool:
    while True:
        inp = input("\n" + message + " : (y/n)  ").lower()
        if inp == "y":
            return True
        if inp == "n":
            return False


def createGame(width: int, nbPlayer: int):
    return Jeu(width, nbPlayer)


def initializeGame():
    width = intInput(
        "Select the size of the square you want to create, minimum 5, maximum 11. \nOnly odd numbers")
    nbPlayer = intInput("How many players ? \nminimum 2, maximum 4")

    return createGame(width, nbPlayer)


def play():
    Game = initializeGame()
    Game.display()

    # TODO: replace True by while not Game.gameOver(), do function self.gameOver()
    while True:
        player = Game.getCurrentPlayer()
        print(player.getNumber())
        if isinstance(player, Bot):
            coordo = player.pickCoordo(Game)
            while Game.movePawn(coordo, player) == False:
                coordo = player.pickCoordo(Game)
        else:
            coordo = (intInput("row")-1, intInput("Col")-1)
            while Game.movePawn(coordo, player) == False:
                coordo = (intInput("row")-1, intInput("Col")-1)

        Game.display()
        Game.NextPlayer()


if __name__ == "__main__":
    play()
