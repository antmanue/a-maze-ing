#!/usr/bin/env python3


class Config:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.width: int = 0
        self.height: int = 0
        self.entry: tuple[int, int] = ()
        self.exit: tuple[int, int] = ()
        self.output_file: str = ""
        self.perfect: bool = 0
        self.content = self.read_config(file_name)

    def print(self) -> None:
        print(f"WIDTH = {self.width} ({type(self.width)})")
        print(f"HEIGHT = {self.height} ({type(self.height)})")
        print(f"ENTRY = {self.entry} ({type(self.entry[0])}, "
              f"{type(self.entry[1])})")
        print(f"EXIT = {self.exit} ({type(self.exit[0])}, "
              f"{type(self.exit[1])})")
        print(f"OUTPUT_FILE = {self.output_file} ({type(self.output_file)})")
        print(f"PERFECT = {self.perfect} ({type(self.perfect)})")

    def setup(self) -> None:
        config = self.read_config(self.file_name)
        self.parse_config(config)


    def read_config(self, file_name: str) -> dict[str, str]:
        with open(file_name) as file:
            config: dict[str, str] = {}
            for line in file.readlines():
                line = line.rstrip('\n')
                key, value = line.split('=')
                config[key] = value
            return config

    def parse_config(self, config: dict[str, str]) -> None:
        self.width = self.validate_pos_int("WIDTH", config["WIDTH"])
        self.height = self.validate_pos_int("HEIGHT", config["HEIGHT"])
        self.entry = tuple([self.validate_pos_int("ENTRY", coordinate)
                            for coordinate in config["ENTRY"].split(',')])
        self.exit = tuple([self.validate_pos_int("EXIT", coordinate)
                            for coordinate in config["EXIT"].split(',')])
        self.output_file = self.validate_str("OUTPUT_FILE",
                                                 config["OUTPUT_FILE"])
        self.perfect = self.validate_bool("PERFECT", config["PERFECT"])

    def validate_pos_int(self, key: str, value: int) -> int:
        try:
            arg: int = int(value)
            if arg < 0:
                # raise(ValueError(f"Error found in '{key}' at '{self.file_name}': positive integer expected, found {arg}"))
                raise(ValueError(f"positive integer expected, found {arg}"))
        except ValueError as err:
            print(f"Error found in '{key}' at '{self.file_name}': {err}")
        return arg

    def validate_str(self, key: str, value: str) -> str:
        try:
            arg = str(value)
        except ValueError as err:
            print(f"Error found in {key}: {err}")
        return arg

    def validate_bool(self, key: str, value: bool) -> bool:
        try:
            arg = bool(value)
        except ValueError as err:
            print(f"Error found in {key}: {err}")
        return arg


class Cell:
    def __init__(self, value: int, x: int, y: int) -> None:
        self.value = value
        # self.west = self.calculate_bit(value, 3)
        # self.south = self.calculate_bit(value, 2)
        # self.east = self.calculate_bit(value, 1)
        # self.north = self.calculate_bit(value, 0)
        self.west = self.calculate_bit(3)
        self.south = self.calculate_bit(2)
        self.east = self.calculate_bit(1)
        self.north = self.calculate_bit(0)
        self.x = x
        self.y = y

    # @staticmethod
    # #   Given the bit position from right to left, calculates the bit
    # #   value (0 or 1)
    # def calculate_bit(value: int, bit_pos: int) -> int:
    #     bit_weigth = 8
    #     iterations = [4, 3, 2, 1]
    #     bit = 0
    #     for _ in range(iterations[bit_pos]):
    #         bit = int(value / bit_weigth)
    #         value = value % bit_weigth
    #         bit_weigth = int(bit_weigth / 2)
    #     return bit
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
        # self.west = self.calculate_bit(value, 3)
        # self.south = self.calculate_bit(value, 2)
        # self.east = self.calculate_bit(value, 1)
        # self.north = self.calculate_bit(value, 0)
        self.west = self.calculate_bit(3)
        self.south = self.calculate_bit(2)
        self.east = self.calculate_bit(1)
        self.north = self.calculate_bit(0)

    def set_bit(self, bit_pos: int, bit_value: int) -> None:
        bit_weigth: int = pow(2, bit_pos)
        if bit_value == 1:
            # if self.calculate_bit(self.value, bit_pos) != 1:
            if self.calculate_bit(bit_pos) != 1:
                self.update_value(self.value + bit_weigth)
        else:
            # if self.calculate_bit(self.value, bit_pos) != 0:
            if self.calculate_bit(bit_pos) != 0:
                self.update_value(self.value - bit_weigth)

    def get_bits(self) -> None:
        # [print(self.calculate_bit(self.value, x), end='')
        [print(self.calculate_bit(x), end='')
            for x in reversed(range(4))]

    def draw_if(self, direction: int, draw: str = None) -> str:
        dir = Directions()
        exist = self.calculate_bit(direction)
        if exist:
            if direction == dir.west or direction == dir.east:
                return "|"
            elif direction == dir.south:
                if draw:
                    start_underline = "\033[4m"
                    end_underline = "\033[0m"
                    return start_underline + draw + end_underline
                else:
                    return "_"
        else:
            if draw:
                return draw
            else:
                return " "


class Directions:
    def __init__(self) -> None:
        self.west = 3
        self.south = 2
        self.east = 1
        self.north = 0

    def opposite(self, direction: int) -> int:
        oppos = [self.south, self.west, self.north, self.east]
        return oppos[direction]
