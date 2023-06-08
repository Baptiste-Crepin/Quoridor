from .barrier import Barrier


class VerticalBarrier(Barrier):
    """
    child of the barriers class
    This class handles the graphical placement of the vertical barriers.
    """

    def __init__(self, boardX: int, boardY: int, col: int, i: int = 0, j: int = 0) -> None:
        """Initializes the parent class with the correct parameters"""
        super().__init__(boardX, boardY, col, i, j)

    def setWidth(self) -> int:
        """sets the width of the barrier"""
        return self.cellTemplate.offset

    def setHeight(self) -> int:
        """sets the height of the barrier"""
        return self.cellTemplate.width-self.cellTemplate.offset

    def coordX(self, i: int) -> float:
        """sets the x coordinate of the barrier"""
        return self.cellTemplate.height * (i+1)-self.cellTemplate.offset/2

    def coordY(self, j: int) -> float:
        """sets the y coordinate of the barrier"""
        return self.cellTemplate.coord(j)+self.cellTemplate.offset/2
