import random
from Player import Player
from Case import Case
from Bot import Bot


class Game():
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

    def movePawn(self, coordo: tuple, player: Player, jump: bool = False) -> bool:
        for neighbour in self.getNeighbours(player.getCoordinates()):
            if not jump:
                if coordo != neighbour.getCoordinates():
                    continue
            if self.wallColide(player, coordo):
                return False

            if self.playerColide(coordo):
                return self.jumpPawn(player, coordo)

            self.placePlayer(Player(0), player.getCoordinates())
            self.placePlayer(player, coordo)
            return True
        return False

    def jumpPawn(self, player: Player, coordo: tuple) -> bool:
        coordo = self.getCoordoFromDirection(player, coordo)
        if self.wallColide(player, coordo, True) or self.playerColide(coordo):
            return self.diagonalMove(player, coordo)
        return self.movePawn(coordo, player, True)

    def diagonalMove(self, player: Player, coordo: tuple) -> bool:
        # 0 = Left, 1 = Right
        secondMove = self.diagonalInput(player, coordo)
        coordo = self.getCoordoFromDirection(player, coordo, secondMove)
        return self.movePawn(coordo, player, True)

    def diagonalInput(self, player: Player, coordo: tuple) -> int:
        secondMove = -1
        neighnourDir = self.getNeighbourDirection(
            self.getDirection(player, coordo))

        if (self.getCell(self.getJumpCoordo(player, coordo)).getWalls()[neighnourDir[0]] == 1):
            secondMove = 0
        elif (self.getCell(self.getJumpCoordo(player, coordo)).getWalls()[neighnourDir[1]] == 1):
            secondMove = 1
        else:
            while secondMove != 0 and secondMove != 1:
                secondMove = int(input("Enter second direction"))

        return secondMove

    def getNeighbourDirection(self, direction: str) -> tuple:
        dirArray = ["Up", "Left", "Down", "Right"]
        index = dirArray.index(direction)
        LeftElement, RightElement = index-1, index+1

        LeftElement = len(dirArray)-1 if LeftElement == -1 else LeftElement
        RightElement = 0 if RightElement == len(dirArray) else RightElement

        return dirArray[LeftElement], dirArray[RightElement]

    def getDirection(self, player: Player, coordo: tuple, reverse: bool = False) -> str:
        playerCoord = player.getCoordinates()
        if reverse:
            coordo, playerCoord = playerCoord, coordo
        if coordo[0] - playerCoord[0] <= -1:
            return "Up"
        if coordo[1] - playerCoord[1] <= -1:
            return "Left"
        if coordo[0] - playerCoord[0] >= 1:
            return "Down"
        if coordo[1] - playerCoord[1] >= 1:
            return "Right"

    def getCoordoFromDirection(self, player: Player, coordo: tuple, secondMove: int = -1, reverse: bool = False) -> tuple:

        if secondMove != -1:
            if secondMove == 0:
                secondMove = "Left"
            if secondMove == 1:
                secondMove = "Right"

        if self.getDirection(player, coordo, reverse) == "Up":
            if secondMove == "Left":
                return (coordo[0], coordo[1]-1)
            if secondMove == "Right":
                return (coordo[0], coordo[1]+1)
            return (coordo[0]-1, coordo[1])
        if self.getDirection(player, coordo, reverse) == "Left":
            if secondMove == "Left":
                return (coordo[0]+1, coordo[1])
            if secondMove == "Right":
                return (coordo[0]-1, coordo[1])
            return (coordo[0], coordo[1]-1)
        if self.getDirection(player, coordo, reverse) == "Down":
            if secondMove == "Left":
                return (coordo[0], coordo[1]+1)
            if secondMove == "Right":
                return (coordo[0], coordo[1]-1)
            return (coordo[0]+1, coordo[1])
        if self.getDirection(player, coordo, reverse) == "Right":
            if secondMove == "Left":
                return (coordo[0]-1, coordo[1])
            if secondMove == "Right":
                return (coordo[0]+1, coordo[1])
            return (coordo[0], coordo[1]+1)

    def wallColide(self, player: Player, coordo: tuple, jump: bool = False) -> bool:
        targetCell = self.getCell(coordo)
        PlayerCell = self.getCell(player.getCoordinates())
        if (targetCell.getWalls()[self.getDirection(player, coordo, True)] or
                PlayerCell.getWalls()[self.getDirection(player, coordo)]):
            return True

        if jump:
            jumpCoordo = self.getJumpCoordo(player, coordo)
            jumpCell = self.getCell(jumpCoordo)
            if (jumpCell.getWalls()[self.getDirection(player, jumpCoordo)] or
                    jumpCell.getWalls()[self.getDirection(player, jumpCoordo, True)]):
                return True
        return False

    def getJumpCoordo(self, player: Player, coordo: tuple) -> tuple:
        return self.getCoordoFromDirection(player, coordo, reverse=True)

    def playerColide(self, coordo: tuple) -> bool:
        if self.getCell(coordo).getPlayer().getNumber() != 0:
            return True
        return False

    def checkGameOver(self) -> bool:
        # top row
        for cell in self.getGrid()[0]:
            if cell.getPlayer().getNumber() == 2:
                return True
        # bottom row
        for cell in self.getGrid()[self.getSquareWidth()-1]:
            if cell.getPlayer().getNumber() == 1:
                return True

        if self.getNumberOfPlayers() == 2:
            return False

        # Left row
        for row in self.getGrid():
            if row[0].getPlayer().getNumber() == 4:
                return True
        # Right row
        for row in self.getGrid():
            if row[self.getSquareWidth()-1].getPlayer().getNumber() == 3:
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


def createGame(width: int, nbPlayer: int) -> Game:
    return Game(width, nbPlayer)


def initializeGame() -> Game:
    width = intInput(
        "Select the size of the square you want to create, minimum 5, maximum 11. \nOnly odd numbers")
    nbPlayer = intInput("How many players ? \nminimum 2, maximum 4")

    return createGame(width, nbPlayer)


def play() -> None:
    Game = initializeGame()
    Game.display()

    while not Game.checkGameOver():
        player = Game.getCurrentPlayer()
        print(player.getNumber())
        if isinstance(player, Bot):
            coordo = player.pickCoordo(Game)
            while Game.movePawn(coordo, player) == False:
                coordo = player.pickCoordo(Game)
        else:
            coordo = (intInput("row")-1, intInput("Col")-1)
            while Game.movePawn(coordo, player) == False:
                print(Game.movePawn(coordo, player))
                coordo = (intInput("row")-1, intInput("Col")-1)

        Game.display()
        Game.NextPlayer()


if __name__ == "__main__":
    play()
