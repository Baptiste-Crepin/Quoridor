class Case():

    def __init__(self, pawnNumber: int, coordinates: tuple, player: object) -> None:
        self.__coordinates = coordinates
        self.__player = player
        self.__walls = {"Up": 1, "Left": 0, "Down": 0, "Right": 0}

    def getCoordinates(self) -> tuple:
        return self.__coordinates

    def getPlayer(self) -> int:
        return self.__player

    def getWalls(self) -> list:
        return self.__walls

    def setCoordinates(self, value: tuple) -> None:
        self.__coordinates = value

    def setPlayer(self, value: object) -> None:
        self.__player = value

    def setWalls(self, value: list) -> None:
        self.__walls = value

    def __repr__(self) -> str:
        return str(self.getPlayer())
