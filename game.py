import random
from Player import Player
from Case import Case
from Bot import Bot


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

    def validateNumberOfBarriers(self, n: int, min: int = 4) -> int:
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

    def getGrid(self) -> list[list[Case]]:
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

    def createGrid(self) -> list[list[Case]]:
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

    def NextPlayer(self) -> None:
        if self.getCurrentPlayerN() < len(self.getPlayerList())-1:
            self.setCurrentPlayerN(self.getCurrentPlayerN() + 1)
        else:
            self.setCurrentPlayerN(0)

        self.setCurrentPlayer(self.getPlayerList()[self.getCurrentPlayerN()])

    def checkOrthogonalMove(self, coordo: tuple, playerCoord: tuple) -> bool:
        for neighbour in self.getNeighbours(playerCoord):
            if coordo != neighbour.getCoordinates():
                continue
            if self.wallColide(playerCoord, coordo):
                continue
            if self.playerColide(coordo):
                continue

            return True
        return False

    def checkJump(self, playerCoord: tuple, coordo: tuple) -> bool:
        jumpCoordo = self.getCoordoFromDirection(
            playerCoord, coordo, jump=True)
        if not self.inGrid(jumpCoordo):
            return False
        if self.wallColide(playerCoord, jumpCoordo, True) or self.playerColide(jumpCoordo):
            return False
        return self.checkOrthogonalMove(jumpCoordo, coordo)

    def checkDiagonalMove(self, playerCoord: tuple, coordo: tuple, secondMove) -> bool:
        """Diagonal movement

        secondMove: (0 = Left || 1 = Right)
        """
        Newcoordo = self.getCoordoFromDirection(
            playerCoord, coordo, secondMove)
        if not self.wallColide(playerCoord, coordo):
            return self.checkOrthogonalMove(Newcoordo, coordo)
        return False

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

        if nextCoordo[0] - currentCoordo[0] <= -1:
            return "Up"
        if nextCoordo[1] - currentCoordo[1] <= -1:
            return "Left"
        if nextCoordo[0] - currentCoordo[0] >= 1:
            return "Down"
        if nextCoordo[1] - currentCoordo[1] >= 1:
            return "Right"

    def getCoordoFromDirection(self, currentCoordo: tuple, nextCoordo: tuple, secondMove: int = None, jump: bool = False) -> tuple:

        if jump:
            jump = 2
        else:
            jump = 1

        if secondMove == 0:
            secondMove = "Left"
        if secondMove == 1:
            secondMove = "Right"

        move_map = {
            ("Up", None): (currentCoordo[0]-jump, currentCoordo[1]),
            ("Up", "Left"): (currentCoordo[0]-jump, currentCoordo[1]-jump),
            ("Up", "Right"): (currentCoordo[0]-jump, currentCoordo[1]+jump),
            ("Left", None): (currentCoordo[0], currentCoordo[1]-jump),
            ("Left", "Left"): (currentCoordo[0]+jump, currentCoordo[1]-jump),
            ("Left", "Right"): (currentCoordo[0]-jump, currentCoordo[1]-jump),
            ("Down", None): (currentCoordo[0]+jump, currentCoordo[1]),
            ("Down", "Left"): (currentCoordo[0]+jump, currentCoordo[1]+jump),
            ("Down", "Right"): (currentCoordo[0]+jump, currentCoordo[1]-jump),
            ("Right", None): (currentCoordo[0], currentCoordo[1]+jump),
            ("Right", "Left"): (currentCoordo[0]-jump, currentCoordo[1]+jump),
            ("Right", "Right"): (currentCoordo[0]+jump, currentCoordo[1]+jump),
        }

        return move_map[(self.getDirection(currentCoordo, nextCoordo), secondMove)]

    def wallColide(self, currentCoordo: tuple, NextCoordo: tuple, jump: bool = False) -> bool:
        CurrentCell = self.getCell(currentCoordo)
        targetCell = self.getCell(NextCoordo)

        if (targetCell.getWalls()[self.getDirection(currentCoordo, NextCoordo, True)] or
                CurrentCell.getWalls()[self.getDirection(currentCoordo, NextCoordo)]):
            return True
        if jump:
            jumpCoordo = self.getJumpCoordo(currentCoordo, NextCoordo)
            if not self.inGrid(jumpCoordo):
                return False
            jumpCell = self.getCell(jumpCoordo)
            if (jumpCell.getWalls()[self.getDirection(currentCoordo, jumpCoordo)] or
                    jumpCell.getWalls()[self.getDirection(currentCoordo, jumpCoordo, True)]):
                return True
        return False

    def placeWholeBarrier(self, coordo: tuple, direction: str, player: Player) -> bool:
        if not self.placeBarrier(coordo, direction, player):
            return False
        if not self.setOpositeWall(coordo, direction):
            return False
        return True

    def placeBarrier(self, coordo: tuple, direction: str, player: Player) -> bool:
        if self.stuck():
            self.cancelPlacement(coordo, direction)
            return False

        if self.detectBarrier(coordo, direction):
            return False
        if self.ignoreSideBarrier(coordo, direction):
            return False
        if player.getBarrier() == 0:
            return False
        celWalls = self.getGrid()[coordo[0]][coordo[1]].getWalls()
        celWalls[direction] = 1

        self.getGrid()[coordo[0]][coordo[1]].setWalls(celWalls)
        return True

    def placeWall(self, coordo: tuple, direction: str, player: Player) -> bool:
        # TODO: refacto like the movement to allow hover
        # a Wall is considered to be a group of two barriers side to side
        if not self.placeWholeBarrier(coordo, direction, player):
            return False
        if not self.setNeighbourWalls(coordo, direction):
            self.cancelPlacement(coordo, direction)
            return False

        player.setBarrier(player.getBarrier()-1)
        return True

    def detectBarrier(self, coordo: tuple, direction: str) -> bool:
        if self.getGrid()[coordo[0]][coordo[1]].getWalls()[direction] == 1:
            return True
        return False

    def ignoreSideBarrier(self, coordo: tuple, direction: str) -> bool:
        if direction == 'Right':
            return coordo[1] == self.getSquareWidth()
        if direction == 'Left':
            return coordo[1] == 0
        if direction == 'Down':
            return coordo[0] == self.getSquareWidth()
        if direction == 'Up':
            return coordo[0] == 0

    def setOpositeWall(self, coordo: tuple, direction: str) -> bool:

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

    def cancelPlacement(self, coordo: tuple, direction: str, firstIteration: bool = True) -> None:
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
            return False

        return self.placeWholeBarrier((neighbourCoordo[0], neighbourCoordo[1]),
                                      direction, self.getCurrentPlayer())

    def getJumpCoordo(self, currentCoordo: tuple, nextCoordo: tuple) -> tuple:
        return self.getCoordoFromDirection(currentCoordo, nextCoordo)

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

    def getWinningLine(self, player: Player) -> int:
        if self.winningSide(player) == "Down" or self.winningSide(player) == "Right":
            return self.getSquareWidth()-1
        if self.winningSide(player) == "Up" or self.winningSide(player) == "Left":
            return 0

    def stuck(self) -> bool:
        for player in self.getPlayerList():
            coordo = player.getCoordinates()
            self.getCell(coordo).setVisited(True)

            if not self.stuckNeighbour(player, coordo):
                self.resetVisited()
                return True
            self.resetVisited()

        return False

    def resetVisited(self) -> None:
        for j in range(self.nbRows):
            for i in range(self.nbColumns):
                self.cells[i][j].setVisited(False)

    def stuckNeighbour(self, player: Player, coordo: tuple) -> bool:
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

    def maxBarrier(key: int) -> int:
        numberMax = {5: '8', 7: '12', 9: '20', 11: '40'}
        return numberMax[key]

    def playerBarrier(self) -> int:
        if self.getSquareWidth() == 5:
            return 8
        if self.getSquareWidth() == 7:
            return 12
        if self.getSquareWidth() == 9:
            return 20
        if self.getSquareWidth() == 11:
            return 40

    def possibleMoves(self, playerCoord: tuple) -> list[tuple]:
        # print('\n'*5, 'NewTurn')

        result = []
        for neighbour in self.getNeighbours(playerCoord):
            neighbourCoordo = neighbour.getCoordinates()
            if self.checkOrthogonalMove(neighbourCoordo, playerCoord):
                result.append(neighbourCoordo)
                continue

            if self.playerColide(neighbourCoordo):
                jumpCoordo = self.getCoordoFromDirection(
                    playerCoord, neighbourCoordo, jump=True)
                if self.checkJump(playerCoord, neighbourCoordo):
                    result.append(jumpCoordo)
                    continue

                a = self.getCoordoFromDirection(
                    playerCoord, jumpCoordo, jump=True)
                if not self.inGrid(a):
                    continue
                if (self.wallColide(playerCoord, jumpCoordo, True) or self.playerColide(a)):
                    for direction in range(2):
                        if self.checkDiagonalMove(playerCoord, neighbourCoordo, direction):
                            diagCoordinates = self.getCoordoFromDirection(
                                playerCoord, jumpCoordo, direction)
                            if self.getCell(diagCoordinates).getPlayer().getNumber() == 0:
                                result.append(diagCoordinates)

        return result

    def movePlayer(self, player: Player, coordo: tuple) -> None:
        self.placePlayer(Player(0), player.getCoordinates())
        self.placePlayer(player, coordo)

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
        inp = input('\n {}  : ({}/{})'.format(message, inp1[0], inp2[0]))
        if inp.lower() == inp1[0].lower():
            return True
        if inp.lower() == inp2[0].lower():
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
        choise = yesNoInput(
            'to place barrier enter "p"\n to play enter "m"', "p", "m")
        coordo = (intInput("row")-1, intInput("Col")-1)

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
            while coordo not in Game.possibleMoves(player.getCoordinates()):
                coordo = (intInput("row")-1, intInput("Col")-1)
            Game.movePlayer(player, coordo)

        Game.display()
        Game.NextPlayer()


if __name__ == "__main__":
    play()
