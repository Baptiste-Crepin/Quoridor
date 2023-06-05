from .barrier import Barrier


class HorizontalBarrier(Barrier):
    def __init__(self, boardX: int, boardY: int, col: int, i: int = 0, j: int = 0) -> None:
        super().__init__(boardX, boardY, col, i, j)

    def setWidth(self) -> int:
        return self.cellTemplate.width-self.cellTemplate.offset

    def setHeight(self) -> int:
        return self.cellTemplate.offset

    def coordX(self, i: int) -> float:
        return self.cellTemplate.coord(i) + self.cellTemplate.offset/2

    def coordY(self, j: int) -> float:
        return self.cellTemplate.width * (j+1)-self.cellTemplate.offset/2
