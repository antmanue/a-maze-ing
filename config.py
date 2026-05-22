#!/usr/bin/env python3


import typing


def read_config(file_name: str) -> dict[str, str]:
    with open(file_name) as file:
        config: dict[str, str] = {}
        for line in file.readlines():
            line = line.rstrip('\n')
            key, value = line.split('=')
            config[key] = value
        return config

#   Given the bit position from right to left, calculates the bit
#   value (0 or 1)
def calculate_bit(value: int, bit_pos: int) -> int:
    bit_weigth = 8
    iterations = [4, 3, 2, 1]
    for _ in range(iterations[bit_pos]):
        bit = int(value / bit_weigth)
        value = value % bit_weigth
        bit_weigth /= 2
    return bit


class Cell:
    def __init__(self, value: int, x: int, y: int) -> None:
        self.value = value
        self.west = calculate_bit(value, 3)
        self.south = calculate_bit(value, 2)
        self.east = calculate_bit(value, 1)
        self.north = calculate_bit(value, 0)
        self.x = x
        self.y = y

    def update_value(self, value: int):
        self.value = value    # 4 bits (WSEN) from 0 - 15 => (0000) - (1111)
        self.west = calculate_bit(value, 3)
        self.south = calculate_bit(value, 2)
        self.east = calculate_bit(value, 1)
        self.north = calculate_bit(value, 0)

    def set_bit(self, bit_pos: int, bit_value: int):
        bit_weigth: int = pow(2, bit_pos)
        if bit_value == 1:
            if calculate_bit(self.value, bit_pos) != 1:
                self.update_value(self.value + bit_weigth)
        else:
            if calculate_bit(self.value, bit_pos) != 0:
                self.update_value(self.value - bit_weigth)

    def get_bits(self) -> None:
        [print(calculate_bit(self.value, x), end='')
         for x in reversed(range(4))]
        # print()

    def print(self):
        # print(f"cell: {self.get_bits()}")
        self.print_if(self.north, "_")
        # print("\n          ", end='')
        self.print_if(self.west, '|')
        self.print_if(self.south, '_')
        self.print_if(self.east, "|\n")

    def print_if(self, exist: int, char: str):
        if exist:
            print(f"{char}", end='')
        else:
            print(" ", end='')

    def draw_if(self, exist: int, char: str):
        if exist:
            return f"{char}"
        else:
            return " "
