import pygame
from gameLogic.game import Game
from graphical.menus.board import Board
from gameLogic.bot import Bot
from gameLogic.player import Player
from graphical.menus.endGame import End


class LocalGame():
    """This class is the main class of the game. It handles the game logic and the graphical interface."""

    def __init__(self, width, nbPlayer, nbBarrier, nbBots, score: list[int] = [0, 0, 0, 0], fullScreen: bool = False) -> None:
        """Initializes the game"""
        self.game = Game(width, nbPlayer, nbBarrier, nbBots)
        self.score = score
        self.board = Board(self.game.getSquareWidth(), score, fullScreen)
        self.newTurn = True

        pygame.mixer.init()
        self.barrierPlacementSound = pygame.mixer.Sound(
            './assets/sounds/barrierPlacement.wav')
        self.movementSound = pygame.mixer.Sound(
            './assets/sounds/movement.wav')

    def highlightPlayer(self, player: Player):
        """Highlights the possible moves of a player"""
        for PossibleMoveCoord in self.game.possibleMoves(player.getCoordinates()):
            self.board.rect[PossibleMoveCoord[1]
                            ][PossibleMoveCoord[0]].highlighted = True

    def highlightBarrier(self):
        """Highlights the possible placements of a barrier"""
        for (possibleBarrierCoord, direction) in self.game.possibleBarrierPlacement(self.game.getCurrentPlayer()):
            if direction == 'Right':
                self.board.verticalBarriers[possibleBarrierCoord[1]
                                            ][possibleBarrierCoord[0]].possiblePlacement = True
            self.board.horizontalBarriers[possibleBarrierCoord[1]
                                          ][possibleBarrierCoord[0]].possiblePlacement = True

    def displayPossibleMoves(self, player: Player):
        """Displays the possible moves of a player at the beginning of his turn"""
        if not self.newTurn:
            return
        self.newTurn = False
        if not isinstance(player, Bot):
            self.highlightPlayer(player)
            self.highlightBarrier()

    def actualizeGame(self):
        """Updates the game with the current state of the board"""
        for i, row in enumerate(self.game.getGrid()):
            for j, cell in enumerate(row):

                self.board.rect[j][i].player = cell.getPlayer()

                if i < len(self.game.getGrid())-1:
                    self.board.horizontalBarriers[j][i].placed = cell.getWalls()[
                        'Down']

                if j < len(row)-1:
                    self.board.verticalBarriers[j][i].placed = cell.getWalls()[
                        'Right']

    def placement(self, currentPlayer: Player):
        """Handles the placement of a barrier or a player"""
        player = self.game.getCurrentPlayer()
        if isinstance(player, Bot):
            return self.botMovement(player)
        # if the player doesn't click on the board, we don't do anything
        event = self.board.handleEvents()
        if not event:
            return

        (action, x, y) = event
        clickCoord = (x, y)

        if action == 'TablePlayer':
            # if the player clicks on a cell that is not a possible move, we don't do anything
            if clickCoord not in self.game.possibleMoves(currentPlayer.getCoordinates()):
                return

            # if the player clicks on a cell that is a possible move, we move the player
            self.board.clearHover(self.board.rect)
            self.game.movePlayer(currentPlayer, clickCoord)
            self.movementSound.play()

        if action == 'VerticalBarrier':
            # if the player clicks on a barrier that is not a possible placement, we don't do anything
            if (clickCoord, 'Right') not in self.game.possibleBarrierPlacement(currentPlayer):
                return
            # if the player clicks on a barrier that is a possible placement, we place the barrier
            self.game.placeWall(clickCoord, 'Right',
                                currentPlayer, place=True)
            self.barrierPlacementSound.play()

        if action == 'HorizontalBarrier':
            # if the player clicks on a barrier that is not a possible placement, we don't do anything
            if (clickCoord, 'Down') not in self.game.possibleBarrierPlacement(currentPlayer):
                return

            # if the player clicks on a barrier that is a possible placement, we place the barrier
            self.game.placeWall(clickCoord, 'Down', currentPlayer)
            self.barrierPlacementSound.play()

        # a legal move has been made, we clear the highlights and change the player
        self.board.clearAllHighlight()
        self.game.nextPlayer()
        self.newTurn = True

    def botMovement(self, player: Bot):
        # Logic for the bot to play
        self.board.newFrame(player, self.game.getPlayerList())
        randomAction = player.randomAction(
            self.game.possibleBarrierPlacement(player))
        if randomAction == 0:
            coord = player.randomMove(
                self.game.possibleMoves(player.getCoordinates()))
            self.game.movePlayer(player, coord)
        elif randomAction == 1:
            coord, direction = player.randomBarrier(
                self.game.possibleBarrierPlacement(player))
            self.game.placeWall(coord, direction, player)

        self.game.nextPlayer()
        self.newTurn = True
        return

    def mainLoop(self) -> None:
        """Main loop of the game"""
        self.highlightPlayer(self.game.getCurrentPlayer())
        self.highlightBarrier()
        while not self.game.checkGameOver():
            self.displayPossibleMoves(self.game.getCurrentPlayer())

            self.placement(self.game.getCurrentPlayer())
            self.actualizeGame()

            self.board.newFrame(self.game.getCurrentPlayer(),
                                self.game.getPlayerList())

        endWindow = End(self.game.getPreviousPlayer(),
                        self.game.getSquareWidth(),
                        self.game.getNumberOfPlayers(),
                        self.game.getNumberOfBarriers(),
                        self.game.getNumberOfBots(),
                        self.score,
                        self.board.fullScreen)
        while True:
            endWindow.mainLoop()
            pygame.display.update()


if __name__ == "__main__":
    width = 11
    nbBarrier = 4
    nbPlayer = 2
    nbBot = 2
    G = LocalGame(width, nbPlayer, nbBarrier, nbBot)
    G.mainLoop()
