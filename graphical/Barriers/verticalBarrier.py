from .barrier import Barrier


class VerticalBarrier(Barrier):
    def __init__(self, boardX, boardY, col, i: int = 0, j: int = 0):
        super().__init__(boardX, boardY, col, i, j)

    def setWidth(self) -> int:
        return self.cellTemplate.offset

    def setHeight(self) -> int:
        return self.cellTemplate.width-self.cellTemplate.offset

    def coordX(self, i: int) -> float:
        return self.cellTemplate.height * (i+1)-self.cellTemplate.offset/2

    def coordY(self, j: int) -> float:
        return self.cellTemplate.coord(j)+self.cellTemplate.offset/2
