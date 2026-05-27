#!/usr/bin/env python3


class Directions:
    def __init__(self) -> None:
        self.west = 3
        self.south = 2
        self.east = 1
        self.north = 0

    def opposite(self, direction: int) -> int:
        oppos = [self.south, self.west, self.north, self.east]
        return oppos[direction]


class Cell:
    def __init__(self, value: int, x: int, y: int) -> None:
        self.value = value
        self.west = self.calculate_bit(3)
        self.south = self.calculate_bit(2)
        self.east = self.calculate_bit(1)
        self.north = self.calculate_bit(0)
        self.x = x
        self.y = y

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

    def get_bits(self) -> None:
        [print(self.calculate_bit(x), end='')
            for x in reversed(range(4))]

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
