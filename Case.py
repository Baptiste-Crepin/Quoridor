class Case():

    def __init__(self, pawnNumber: int, coordinates: tuple, player: object) -> None:
        self.__coordinates = coordinates
        self.__player = player
        self.__walls = [0, 0, 0, 0]  # N W S E

    def getCoordinates(self) -> int:
        return self.__coordinates

    def getPlayer(self) -> int:
        return self.__player

    def getWalls(self) -> list:
        return self.__walls

    def setCoordinates(self, value: int) -> None:
        self.__coordinates = value

    def setPlayer(self, value: object) -> None:
        self.__player = value

    def setWalls(self, value: list) -> None:
        self.__walls = value

    def __repr__(self) -> str:
        return str(self.getPlayer())
