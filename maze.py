from enum import Enum
from pydantic import BaseModel


class Cell(Enum):
    empty = 1
    wall = 0

    def __bool__(self) -> bool:
        return bool(self.value)


class Maze(BaseModel):
    height: int
    width: int
    start: tuple[int, int]
    end: tuple[int, int]
    cells: list[list[Cell]]
