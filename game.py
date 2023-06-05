import random
from player import Player
from cell import Cell
from Bot import Bot


class Game():
    """
    the game class contains all the logic of the game
    """

    def __init__(self, width: int, nbPlayers: int, nbBarrier: int, nbBots: int) -> None:
        """
        the game class contains all the logic of the game
        width: the width of the square grid
        nbPlayers: the number of players
        nbBarrier: the number of barriers
        nbBots: the number of bots
        """
        self.__squareWidth = width
        self.__NumberOfBots = nbBots
        self.__NumberOfPlayers = nbPlayers
        self.__NumberOfBarriers = nbBarrier

        self.__PlayerList = self.createPlayerList()
        # initialize the current playerIndex to a random player
        self.__currentPlayerIndex = random.randint(
            0, self.getNumberOfPlayers()-1)
        # initialize the current player to the player at the current player index
        self.__currentPlayer = self.getPlayerList()[
            self.getCurrentPlayerIndex()]

        self.__grid = self.createGrid()
        self.initializePawns()

    def getSquareWidth(self) -> int:
        return self.__squareWidth

    def getGrid(self) -> list[list[Cell]]:
        return self.__grid

    def getNumberOfPlayers(self) -> int:
        return self.__NumberOfPlayers

    def getNumberOfBots(self) -> int:
        return self.__NumberOfBots

    def getNumberOfBarriers(self) -> int:
        return self.__NumberOfBarriers

    def getPlayerList(self) -> list[Player]:
        return self.__PlayerList

    def getCurrentPlayerIndex(self) -> int:
        return self.__currentPlayerIndex

    def getCurrentPlayer(self) -> Player | Bot:
        return self.__currentPlayer

    def setSquareWidth(self, value: int) -> None:
        self.__squareWidth = value

    def setGrid(self, value: list[list[Cell]]) -> None:
        self.__grid = value

    def setNumberOfPlayers(self, value: int) -> None:
        self.__NumberOfPlayers = value

    def setNumberOfBots(self, value: int) -> None:
        self.__NumberOfBots = value

    def setPlayerList(self, value: list[Player]) -> None:
        self.__PlayerList = value

    def setCurrentPlayerIndex(self, value: int) -> None:
        self.__currentPlayerIndex = value

    def setCurrentPlayer(self, value: Player | Bot) -> None:
        self.__currentPlayer = value

    def createGrid(self) -> list[list[Cell]]:
        """create a grid of cells"""
        return [[Cell((y, x), Player(0, self.getNumberOfBarriers()))
                for x in range(self.getSquareWidth())]
                for y in range(self.getSquareWidth())]

    def placePlayer(self, player: Player, coordinates: tuple[int, int]) -> None:
        """place a player on the grid at specific coordinates"""
        self.getGrid()[coordinates[0]][coordinates[1]].setPlayer(player)
        player.setCoordinates((coordinates[0], coordinates[1]))

    def initializePawns(self) -> None:
        """place the pawns on the starting squares"""
        startingSquares = {0: (0, self.getSquareWidth()//2),
                           1: (self.getSquareWidth()-1, self.getSquareWidth()//2),
                           2: (self.getSquareWidth()//2, 0),
                           3: (self.getSquareWidth()//2, self.getSquareWidth()-1)}

        for i, player in enumerate(self.getPlayerList()):
            self.placePlayer(player, startingSquares[i])

    def createPlayerList(self) -> list[Player]:
        """create a list of players"""
        playerList = [Player(x+1, self.getNumberOfBarriers())
                      for x in range(self.getNumberOfPlayers())]
        if self.getNumberOfBots() != 0:
            bots = [Bot(len(playerList)+x+1, self.getNumberOfBarriers())
                    for x in range(self.getNumberOfBots())]
            playerList += bots
        return playerList

    def display(self) -> None:
        """display the grid in the console"""
        for r, row in enumerate(self.getGrid()):
            for i in range(2):
                for c, cell in enumerate(row):
                    if i == 0:
                        print(cell, end="")
                        if cell.getWalls()["Right"]:
                            print("|", end="")
                        else:
                            print(" ", end="")
                    elif i == 1:
                        if self.getGrid()[r][c].getWalls()["Down"]:
                            print("- ", end="")
                        else:
                            print("  ", end="")
                print()

    def inGrid(self, coord: tuple[int, int]) -> bool:
        """Return True if the given coordinates are in the grid"""
        return (
            coord[0] >= 0
            and coord[1] >= 0
            and coord[0] < self.getSquareWidth()
            and coord[1] < self.getSquareWidth()
        )

    def getNeighbors(self, coord: tuple[int, int]) -> list[Cell]:
        """Return a list of the neighbors of the cell at the given coordinates"""

        neighbors = list[Cell]()

        if coord[0] >= 1:
            neighbors.append(self.getCell((coord[0]-1, coord[1])))
        if coord[1] >= 1:
            neighbors.append(self.getCell((coord[0], coord[1]-1)))
        if coord[0]+1 < self.getSquareWidth():
            neighbors.append(self.getCell((coord[0]+1, coord[1])))
        if coord[1]+1 < self.getSquareWidth():
            neighbors.append(self.getCell((coord[0], coord[1]+1)))

        return neighbors

    def getCell(self, coord: tuple[int, int]) -> Cell:
        """Return the cell at the given coordinates"""
        return self.getGrid()[coord[0]][coord[1]]

    def getPreviousPlayer(self) -> Player:
        """Return the previous player"""
        if self.getCurrentPlayerIndex() == 0:
            return self.getPlayerList()[len(self.getPlayerList())-1]
        return self.getPlayerList()[self.getCurrentPlayerIndex()-1]

    def getNextPlayer(self) -> Player:
        """Return the next player"""
        if self.getCurrentPlayerIndex() == len(self.getPlayerList())-1:
            return self.getPlayerList()[0]
        return self.getPlayerList()[self.getCurrentPlayerIndex()+1]

    def nextPlayer(self) -> None:
        """Set the current player to the next player"""
        nextPlayerIndex = self.getPlayerList().index(self.getNextPlayer())
        self.setCurrentPlayer(self.getNextPlayer())
        self.setCurrentPlayerIndex(nextPlayerIndex)

    def checkOrthogonalMove(self, coord: tuple[int, int], playerCoord: tuple[int, int]) -> bool:
        """Check if the given coordinates are a valid orthogonal move"""
        for neighbor in self.getNeighbors(playerCoord):
            if coord != neighbor.getCoordinates():
                continue
            if self.wallCollide(playerCoord, coord):
                continue
            if self.playerCollide(coord):
                continue

            return True
        return False

    def checkJump(self, playerCoord: tuple[int, int], coord: tuple[int, int]) -> bool:
        """Check if the given coordinates are a valid jump move"""
        jumpCoord = self.getCoordsFromDirection(
            playerCoord, coord, jump=True)
        if not self.inGrid(jumpCoord):
            return False
        if self.wallCollide(playerCoord, jumpCoord, True) or self.playerCollide(jumpCoord):
            return False
        return self.checkOrthogonalMove(jumpCoord, coord)

    def checkDiagonalMove(self, playerCoord: tuple[int, int], coord: tuple[int, int], secondMove: int) -> bool:
        """
        Check if the given coordinates are a valid jump move

        secondMove: {0: Left, 1: Right}
        """
        newCoord = self.getCoordsFromDirection(
            playerCoord, coord, secondMove)
        if not self.wallCollide(playerCoord, coord):
            return self.checkOrthogonalMove(newCoord, coord)
        return False

    def getNeighborDirection(self, direction: str) -> tuple[str, str]:
        """Return the left and right direction of the given direction"""
        dirArray = ["Up", "Left", "Down", "Right"]
        index = dirArray.index(direction)
        LeftElement, RightElement = index-1, index+1

        LeftElement = len(dirArray)-1 if LeftElement == -1 else LeftElement
        RightElement = 0 if RightElement == len(dirArray) else RightElement

        return dirArray[LeftElement], dirArray[RightElement]

    def getDirection(self, currentCoord: tuple[int, int], nextCoord: tuple[int, int], reverse: bool = False) -> str:
        """Return the direction to go from the currentCoord to the nextCoord"""
        if reverse:
            nextCoord, currentCoord = currentCoord, nextCoord

        if nextCoord[0] - currentCoord[0] <= -1:
            return "Up"
        if nextCoord[1] - currentCoord[1] <= -1:
            return "Left"
        return "Down" if nextCoord[0] - currentCoord[0] >= 1 else "Right"

    def isValidWall(self, direction: str) -> bool:
        """
        Return True if the given direction is a valid wall direction
        Walls are only set on the right and down side of a cell
        the Left and Up sides are the neighbor's right and down sides
        """
        return direction in {"Right", "Down"}

    def getCoordsFromDirection(self, currentCoord: tuple[int, int], nextCoord: tuple[int, int], secondMove: int | None = None, jump: bool = False) -> tuple[int, int]:
        """Return the coordinates of the cell in the given direction"""

        jumpOffset = 2 if jump else 1
        moveMap = {
            "Up": {
                "": (currentCoord[0]-jumpOffset, currentCoord[1]),
                "Left": (currentCoord[0]-jumpOffset, currentCoord[1]-jumpOffset),
                "Right": (currentCoord[0]-jumpOffset, currentCoord[1]+jumpOffset)
            },
            "Left": {
                "": (currentCoord[0], currentCoord[1]-jumpOffset),
                "Left": (currentCoord[0]+jumpOffset, currentCoord[1]-jumpOffset),
                "Right": (currentCoord[0]-jumpOffset, currentCoord[1]-jumpOffset)
            },
            "Down": {
                "": (currentCoord[0]+jumpOffset, currentCoord[1]),
                "Left": (currentCoord[0]+jumpOffset, currentCoord[1]+jumpOffset),
                "Right": (currentCoord[0]+jumpOffset, currentCoord[1]-jumpOffset)
            },
            "Right": {
                "": (currentCoord[0], currentCoord[1]+jumpOffset),
                "Left": (currentCoord[0]-jumpOffset, currentCoord[1]+jumpOffset),
                "Right": (currentCoord[0]+jumpOffset, currentCoord[1]+jumpOffset)
            }
        }

        secondMoveKey = ""
        if secondMove == 0:
            secondMoveKey = "Left"
        elif secondMove == 1:
            secondMoveKey = "Right"
        direction1 = self.getDirection(currentCoord, nextCoord)
        return moveMap[direction1][secondMoveKey]

    def wallCollide(self, currentCoord: tuple[int, int], nextCoord: tuple[int, int], jump: bool = False) -> bool:
        """Return True if there is a wall between the currentCoord and the nextCoord"""
        CurrentCell = self.getCell(currentCoord)
        targetCell = self.getCell(nextCoord)

        if self.isValidWall(self.getDirection(currentCoord, nextCoord, True)):
            if targetCell.getWalls()[self.getDirection(currentCoord, nextCoord, True)]:
                return True
        if self.isValidWall(self.getDirection(currentCoord, nextCoord)):
            if CurrentCell.getWalls()[self.getDirection(currentCoord, nextCoord)]:
                return True

        if jump:
            jumpCoord = self.getCoordsFromDirection(currentCoord, nextCoord)
            if not self.inGrid(jumpCoord):
                return False
            jumpCell = self.getCell(jumpCoord)
            if self.isValidWall(self.getDirection(currentCoord, jumpCoord)):
                if (jumpCell.getWalls()[self.getDirection(currentCoord, jumpCoord)]):
                    return True
            if self.isValidWall(self.getDirection(currentCoord, jumpCoord, True)):
                if (jumpCell.getWalls()[self.getDirection(currentCoord, jumpCoord, True)]):
                    return True
        return False

    def placeBarrier(self, coord: tuple[int, int], direction: str, player: Player, place: bool = True) -> bool:
        """
        Place a barrier on the grid at the given coordinates and direction
        note that a barrier is only one cell wide

        place: if True, the barrier is placed on the grid
        else the barrier is not placed on the grid, the function only checks if the barrier can be placed
        """
        if self.detectBarrier(coord, direction):
            return False
        if self.ignoreSideBarrier(coord, direction):
            return False
        if player.getBarrier() == 0:
            return False

        if place:
            celWalls = self.getGrid()[coord[0]][coord[1]].getWalls()
            celWalls[direction] = True
            self.getGrid()[coord[0]][coord[1]].setWalls(celWalls)

        return True

    def placeWall(self, coord: tuple[int, int], direction: str, player: Player, place: bool = True, ignorePlayerBarriers: bool = False) -> bool:
        '''Place a wall on the grid

        a wall is considered to be a group of two barriers side by side
        '''
        if not self.placeBarrier(coord, direction, player, place=place):
            return False
        if not self.placeNeighborBarrier(coord, direction, place=place):
            if place:
                self.cancelBarrierPlacement(coord, direction)
            return False

        if place and not ignorePlayerBarriers:
            player.setBarrier(player.getBarrier()-1)
        return True

    def detectBarrier(self, coord: tuple[int, int], direction: str) -> bool:
        """Return True if there is a barrier at the given coordinates and direction"""
        return self.getGrid()[coord[0]][coord[1]].getWalls()[direction]

    def ignoreSideBarrier(self, coord: tuple[int, int], direction: str) -> bool:
        '''Return True if a barrier is on the side of the given coordinates'''
        if direction == 'Right':
            return coord[1] == self.getSquareWidth()
        return coord[0] == self.getSquareWidth()

    def cancelBarrierPlacement(self, coord: tuple[int, int], direction: str) -> None:
        '''Cancel the placement of a barrier'''

        walls = self.getGrid()[coord[0]][coord[1]].getWalls()
        walls[direction] = False
        self.getGrid()[coord[0]][coord[1]].setWalls(walls)

    def placeNeighborBarrier(self, coord: tuple[int, int], direction: str, place: bool = True) -> bool:
        '''Set the Barrier of the neighbors of the given coordinates and direction'''
        if (direction == 'Right'):
            # right neighbor
            if coord[0] >= len(self.getGrid())-1:
                return False
            neighborCoord = (coord[0]+1, coord[1])
        elif coord[1] >= len(self.getGrid())-1:
            return False
        else:
            neighborCoord = (coord[0], coord[1]+1)

        if self.detectBarrier(neighborCoord, direction):
            if place:
                self.cancelBarrierPlacement(neighborCoord, direction)
            return False

        return self.placeBarrier((neighborCoord[0], neighborCoord[1]),
                                 direction, self.getCurrentPlayer(), place=place)

    def cancelNeighborBarriers(self, coord: tuple[int, int], direction: str) -> None:
        '''Cancel the placement of the neighbor's barrier'''

        if (direction == 'Right'):
            if coord[0] >= len(self.getGrid())-1:
                return
            neighborCoord = (coord[0]+1, coord[1])
        elif coord[1] >= len(self.getGrid())-1:
            return
        else:
            neighborCoord = (coord[0], coord[1]+1)

        if self.detectBarrier(neighborCoord, direction):
            self.cancelBarrierPlacement(neighborCoord, direction)

    def playerCollide(self, coord: tuple[int, int]) -> bool:
        '''Check if a cell at given coord is occupied by a player'''
        return self.getCell(coord).getPlayer().getNumber() != 0

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
        return any(cell.getPlayer().getNumber() == playerN for cell in self.getGrid()[row])

    def checkPlayerInCol(self, playerN: int, col: int) -> bool:
        return any(row[col].getPlayer().getNumber() == playerN for row in self.getGrid())

    def winningSide(self, player: Player):
        '''Return the side that the player must reach to win'''
        direction = ["Down", "Up", "Right", "Left"]
        return direction[player.getNumber()-1]

    def getWinningLine(self, player: Player) -> int:
        '''Return the line that the player must reach to win'''
        if self.winningSide(player) in ["Down", "Right"]:
            return self.getSquareWidth()-1
        return 0

    def stuck(self) -> bool:
        """Check if the player is stuck"""
        for player in self.getPlayerList():
            coord = player.getCoordinates()
            self.getCell(coord).setVisited(True)

            if not self.stuckNeighbor(player, coord):
                self.resetVisited()
                return True
            self.resetVisited()

        return False

    def stuckNeighbor(self, player: Player, coord: tuple[int, int]) -> bool:
        """check if the player is stuck in the given coordinates"""
        if self.winningSide(player) in ["Up", "Down"]:
            if coord[0] == self.getWinningLine(player):
                return True
        if self.winningSide(player) in ["Left", "Right"]:
            if coord[1] == self.getWinningLine(player):
                return True

        for neighbor in self.getNeighbors(coord):
            if neighbor.getCoordinates() == player.getCoordinates():
                continue
            if self.wallCollide(coord, neighbor.getCoordinates()):
                continue
            if neighbor.getVisited():
                continue

            nextCellCoord = neighbor.getCoordinates()
            neighbor.setVisited(True)
            if nextCell := self.stuckNeighbor(player, nextCellCoord):
                return nextCell

        return False

    def resetVisited(self) -> None:
        '''Reset the visited attribute of all cells to False'''
        for row in self.getGrid():
            for cell in row:
                cell.setVisited(False)

    @ staticmethod
    def maxBarrier(key: int) -> int:
        '''Return the maximum number of barriers for the given square width'''
        numberMax = {5: 8, 7: 12, 9: 20, 11: 40}
        return numberMax[key]

    def possibleMoves(self, playerCoord: tuple[int, int]) -> list[tuple[int, int]]:
        '''Return a list of possible moves for the player'''
        result = list[tuple[int, int]]()
        for neighbor in self.getNeighbors(playerCoord):
            neighborCoord = neighbor.getCoordinates()
            if self.checkOrthogonalMove(neighborCoord, playerCoord):
                result.append(neighborCoord)
                continue

            if self.playerCollide(neighborCoord):
                jumpCoord = self.getCoordsFromDirection(
                    playerCoord, neighborCoord, jump=True)
                if self.checkJump(playerCoord, neighborCoord):
                    result.append(jumpCoord)
                    continue

                coordinatesAfterJump = self.getCoordsFromDirection(
                    playerCoord, jumpCoord, jump=True)
                if not self.inGrid(coordinatesAfterJump):
                    continue
                if (self.wallCollide(playerCoord, jumpCoord, True) or self.playerCollide(coordinatesAfterJump)):
                    for direction in range(2):
                        if self.checkDiagonalMove(playerCoord, neighborCoord, direction):
                            diagCoordinates = self.getCoordsFromDirection(
                                playerCoord, jumpCoord, direction)
                            if self.getCell(diagCoordinates).getPlayer().getNumber() == 0:
                                result.append(diagCoordinates)

        return result

    def checkBarrierIntersection(self, i: int, j: int, direction: str) -> bool:
        nbBarrier = 0
        if direction == 'Down':
            otherDirection = 'Right'
            while i-nbBarrier >= 0 and self.getGrid()[i-nbBarrier][j].getWalls()[otherDirection]:
                nbBarrier += 1
            if nbBarrier % 2 == 0:
                return False
            if self.getGrid()[i][j].getWalls()[otherDirection]:
                return True

        elif direction == 'Right':
            otherDirection = 'Down'
            while j-nbBarrier >= 0 and self.getGrid()[i][j-nbBarrier].getWalls()[otherDirection]:
                nbBarrier += 1
            if nbBarrier % 2 == 0:
                return False
            if self.getGrid()[i][j].getWalls()[otherDirection]:
                return True

        return False

    def possibleBarrierPlacement(self, player: Player) -> list[tuple[tuple[int, int], str]]:
        '''Return a list of possible coordinates for a barrier placement
        '''

        result = list[tuple[tuple[int, int], str]]()

        for i in range(len(self.getGrid())-1):
            for j in range(len(self.getGrid()[i])-1):
                cell = self.getGrid()[i][j]
                for direction in cell.getWalls().keys():
                    if direction not in ['Down', 'Right']:
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
                    self.cancelNeighborBarriers((i, j), direction)
        return result

    def movePlayer(self, player: Player, coord: tuple[int, int]) -> None:
        '''moves the player to the given coordinates'''
        self.placePlayer(Player(0), player.getCoordinates())
        self.placePlayer(player, coord)

    def directionInput(self) -> str:
        '''Return the direction input by the user or False if the input is invalid'''
        directions = list(self.getGrid()[0][0].getWalls().keys())
        while True:
            inp = input("Direction |Right or Down|").capitalize()
            if inp in directions:
                return inp

    @ staticmethod
    def intInput(message: str) -> int:
        '''Return an integer inputted by the user'''
        try:
            return int(input("\n" + message + ":  "))
        except ValueError:
            return Game.intInput("\nIncorrect Value, please enter a number")

    @ staticmethod
    def yesNoInput(message: str, inp1: str, inp2: str) -> bool:
        """Return a boolean inputted by the user

        True if the user inputted the first string, false if the user inputted the second string
        """
        while True:
            inp = input(f'\n {message}  : ({inp1[0]}/{inp2[0]})')
            if inp.lower() == inp1[0].lower():
                return True
            if inp.lower() == inp2[0].lower():
                return False


def initializeGame() -> Game:
    '''Initialize the game'''
    width = Game.intInput(
        "Select the size of the square you want to create, minimum 5, maximum 11. \nOnly odd numbers")
    nbPlayer = Game.intInput("How many players ? \nminimum 2, maximum 4")
    nbBarrier = Game.intInput("How many Barriers? \nminimum 4, maximum ")
    bots = Game.intInput("how many bots do you want to play against?")

    return Game(width, nbPlayer, nbBarrier, bots)


def main() -> None:
    '''
    Main function of the game loop in console,
    it is used to test the game logic in the console without the GUI
    '''
    currentGame = initializeGame()
    currentGame.display()

    while not currentGame.checkGameOver():
        player = currentGame.getCurrentPlayer()
        print(player)

        if isinstance(player, Bot):
            randomAction = player.randomAction(
                currentGame.possibleBarrierPlacement(player))
            if randomAction == 0:
                coord = player.randomMove(
                    currentGame.possibleMoves(player.getCoordinates()))
                currentGame.movePlayer(player, coord)
            elif randomAction == 1:
                coord, direction = player.randomBarrier(
                    currentGame.possibleBarrierPlacement(player))
                currentGame.placeWall(coord, direction, player)

        else:
            choice = Game.yesNoInput(
                'to place barrier enter "p"\n to play enter "m"', "p", "m")
            coord = (Game.intInput("row")-1, Game.intInput("Col")-1)
            if choice:
                direction = currentGame.directionInput()
                while not direction:
                    direction = currentGame.directionInput()

                while not currentGame.placeWall(coord, direction, player):
                    coord = (Game.intInput("row")-1, Game.intInput("Col")-1)
                    direction = currentGame.directionInput()

                player.setBarrier(player.getBarrier()-1)
            else:
                while coord not in currentGame.possibleMoves(player.getCoordinates()):
                    coord = (Game.intInput("row")-1, Game.intInput("Col")-1)
                currentGame.movePlayer(player, coord)

        currentGame.display()
        currentGame.nextPlayer()


if __name__ == "__main__":
    main()
