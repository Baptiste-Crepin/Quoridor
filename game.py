import random
from Player import Player
from Case import Case
from Bot import Bot


class Game():
    def __init__(self, width: int, nbPlayers: int, nbBarrier: int, nbBots: int, num:int) -> None:
        self.__squareWidth = self.validWidth(width)
        self.__NumberOfBots = nbBots
        # self.__NumberOfPlayers = self.validNumberOfPlayers(nbPlayers)
        self.__NumberOfPlayers = nbPlayers
        self.__NumberOfBarriers = self.validateNumberOfBarriers(nbBarrier)
        self.__PlayerList = self.createPlayerList()
        #self.__currentPlayerN = random.randint(0, self.getNumberOfPlayers()-1)
        self.__currentPlayerN = 0
        self.__currentPlayer = self.getPlayerList()[self.getCurrentPlayerN()]
        self.__grid = self.createGrid()

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

    def getNumberOfBots(self):
        return self.__NumberOfBots

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
        if len(self.getPlayerList()) == 2:
            numberOfBarriers = value//2
            return numberOfBarriers
        elif len(self.getPlayerList()) == 4:
            numberOfBarriers = value//4
            return numberOfBarriers

    def setNumberOfBots(self, value: int):
        self.__NumberOfBots = value

    def createGrid(self) -> list[list[Case]]:
        return [[Case(0, (y, x), Player(0, self.getNumberOfBarriers())) for x in range(self.getSquareWidth())]
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

        if len(self.getPlayerList()) == 4:
            self.placePlayer(self.getPlayerList()[
                             2], (self.getSquareWidth()//2, 0))
            self.placePlayer(self.getPlayerList()[
                             3], (self.getSquareWidth()//2, self.getSquareWidth()-1))

        self.setGrid(grid)

    def createPlayerList(self) -> list:
        playerList = [Player(x+1, self.getNumberOfBarriers())
                      for x in range(self.getNumberOfPlayers())]
        if self.getNumberOfBots() != 0:
            bots = [Bot(len(playerList)+x+1, self.getNumberOfBarriers())
                    for x in range(self.getNumberOfBots())]
            playerList += bots
        return playerList

    def display(self) -> None:
        for r, row in enumerate(self.getGrid()):
            for i in range(2):
                for c, cell in enumerate(row):
                    if i == 0:
                        print(cell, end="")
                        if cell.getWalls()["Right"] == 0:
                            print(" ", end="")
                        else:
                            print("|", end="")
                    elif i == 1:
                        if self.getGrid()[r][c].getWalls()["Down"] == 0:
                            print("  ", end="")
                        else:
                            print("- ", end="")
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

    def nextPlayer(self) -> None:
        if self.getCurrentPlayerN() < len(self.getPlayerList())-1:
            self.setCurrentPlayerN(self.getCurrentPlayerN() + 1)
        else:
            self.setCurrentPlayerN(0)

        self.setCurrentPlayer(self.getPlayerList()[self.getCurrentPlayerN()])

    def previousPlayer(self) -> None:
        if self.getCurrentPlayerN() > 0:
            self.setCurrentPlayerN(self.getCurrentPlayerN() - 1)
        else:
            self.setCurrentPlayerN(len(self.getPlayerList()))

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

    def isValidWall(self, direction: str) -> bool:
        return direction == "Right" or direction == "Down"

    def getCoordoFromDirection(self, currentCoordo: tuple, nextCoordo: tuple, secondMove: int = None, jump: bool = False) -> tuple:

        jump = 2 if jump else 1

        if secondMove == 0:
            secondMove = "Left"
        if secondMove == 1:
            secondMove = "Right"

        moveMap = {
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

        return moveMap[(self.getDirection(currentCoordo, nextCoordo), secondMove)]

    def wallColide(self, currentCoordo: tuple, NextCoordo: tuple, jump: bool = False) -> bool:
        CurrentCell = self.getCell(currentCoordo)
        targetCell = self.getCell(NextCoordo)

        if self.isValidWall(self.getDirection(currentCoordo, NextCoordo, True)):
            if targetCell.getWalls()[self.getDirection(currentCoordo, NextCoordo, True)]:
                return True
        if self.isValidWall(self.getDirection(currentCoordo, NextCoordo)):
            if CurrentCell.getWalls()[self.getDirection(currentCoordo, NextCoordo)]:
                return True

        if jump:
            jumpCoordo = self.getJumpCoordo(currentCoordo, NextCoordo)
            if not self.inGrid(jumpCoordo):
                return False
            jumpCell = self.getCell(jumpCoordo)
            if self.isValidWall(self.getDirection(currentCoordo, jumpCoordo)):
                if (CurrentCell.getWalls()[self.getDirection(currentCoordo, jumpCoordo)]):
                    return True
            if self.isValidWall(self.getDirection(currentCoordo, jumpCoordo, True)):
                if (jumpCell.getWalls()[self.getDirection(currentCoordo, jumpCoordo, True)]):
                    return True
        return False

    def placeWholeBarrier(self, coordo: tuple, direction: str, player: Player, place=True) -> bool:
        if not self.placeBarrier(coordo, direction, player, place=place):
            return False
        # if not self.setOpositeWall(coordo, direction, place=place):
        #     return False
        return True

    def placeBarrier(self, coordo: tuple, direction: str, player: Player, place=True) -> bool:

        if self.detectBarrier(coordo, direction):
            return False
        if self.ignoreSideBarrier(coordo, direction):
            return False
        if player.getBarrier() == 0:
            return False

        if place:
            celWalls = self.getGrid()[coordo[0]][coordo[1]].getWalls()
            celWalls[direction] = 1
            self.getGrid()[coordo[0]][coordo[1]].setWalls(celWalls)

        return True

    def placeWall(self, coordo: tuple, direction: str, player: Player, place=True, ignorePlayerBarriers=False) -> bool:
        '''Place a wall on the grid

        a wall is considered to be a group of two barriers side by side'''
        if not self.placeWholeBarrier(coordo, direction, player, place=place):
            return False
        if not self.setNeighbourWalls(coordo, direction, place=place):
            if place:
                self.cancelBarrierPlacement(coordo, direction)
            return False

        if place and not ignorePlayerBarriers:
            player.setBarrier(player.getBarrier()-1)
        return True

    def detectBarrier(self, coordo: tuple, direction: str) -> bool:
        return self.getGrid()[coordo[0]][coordo[1]].getWalls()[direction] == 1

    def ignoreSideBarrier(self, coordo: tuple, direction: str) -> bool:
        if direction == 'Right':
            return coordo[1] == self.getSquareWidth()
        if direction == 'Down':
            return coordo[0] == self.getSquareWidth()

    def cancelBarrierPlacement(self, coordo: tuple, direction: str) -> None:
        '''Cancel the placement of a barrier'''

        walls = self.getGrid()[coordo[0]][coordo[1]].getWalls()
        walls[direction] = 0
        self.getGrid()[coordo[0]][coordo[1]].setWalls(walls)

    def setNeighbourWalls(self, coordo: tuple, direction: str, place=True) -> bool:

        if (direction == 'Right'):
            if coordo[0] >= len(self.getGrid())-1:
                return False
            neighbourCoordo = (coordo[0]+1, coordo[1])

        if (direction == 'Down'):
            if coordo[1] >= len(self.getGrid())-1:
                return False
            neighbourCoordo = (coordo[0], coordo[1]+1)

        if self.detectBarrier(neighbourCoordo, direction):
            if place:
                self.cancelBarrierPlacement(neighbourCoordo, direction)
            return False

        return self.placeWholeBarrier((neighbourCoordo[0], neighbourCoordo[1]),
                                      direction, self.getCurrentPlayer(), place=place)

    def cancelNeighbourBarriers(self, coordo: tuple, direction: str) -> bool:

        if (direction == 'Right'):
            if coordo[0] >= len(self.getGrid())-1:
                return False
            neighbourCoordo = (coordo[0]+1, coordo[1])

        if (direction == 'Down'):
            if coordo[1] >= len(self.getGrid())-1:
                return False
            neighbourCoordo = (coordo[0], coordo[1]+1)

        if self.detectBarrier(neighbourCoordo, direction):
            self.cancelBarrierPlacement(neighbourCoordo, direction)

    def getJumpCoordo(self, currentCoordo: tuple, nextCoordo: tuple) -> tuple:
        return self.getCoordoFromDirection(currentCoordo, nextCoordo)

    def playerColide(self, coordo: tuple) -> bool:
        '''Check if a cell at given coordo is occupied by a player'''
        if self.getCell(coordo).getPlayer().getNumber() != 0:
            return True
        return False

    def checkGameOver(self) -> bool:
        '''Check if the game is over'''
        if (self.checkPlayerInRow(1, self.getSquareWidth()-1) or
                self.checkPlayerInRow(2, 0)):
            return True

        if len(self.getPlayerList()) == 4:
            if (self.checkPlayerInCol(3, self.getSquareWidth()-1) or
                    self.checkPlayerInCol(4, 0)):
                return True

        return False

    def checkPlayerInRow(self, playerN: int, row: int) -> bool:
        '''Check if the player is in the given column'''
        for cell in self.getGrid()[row]:
            if cell.getPlayer().getNumber() == playerN:
                return True
        return False

    def checkPlayerInCol(self, playerN: int, col: int) -> bool:
        '''Check if the player is in the given column'''
        for row in self.getGrid():
            if row[col].getPlayer().getNumber() == playerN:
                return True
        return False

    def winningSide(self, player: Player):
        '''Return the side that the player must reach to win'''
        direction = ["Down", "Up", "Right", "Left"]
        return direction[player.getNumber()-1]

    def getWinningLine(self, player: Player) -> int:
        '''Return the line that the player must reach to win'''
        if self.winningSide(player) == "Down" or self.winningSide(player) == "Right":
            return self.getSquareWidth()-1
        if self.winningSide(player) == "Up" or self.winningSide(player) == "Left":
            return 0

    def stuck(self) -> bool:
        '''Check any player is stuck'''
        for player in self.getPlayerList():
            coordo = player.getCoordinates()
            self.getCell(coordo).setVisited(True)

            if not self.stuckNeighbour(player, coordo):
                self.resetVisited()
                return True
            self.resetVisited()

        return False

    def resetVisited(self) -> None:
        '''Reset the visited attribute of all cells to False'''
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
        '''Reset the visited attribute of all cells to False'''
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
        '''Return a list of possible moves for the player
        '''

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

                coordinatesAfterJump = self.getCoordoFromDirection(
                    playerCoord, jumpCoordo, jump=True)
                if not self.inGrid(coordinatesAfterJump):
                    continue
                if (self.wallColide(playerCoord, jumpCoordo, True) or self.playerColide(coordinatesAfterJump)):
                    for direction in range(2):
                        if self.checkDiagonalMove(playerCoord, neighbourCoordo, direction):
                            diagCoordinates = self.getCoordoFromDirection(
                                playerCoord, jumpCoordo, direction)
                            if self.getCell(diagCoordinates).getPlayer().getNumber() == 0:
                                result.append(diagCoordinates)

        return result

    def checkBarrierIntersection(self, i, j, direction):
        nbBarrier = 0
        if direction == 'Down':
            otherDirection = 'Right'
            while i-nbBarrier >= 0 and self.getGrid()[i-nbBarrier][j].getWalls()[otherDirection] == 1:
                nbBarrier += 1
            if nbBarrier % 2 == 0:
                return False
            if self.getGrid()[i][j].getWalls()[otherDirection] == 1:
                return True

        if direction == 'Right':
            otherDirection = 'Down'
            while j-nbBarrier >= 0 and self.getGrid()[i][j-nbBarrier].getWalls()[otherDirection] == 1:
                nbBarrier += 1
            if nbBarrier % 2 == 0:
                return False
            if self.getGrid()[i][j].getWalls()[otherDirection] == 1:
                return True

        return False

    def possibleBarrierPlacement(self, player: Player) -> list[tuple]:
        '''Return a list of possible coordinates for a barrier placement
        '''

        result = []

        for i in range(len(self.getGrid())-1):
            for j in range(len(self.getGrid()[i])-1):
                cell = self.getGrid()[i][j]
                for direction in cell.getWalls().keys():
                    if not (direction == 'Down' or direction == 'Right'):
                        continue
                    if self.checkBarrierIntersection(i, j, direction):
                        continue
                    if not self.placeWall((i, j), direction, player, place=False, ignorePlayerBarriers=True):
                        continue
                    self.placeWall((i, j), direction, player,
                                   place=True, ignorePlayerBarriers=True)

                    if not self.stuck():
                        result.append(((i, j), direction))

                    self.cancelBarrierPlacement((i, j), direction)
                    self.cancelNeighbourBarriers((i, j), direction)
        return result

    def movePlayer(self, player: Player, coordo: tuple) -> None:
        '''moves the player to the given coordinates'''
        self.placePlayer(Player(0), player.getCoordinates())
        self.placePlayer(player, coordo)

    def directionInput(self) -> str | None:
        '''Return the direction input by the user or False if the input is invalid'''
        directions = list(self.getGrid()[0][0].getWalls().keys())
        inp = input("Direction |Right or Down|").capitalize()
        if inp in directions:
            return inp
        return


def intInput(message: str) -> int:
    '''Return an integer inputed by the user'''
    try:
        return int(input("\n" + message + ":  "))
    except ValueError:
        return intInput("\nIncorect Value, please enter a number")


def yesNoInput(message: str, inp1: str, inp2: str) -> bool:
    """Return a boolean inputed by the user

    True if the user inputed the first string, false if the user inputed the second string
    """
    while True:
        inp = input('\n {}  : ({}/{})'.format(message, inp1[0], inp2[0]))
        if inp.lower() == inp1[0].lower():
            return True
        if inp.lower() == inp2[0].lower():
            return False


def initializeGame() -> Game:
    '''Initialize the game'''
    width = intInput(
        "Select the size of the square you want to create, minimum 5, maximum 11. \nOnly odd numbers")
    nbPlayer = intInput("How many players ? \nminimum 2, maximum 4")
    nbBarrier = intInput(
        "How many Barriers? \nminimum 4, maximum "+Game.maxBarrier(width))
    bots = intInput("how many bots do you want to play against?")

    return Game(width, nbPlayer, nbBarrier, bots)


def play() -> None:
    '''Main function of the game'''
    Game = initializeGame()
    Game.display()

    while not Game.checkGameOver():
        player = Game.getCurrentPlayer()
        print(player)

        if isinstance(player, Bot):
            player.randomMoves(Game)
        else:
            choise = yesNoInput(
                'to place barrier enter "p"\n to play enter "m"', "p", "m")
            coordo = (intInput("row")-1, intInput("Col")-1)
            if choise:
                direction = Game.directionInput()
                while not direction:
                    direction = Game.directionInput()

                while not Game.placeWall(coordo, direction, player):
                    coordo = (intInput("row")-1, intInput("Col")-1)
                    while direction == False:
                        direction = Game.directionInput()

                player.setBarrier(player.getBarrier()-1)
            else:
                while coordo not in Game.possibleMoves(player.getCoordinates()):
                    coordo = (intInput("row")-1, intInput("Col")-1)
                Game.movePlayer(player, coordo)

        Game.display()
        #Game.nextPlayer()


if __name__ == "__main__":
    play()
