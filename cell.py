from player import Player


class Cell():

    def __init__(self, coordinates: tuple[int, int], player: Player) -> None:
        self.__coordinates = coordinates
        self.__player = player
        self.__walls = {"Down": False, "Right": False}
        self.__visited = False

    def getCoordinates(self) -> tuple[int, int]:
        return self.__coordinates

    def getPlayer(self) -> Player:
        return self.__player

    def getWalls(self) -> dict[str, bool]:
        return self.__walls

    def getVisited(self) -> bool:
        return self.__visited

    def setCoordinates(self, value: tuple[int, int]) -> None:
        self.__coordinates = value

    def setPlayer(self, value: Player) -> None:
        self.__player = value

    def setWalls(self, value: dict[str, bool]) -> None:
        self.__walls = value

    def setVisited(self, value: bool) -> None:
        self.__visited = value

    def __repr__(self) -> str:
        return str(self.getPlayer())
