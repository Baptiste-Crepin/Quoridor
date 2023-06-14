class Player():
    def __init__(self, number: int, barrier: int = 0):
        self.__number = number
        self.__barrier = barrier
        self.__color = self.setColorFromNumber()
        self.__coordinates = (0, 0)

    def getNumber(self) -> int:
        return self.__number

    def getBarrier(self) -> int:
        return self.__barrier

    def getColor(self) -> str:
        return self.__color

    def getCoordinates(self) -> tuple[int, int]:
        return self.__coordinates

    def setNumber(self, value: int) -> None:
        self.__number = value

    def setBarrier(self, value: int) -> None:
        self.__barrier = value

    def setColor(self, value: str) -> None:
        self.__color = value

    def setCoordinates(self, value: tuple[int, int]) -> None:
        self.__coordinates = value

    def __repr__(self) -> str:
        return str(self.getNumber())

    def stringColor(self) -> str:
        colorList = {"#fe001c": "RED",
                     "#efe743": "YELLOW",
                     "#639d39": "GREEN",
                     "#1a6baa": "BLUE"}
        return colorList[self.getColor()]

    def setColorFromNumber(self) -> str:
        RED = "#fe001c"
        YELLOW = "#efe743"
        GREEN = "#639d39"
        BLUE = "#1a6baa"
        COLORLIST = [RED, YELLOW, GREEN, BLUE]

        return COLORLIST[self.getNumber()-1]
