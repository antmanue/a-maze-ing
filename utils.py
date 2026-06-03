#!/usr/bin/env python3


class Cell:
    def __init__(self, value: int, x: int, y: int) -> None:
        self.value = value
        self.west = self.calculate_bit(3)
        self.south = self.calculate_bit(2)
        self.east = self.calculate_bit(1)
        self.north = self.calculate_bit(0)
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent: Cell | None = None
        self.coord = (self.x, self.y)

    def calculate_bit(self, bit_pos: int) -> int:
        bit_weigth = 8
        iterations = [4, 3, 2, 1]
        value = self.value
        bit = 0
        for _ in range(iterations[bit_pos]):
            bit = int(value / bit_weigth)
            value = value % bit_weigth
            bit_weigth = int(bit_weigth / 2)
        return bit

    def update_value(self, value: int) -> None:
        self.value = value    # 4 bits (WSEN) from 0-15 => (0000)-(1111)
        self.west = self.calculate_bit(3)
        self.south = self.calculate_bit(2)
        self.east = self.calculate_bit(1)
        self.north = self.calculate_bit(0)

    def set_bit(self, bit_pos: int, bit_value: int) -> None:
        bit_weigth: int = pow(2, bit_pos)
        if bit_value == 1:
            if self.calculate_bit(bit_pos) != 1:
                self.update_value(self.value + bit_weigth)
        else:
            if self.calculate_bit(bit_pos) != 0:
                self.update_value(self.value - bit_weigth)

    def get_bits(self) -> str:
        bits = [str(self.calculate_bit(x)) for x in reversed(range(4))]
        return ''.join(bits)

    def draw_if(self, direction: int, draw: str = "") -> str:
        dir = Directions()
        exist = self.calculate_bit(direction)
        output = ""
        if exist:
            if direction == dir.west or direction == dir.east:
                output = "|"
            elif direction == dir.south:
                if draw:
                    start_underline = "\033[4m"
                    end_underline = "\033[0m"
                    output = start_underline + draw + end_underline
                else:
                    output = "_"
        else:
            if len(draw) > 0:
                output = draw
            else:
                output = " "
        return output


class Directions:
    def __init__(self) -> None:
        self.west = 3   # Byte position 1000 of Wall
        self.south = 2  # Byte position 0100 of Wall
        self.east = 1   # Byte position 0010 of Wall
        self.north = 0  # Byte position 0001 of Wall

    def opposite(self, direction: int) -> int:
        oppos = [self.south, self.west, self.north, self.east]
        return oppos[direction]

    def between(self, orig: Cell, dest: Cell) -> int:
        if orig.x > dest.x:
            return self.west
        elif orig.y < dest.y:
            return self.south
        elif orig.x < dest.x:
            return self.east
        elif orig.y > dest.y:
            return self.north
        raise ValueError("Directions:between() - No walls in between "
                         f"{(orig.y, orig.x)} and {(dest.y, dest.x)}")

    def get_orientation(self, direction: int):
        orientation = ["N", "E", "S", "W"]
        return orientation[direction]


class Neighbour:
    def __init__(self, cell: Cell, direction: int) -> None:
        self.cell = cell
        # self.x = self.set_x(x, direction)
        # self.y = self.set_y(y, direction)
        self.x = self.set_x(direction)
        self.y = self.set_y(direction)
        self.coord = (self.x, self.y)

    # def set_x(self, x: int, direction: int) -> int:
    def set_x(self, direction: int) -> int:
        dir = Directions()
        if direction == dir.east:
            return self.cell.x + 1
            # return x + 1
        elif direction == dir.west:
            return self.cell.x - 1
            # return x - 1
        else:
            return self.cell.x
            # return x

    # def set_y(self, y: int, direction: int) -> int:
    def set_y(self, direction: int) -> int:
        dir = Directions()
        if direction == dir.north:
            return self.cell.y - 1
            # return y - 1
        elif direction == dir.south:
            return self.cell.y + 1
            # return y + 1
        else:
            return self.cell.y
            # return y
