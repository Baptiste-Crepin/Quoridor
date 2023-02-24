import random
from Player import Player
from Case import Case
from Bot import Bot
# from Table import Board


class Game():
    def __init__(self, width: int, nbPlayers: int, nbBarrier: int) -> None:
        self.__squareWidth = self.validWidth(width)
        self.__grid = self.createGrid()
        self.__NumberOfPlayers = self.validNumberOfPlayers(nbPlayers)
        self.__NumberOfBarriers = self.validateNumberOfBarriers(nbBarrier)
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

    def validateNumberOfBarriers(self, n: int, min: int = 4):
        if n % 4 == 1:
            print("You mush set an even amount of barriers")
        if n < min:
            print(
                f"The amount of Barriers must not be greater than {min}, it has automatically been increased")
            n = min
        elif n > int(self.playerBarrier()):
            print(
                f"The amount of players must exceed {self.playerBarrier()}, it has automatically been increased")
            n = int(self.playerBarrier())
        return n

    def getSquareWidth(self) -> int:
        return self.__squareWidth

    def getGrid(self) -> list:
        return self.__grid

    def getNumberOfPlayers(self) -> int:
        return self.__NumberOfPlayers

    def getNumberOfBots(self) -> int:
        return self.__NumberOfBots

    def getNumberOfBarriers(self) -> int:
        return self.__NumberOfBarriers

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

    def setNumberOfBarriers(self, value: int) -> None:
        if self.getNumberOfPlayers == 2:
            numberOfBarriers = value//2
            return numberOfBarriers
        elif self.getNumberOfPlayers == 4:
            numberOfBarriers = value//4
            return numberOfBarriers

    def createGrid(self) -> list:
        return [[Case(0, (y, x), Player(0, self.setNumberOfBarriers(self.getNumberOfBarriers))) for x in range(self.getSquareWidth())]
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
        return [Player(x+1, self.getNumberOfBarriers()) for x in range(self.getNumberOfPlayers())]

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
        playerCoord = player.getCoordinates()
        for neighbour in self.getNeighbours(playerCoord):
            if not jump:
                if coordo != neighbour.getCoordinates():
                    continue
            if self.wallColide(playerCoord, coordo):
                return False

            if self.playerColide(coordo):
                return self.jumpPawn(player, coordo)

            self.placePlayer(Player(0), playerCoord)
            self.placePlayer(player, coordo)
            return True
        return False

    def jumpPawn(self, player: Player, coordo: tuple) -> bool:
        # TODO: fix oor bug when jumping to a sidewall
        playerCoord = player.getCoordinates()
        coordo = self.getCoordoFromDirection(playerCoord, coordo)
        if self.wallColide(playerCoord, coordo, True) or self.playerColide(coordo):
            return self.diagonalMove(player, coordo)
        return self.movePawn(coordo, player, True)

    def diagonalMove(self, player: Player, coordo: tuple) -> bool:
        playerCoord = player.getCoordinates()
        # 0 = Left, 1 = Right
        secondMove = self.diagonalInput(player, coordo)
        coordo = self.getCoordoFromDirection(playerCoord, coordo, secondMove)
        return self.movePawn(coordo, player, True)

    def diagonalInput(self, player: Player, coordo: tuple) -> int:
        playerCoord = player.getCoordinates()
        secondMove = -1
        neighnourDir = self.getNeighbourDirection(
            self.getDirection(playerCoord, coordo))

        if (self.getCell(self.getJumpCoordo(playerCoord, coordo)).getWalls()[neighnourDir[0]] == 1):
            secondMove = 0
        elif (self.getCell(self.getJumpCoordo(playerCoord, coordo)).getWalls()[neighnourDir[1]] == 1):
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

    def getDirection(self, currentCoordo: tuple, nextCoordo: tuple, reverse: bool = False) -> str:
        if reverse:
            nextCoordo, currentCoordo = currentCoordo, nextCoordo

        # print(coordo, playerCoord, coordo[0] -
            #   playerCoord[0], coordo[1] - playerCoord[1])
        if nextCoordo[0] - currentCoordo[0] <= -1:
            return "Up"
        if nextCoordo[1] - currentCoordo[1] <= -1:
            return "Left"
        if nextCoordo[0] - currentCoordo[0] >= 1:
            return "Down"
        if nextCoordo[1] - currentCoordo[1] >= 1:
            return "Right"

    def getCoordoFromDirection(self, currentCoordo: tuple, nextCoordo: tuple, secondMove: int = -1, reverse: bool = False) -> tuple:

        if secondMove != -1:
            if secondMove == 0:
                secondMove = "Left"
            if secondMove == 1:
                secondMove = "Right"

        if self.getDirection(currentCoordo, nextCoordo, reverse) == "Up":
            if secondMove == "Left":
                return (nextCoordo[0], nextCoordo[1]-1)
            if secondMove == "Right":
                return (nextCoordo[0], nextCoordo[1]+1)
            return (nextCoordo[0]-1, nextCoordo[1])
        if self.getDirection(currentCoordo, nextCoordo, reverse) == "Left":
            if secondMove == "Left":
                return (nextCoordo[0]+1, nextCoordo[1])
            if secondMove == "Right":
                return (nextCoordo[0]-1, nextCoordo[1])
            return (nextCoordo[0], nextCoordo[1]-1)
        if self.getDirection(currentCoordo, nextCoordo, reverse) == "Down":
            if secondMove == "Left":
                return (nextCoordo[0], nextCoordo[1]+1)
            if secondMove == "Right":
                return (nextCoordo[0], nextCoordo[1]-1)
            return (nextCoordo[0]+1, nextCoordo[1])
        if self.getDirection(currentCoordo, nextCoordo, reverse) == "Right":
            if secondMove == "Left":
                return (nextCoordo[0]-1, nextCoordo[1])
            if secondMove == "Right":
                return (nextCoordo[0]+1, nextCoordo[1])
            return (nextCoordo[0], nextCoordo[1]+1)

    def wallColide(self, currentCoordo: tuple, NextCoordo: tuple, jump: bool = False) -> bool:
        CurrentCell = self.getCell(currentCoordo)
        targetCell = self.getCell(NextCoordo)
        # print(self.getDirection(player, coordo, True))
        if (targetCell.getWalls()[self.getDirection(currentCoordo, NextCoordo, True)] or
                CurrentCell.getWalls()[self.getDirection(currentCoordo, NextCoordo)]):
            return True

        if jump:
            jumpCoordo = self.getJumpCoordo(currentCoordo, NextCoordo)
            jumpCell = self.getCell(jumpCoordo)
            if (jumpCell.getWalls()[self.getDirection(currentCoordo, jumpCoordo)] or
                    jumpCell.getWalls()[self.getDirection(currentCoordo, jumpCoordo, True)]):
                return True
        return False

    def placeWholeBarrier(self, coordo, direction, player):
        if not self.placeBarrier(coordo, direction, player):
            return False
        if not self.setOpositeWall(coordo, direction):
            return False
        return True

    def placeBarrier(self, coordo: tuple, direction: str, player: Player):
        if self.stuck():
            self.cancelPlacement(coordo, direction)
            print('STUCK', coordo, direction)
            return False

        if self.detectBarrier(coordo, direction):
            print('HELP', coordo)
            return False
        if self.ignoreSideBarrier(coordo, direction):
            return False
        if player.getBarrier() == 0:
            return False
        celWalls = self.getGrid()[coordo[0]][coordo[1]].getWalls()
        celWalls[direction] = 1

        self.getGrid()[coordo[0]][coordo[1]].setWalls(celWalls)
        return True

    def placeWall(self, coordo, direction, player):
        # a Wall is considered to be a group of two barriers side to side
        if not self.placeWholeBarrier(coordo, direction, player):
            return False
        if not self.setNeighbourWalls(coordo, direction):
            self.cancelPlacement(coordo, direction)
            return False

        player.setBarrier(player.getBarrier()-1)
        return True

    def detectBarrier(self, coordo: tuple, direction: str):
        if self.getGrid()[coordo[0]][coordo[1]].getWalls()[direction] == 1:
            return True
        return False

    def ignoreSideBarrier(self, coordo: tuple, direction: str):
        if direction == 'Right':
            if coordo[1] == self.getSquareWidth():
                return True
            return False
        if direction == 'Left':
            if coordo[1] == 0:
                return True
            return False
        if direction == 'Down':
            if coordo[0] == self.getSquareWidth():
                return True
            return False
        if direction == 'Up':
            if coordo[0] == 0:
                return True
            return False

    def setOpositeWall(self, coordo: tuple, direction: str):

        if direction == 'Right':
            return self.placeBarrier((coordo[0], coordo[1]+1),
                                     self.oppositeDirection(direction), self.getCurrentPlayer())

        if direction == 'Left':
            return self.placeBarrier((coordo[0], coordo[1]-1),
                                     self.oppositeDirection(direction), self.getCurrentPlayer())

        if direction == 'Down':
            return self.placeBarrier((coordo[0]+1, coordo[1]),
                                     self.oppositeDirection(direction), self.getCurrentPlayer())

        if direction == 'Up':
            return self.placeBarrier((coordo[0]-1, coordo[1]),
                                     self.oppositeDirection(direction), self.getCurrentPlayer())

    def cancelPlacement(self, coordo, direction, firstIteration=True):
        print(coordo, direction)
        if firstIteration:
            if direction == 'Left':
                oppositeWallCellCoordo = (coordo[0], coordo[1]-1)
            if direction == 'Right':
                oppositeWallCellCoordo = (coordo[0], coordo[1]+1)
            if direction == 'Up':
                oppositeWallCellCoordo = (coordo[0]-1, coordo[1])
            if direction == 'Down':
                oppositeWallCellCoordo = (coordo[0]+1, coordo[1])
            self.cancelPlacement(oppositeWallCellCoordo,
                                 self.oppositeDirection(direction), False)

        walls = self.getGrid()[coordo[0]][coordo[1]].getWalls()
        walls[direction] = 0
        self.getGrid()[coordo[0]][coordo[1]].setWalls(walls)

    def setNeighbourWalls(self, coordo: tuple, direction: str) -> bool:
        if (direction == 'Right' or direction == 'Left'):
            if coordo[0] >= len(self.getGrid())-1:
                return False
            neighbourCoordo = (coordo[0]+1, coordo[1])

        if (direction == 'Up' or direction == 'Down'):
            if coordo[1] >= len(self.getGrid())-1:
                return False
            neighbourCoordo = (coordo[0], coordo[1]+1)

        if self.detectBarrier(neighbourCoordo, direction):
            self.cancelPlacement(neighbourCoordo, direction)
            # self.cancelPlacement(coordo, direction)
            return False

        return self.placeWholeBarrier((neighbourCoordo[0], neighbourCoordo[1]),
                                      direction, self.getCurrentPlayer())

    def getJumpCoordo(self, currentCoordo: tuple, nextCoordo: tuple) -> tuple:
        return self.getCoordoFromDirection(currentCoordo, nextCoordo, reverse=True)

    def playerColide(self, coordo: tuple) -> bool:
        if self.getCell(coordo).getPlayer().getNumber() != 0:
            return True
        return False

    def checkGameOver(self) -> bool:
        if (self.checkPlayerInRow(1, self.getSquareWidth()-1) or
                self.checkPlayerInRow(2, 0)):
            return True

        if self.getNumberOfPlayers() == 4:
            if (self.checkPlayerInCol(3, self.getSquareWidth()-1) or
                    self.checkPlayerInCol(4, 0)):
                return True

        return False

    def checkPlayerInRow(self, playerN: int, row: int) -> bool:
        for cell in self.getGrid()[row]:
            if cell.getPlayer().getNumber() == playerN:
                return True
        return False

    def checkPlayerInCol(self, playerN: int, col: int) -> bool:
        for row in self.getGrid():
            if row[col].getPlayer().getNumber() == playerN:
                return True
        return False

    def oppositeDirection(self, direction: str) -> str:
        directions = list(self.getGrid()[0][0].getWalls().keys())

        return directions[directions.index(direction)-2]

    def winningSide(self, player: Player):
        direction = ["Down", "Up", "Right", "Left"]
        return direction[player.getNumber()-1]

    def getWinningLine(self, player: Player):
        if self.winningSide(player) == "Down" or self.winningSide(player) == "Right":
            return self.getSquareWidth()-1
        if self.winningSide(player) == "Up" or self.winningSide(player) == "Left":
            return 0

    def stuck(self):
        for player in self.getPlayerList():
            coordo = player.getCoordinates()
            self.getCell(coordo).setVisited(True)

            if not self.stuckNeighbour(player, coordo):
                self.resetVisited()
                return True
            self.resetVisited()

        return False

    def resetVisited(self):
        for j in range(self.nbRows):
            for i in range(self.nbColumns):
                self.cells[i][j].setVisited(False)

    def stuckNeighbour(self, player, coordo):
        if self.winningSide(player) == "Up" or self.winningSide(player) == "Down":
            if coordo[0] == self.getWinningLine(player):
                return True
        if self.winningSide(player) == "Left" or self.winningSide(player) == "Right":
            if coordo[1] == self.getWinningLine(player):
                return True

        for neighbour in self.getNeighbours(coordo):
            if neighbour.getCoordinates() == player.getCoordinates():
                continue
            if self.wallColide(coordo, neighbour.getCoordinates()):
                continue
            if neighbour.getVisited():
                continue

            nextCellCoordo = neighbour.getCoordinates()
            neighbour.setVisited(True)
            nextCell = self.stuckNeighbour(player, nextCellCoordo)
            if nextCell:
                return nextCell

        return False

    def resetVisited(self) -> None:
        for row in self.getGrid():
            for cell in row:
                cell.setVisited(False)

    def maxBarrier(key: int):
        numberMax = {5: '8', 7: '12', 9: '20', 11: '40'}
        return numberMax[key]

    def playerBarrier(self):
        if self.getSquareWidth() == 5:
            return 8
        if self.getSquareWidth() == 7:
            return 12
        if self.getSquareWidth() == 9:
            return 20
        if self.getSquareWidth() == 11:
            return 40

    def directionInput(self, message: str) -> str | bool:
        directions = list(self.getGrid()[0][0].getWalls().keys())
        inp = input(message).capitalize()
        if inp in directions:
            return inp
        return False


def intInput(message: str) -> int:
    try:
        return int(input("\n" + message + ":  "))
    except ValueError:
        return intInput("\nIncorect Value, please enter a number")


def yesNoInput(message: str, inp1: str, inp2: str) -> bool:
    while True:
        inp = input("\n" + message + " : ("+inp1[0]+"/"+inp2[0]+")")
        if inp.lower() == inp1[0].lower():
            return True
        if inp.lower == inp2[0].lower():
            return False


def initializeGame() -> Game:
    width = intInput(
        "Select the size of the square you want to create, minimum 5, maximum 11. \nOnly odd numbers")
    nbPlayer = intInput("How many players ? \nminimum 2, maximum 4")
    nbBarrier = intInput(
        "How many Barriers? \nminimum 4, maximum "+Game.maxBarrier(width))
    return Game(width, nbPlayer, nbBarrier)


def play() -> None:
    Game = initializeGame()
    Game.display()

    while not Game.checkGameOver():
        player = Game.getCurrentPlayer()
        print(player)
        coordo = (intInput("row")-1, intInput("Col")-1)
        choise = yesNoInput(
            'to place barrier enter "p"\n to play enter "m"', "p", "m")

        if choise:
            direction = Game.directionInput("direction")
            while direction == False:
                direction = Game.directionInput("direction")

            while Game.placeWall(coordo, direction, player) == False:
                coordo = (intInput("row")-1, intInput("Col")-1)
                while direction == False:
                    direction = Game.directionInput("direction")

            player.setBarrier(player.getBarrier()-1)
        else:
            while Game.movePawn(coordo, player) == False:
                print(Game.movePawn(coordo, player))
                coordo = (intInput("row")-1, intInput("Col")-1)

        Game.display()
        Game.NextPlayer()


if __name__ == "__main__":
    play()
