#!/usr/bin/env python3

from enum import IntEnum


class Cell:
    """Represents an individual coordinate element in the grid."""
    def __init__(self, value: int, x: int, y: int) -> None:
        """Initializes cell boundaries, coordinate and solving attributes."""
        self.value = value
        self.x = x
        self.y = y
        self.coord = (self.x, self.y)

        # Attributes for A* algorithm
        self.f = float('inf')
        self.g = float('inf')
        self.h = float('inf')
        self.parent: Cell | None = None

    def calculate_bit(self, bit_pos: int) -> int:
        """Extracts explicit wall state flags matching index keys."""
        bit_weigth = 8
        iterations = [4, 3, 2, 1]
        value = self.value
        bit = 0
        for _ in range(iterations[bit_pos]):
            bit = int(value / bit_weigth)
            value = value % bit_weigth
            bit_weigth = int(bit_weigth / 2)
        return bit

    def get_neighbour_coords(self, direction: int) -> tuple[int, int]:
        """Calculates relative neighbor location tracking elements."""
        x: int
        y: int
        if direction == Directions.EAST:
            x = self.x + 1
        elif direction == Directions.WEST:
            x = self.x - 1
        else:
            x = self.x

        if direction == Directions.NORTH:
            y = self.y - 1
        elif direction == Directions.SOUTH:
            y = self.y + 1
        else:
            y = self.y

        return (x, y)

    def update_value(self, value: int) -> None:
        """Updates the integer mask tracking current cell walls."""
        self.value = value

    def set_bit(self, bit_pos: int, bit_value: int) -> None:
        """Modifies wall and sync correspondent neighbour's wall."""
        bit_weigth: int = pow(2, bit_pos)
        if bit_value == 1:
            if self.calculate_bit(bit_pos) != 1:
                self.update_value(self.value + bit_weigth)
        else:
            if self.calculate_bit(bit_pos) != 0:
                self.update_value(self.value - bit_weigth)


class Directions(IntEnum):
    """Maps coordinate directions to integer identifiers."""
    WEST = 3   # Byte position 1000 of Wall
    SOUTH = 2  # Byte position 0100 of Wall
    EAST = 1   # Byte position 0010 of Wall
    NORTH = 0  # Byte position 0001 of Wall

    @classmethod
    def opposite(cls, direction: int) -> int:
        """Returns inverse of current direction."""
        oppos = [Directions.SOUTH, Directions.WEST,
                 Directions.NORTH, Directions.EAST]
        return oppos[direction]

    @classmethod
    def between(cls, orig: Cell, dest: Cell) -> 'Directions':
        """Identifies direction between two consecutive cells."""
        if orig.x > dest.x:
            return Directions.WEST
        elif orig.y < dest.y:
            return Directions.SOUTH
        elif orig.x < dest.x:
            return Directions.EAST
        elif orig.y > dest.y:
            return Directions.NORTH
        raise ValueError("Directions:between() - No walls in between "
                         f"{(orig.y, orig.x)} and {(dest.y, dest.x)}")

    @classmethod
    def get_orientation(cls, direction: int) -> str:
        """Translate direction into cardinal abbreviation string."""
        orientation = ["N", "E", "S", "W"]
        return orientation[direction]
