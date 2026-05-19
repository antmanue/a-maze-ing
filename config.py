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


class Cell:
    def __init__(self, west: int, south:int, east:int, north: int) -> None:
        self.west = west
        self.south = south
        self.east = east
        self.north = north
        self.bits = west * 8 + south * 4 + east * 2 + north

    def set_walls(self, bits: int):
        self.bits = bits
        self.west = int(bits / 8)
        self.south = int((bits % 8) / 4)
        self.east = int(((bits % 8) % 4) / 2)
        self.north = int((((bits % 8) % 4) % 2) / 1)

    def get_bits(self):
        print(f"cell: {self.west}{self.south}{self.east}{self.north} ", end='')
        self.print_if(self.north, "_")
        print("\n          ", end='')
        self.print_if(self.west, '|')
        self.print_if(self.south, '_')
        self.print_if(self.east, "|\n")
    
    def print_if(self, exist: int, char: str):
        if exist:
            print(f"{char}", end='')
        else:
            print(" ", end='')
