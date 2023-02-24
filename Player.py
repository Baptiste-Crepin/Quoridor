class Player():
    def __init__(self, number: int, barrer: int = 0):
        self.__number = number
        self.__barrier = barrer
        self.__color = self.setColorFromNumber()
        self.__coordinates = None

    def getNumber(self) -> int:
        return self.__number

    def getBarrier(self) -> int:
        return self.__barrier

    def getColor(self) -> str:
        return self.__color

    def getCoordinates(self) -> int:
        return self.__coordinates

    def setNumber(self, value: int) -> None:
        self.__number = value

    def setBarrier(self, value: int) -> None:
        self.__barrier = value

    def setColor(self, value: str) -> None:
        self.__color = value

    def setCoordinates(self, value: int) -> None:
        self.__coordinates = value

    def __repr__(self) -> str:
        return str(self.getNumber())

    def setColorFromNumber(self) -> None:
        RED = "#fe001c"
        YELLOW = "#efe743"
        GREEN = "#639d39"
        BLUE = "#1a6baa"
        COLORLIST = [RED, YELLOW, GREEN, BLUE]

        return COLORLIST[self.getNumber()-1]
