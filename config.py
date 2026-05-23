#!/usr/bin/env python3


def read_config(file_name: str) -> dict[str, str]:
    with open(file_name) as file:
        config: dict[str, str] = {}
        for line in file.readlines():
            line = line.rstrip('\n')
            key, value = line.split('=')
            config[key] = value
        return config


class Cell:
    def __init__(self, value: int, x: int, y: int) -> None:
        self.value = value
        self.west = self.calculate_bit(value, 3)
        self.south = self.calculate_bit(value, 2)
        self.east = self.calculate_bit(value, 1)
        self.north = self.calculate_bit(value, 0)
        self.x = x
        self.y = y

    @staticmethod
    #   Given the bit position from right to left, calculates the bit
    #   value (0 or 1)
    def calculate_bit(value: int, bit_pos: int) -> int:
        bit_weigth = 8
        iterations = [4, 3, 2, 1]
        bit = 0
        for _ in range(iterations[bit_pos]):
            bit = int(value / bit_weigth)
            value = value % bit_weigth
            bit_weigth = int(bit_weigth / 2)
        return bit

    def update_value(self, value: int) -> None:
        self.value = value    # 4 bits (WSEN) from 0-15 => (0000)-(1111)
        self.west = self.calculate_bit(value, 3)
        self.south = self.calculate_bit(value, 2)
        self.east = self.calculate_bit(value, 1)
        self.north = self.calculate_bit(value, 0)

    def set_bit(self, bit_pos: int, bit_value: int) -> None:
        bit_weigth: int = pow(2, bit_pos)
        if bit_value == 1:
            if self.calculate_bit(self.value, bit_pos) != 1:
                self.update_value(self.value + bit_weigth)
        else:
            if self.calculate_bit(self.value, bit_pos) != 0:
                self.update_value(self.value - bit_weigth)

    def get_bits(self) -> None:
        [print(self.calculate_bit(self.value, x), end='')
            for x in reversed(range(4))]

    def draw_if(self, exist: int, char: str) -> str:
        if exist:
            return f"{char}"
        else:
            return " "


class Directions:
    def __init__(self) -> None:
        self.west = 3
        self.south = 2
        self.east = 1
        self.north = 0
