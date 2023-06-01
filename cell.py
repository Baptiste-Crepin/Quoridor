from Player import Player


class Cell():

    def __init__(self, coordinates: tuple, player: Player) -> None:
        self.__coordinates = coordinates
        self.__player = player
        self.__walls = {"Down": 0, "Right": 0}
        self.__visited = False

    def getCoordinates(self) -> tuple:
        return self.__coordinates

    def getPlayer(self) -> Player:
        return self.__player

    def getWalls(self) -> dict[str, int]:
        return self.__walls

    def getVisited(self) -> bool:
        return self.__visited

    def setCoordinates(self, value: tuple) -> None:
        self.__coordinates = value

    def setPlayer(self, value: Player) -> None:
        self.__player = value

    def setWalls(self, value: dict[str, int]) -> None:
        self.__walls = value

    def setVisited(self, value: bool) -> None:
        self.__visited = value

    def __repr__(self) -> str:
        return str(self.getPlayer())
