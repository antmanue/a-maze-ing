#!/usr/bin/env python3


import config as conf
import random as rand
import sys


class MazeGenerator:
    def __init__(self, config: dict[str, str]) -> None:
        self.width = int(config["WIDTH"])
        self.height = int(config["HEIGHT"])
        self.entry = tuple([int(coordinate) for coordinate in
                            config["ENTRY"].split(',')])
        self.exit = tuple([int(coordinate) for coordinate in
                           config["EXIT"].split(',')])
        self.output_file = config["OUTPUT_FILE"]
        self.perfect = bool(config["PERFECT"])
        self.rows: list[list[MazeGenerator.Cell]] = []
        self.output = self.generate_map()
        self.map = self.draw_map()
        self.generate_output()

    def __str__(self) -> str:
        return '\n'.join([self.output, self.map])

    
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

        def update_value(self, value: int):
            self.value = value    # 4 bits (WSEN) from 0 - 15 => (0000) - (1111)
            self.west = self.calculate_bit(value, 3)
            self.south = self.calculate_bit(value, 2)
            self.east = self.calculate_bit(value, 1)
            self.north = self.calculate_bit(value, 0)

        def set_bit(self, bit_pos: int, bit_value: int):
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

        def draw_if(self, exist: int, char: str):
            if exist:
                return f"{char}"
            else:
                return " "

    def show_config(self) -> None:
        print(f"WIDTH: {self.width} ({type(self.width)})")
        print(f"HEIGHT: {self.height} ({type(self.height)})")
        print("ENTRY: ", end='')
        [print(f"{coordinate} ({type(coordinate)}) ", end='') for coordinate
         in self.entry]
        print("\nEXIT: ", end='')
        [print(f"{coordinate} ({type(coordinate)}) ", end='') for coordinate
         in self.exit]
        print(f"\nOUTPUT_FILE: {self.output_file} ({type(self.output_file)})")
        print(f"PERFECT: {self.perfect} ({type(self.perfect)})")

    def draw_map(self) -> str:
        map: list[str] = []
        for row in self.rows:
            if row[0].y == 0:   # first_row
                row_repr = ' '
                for cell in row:
                    if cell.y == 0 and cell.north:
                        row_repr += "_ "
                map.append(row_repr)
            row_repr = ""
            for cell in row:
                coord = (cell.x, cell.y)
                fill = ""
                if coord == self.entry:
                    fill = 'O'
                elif coord == self.exit:
                    fill = 'X'
                row_repr += cell.draw_if(cell.west, '|')
                if coord == self.entry or coord == self.exit:
                    if cell.south:
                        row_repr += cell.draw_if(cell.south, "\033[4m" + fill + "\033[0m")
                    else:
                        row_repr += fill
                else:
                    row_repr += cell.draw_if(cell.south, '_')
                if cell.x == self.width - 1:
                    row_repr += cell.draw_if(cell.east, '|')
            map.append(row_repr)
        return '\n'.join(map)

    def generate_output(self) -> None:
        with open(self.output_file, 'w') as file:
            file.write(self.output + '\n\n')
            file.write(str(self.entry) + '\n')
            file.write(str(self.exit))

    def generate_map(self) -> str:
        output: list[str] = []
        for y in range(self.height):
            columns: list[MazeGenerator.Cell]= []
            row_output = ""
            self.rows.append(columns)
            for x in range(self.width):
                value = rand.randint(0, 15)
                cell = MazeGenerator.Cell(value, x, y)
                self.generate_borders(cell)
                # columns.append(cell)
                # print("Prev - ", end='')
                # [print(hex(x.value).split('0x')[1].upper(), end='') for x in columns]
                # print()
                # print(self.draw_map())
                self.validate_walls(cell)
                # columns.pop()
                columns.append(cell)
                # print("Later - ", end='')
                # [print(hex(x.value).split('0x')[1].upper(), end='') for x in columns]
                # print()
                # print(self.draw_map())
                # print("--------------")
                row_output += hex(cell.value).split('0x')[1].upper()
            output.append(row_output)
        return '\n'.join(output)

    def generate_borders(self, cell: Cell) -> None:
        west = 3
        south = 2
        east = 1
        north = 0
        if cell.y == 0:
            cell.set_bit(north, 1)
        if cell.y == self.height - 1:
            cell.set_bit(south, 1)
        if cell.x == 0:
            cell.set_bit(west, 1)
        if cell.x == self.width - 1:
            cell.set_bit(east, 1)

    def validate_walls(self, cell: Cell) -> None:
        west = 3
        north = 0
        up = cell.y - 1
        left = cell.x - 1
        if up >= 0:
            upper_cell = self.rows[up][cell.x]
            self.check_wall(upper_cell, north, cell)
        if left >= 0:
            left_cell = self.rows[cell.y][left]
            self.check_wall(left_cell, west, cell)

    def check_wall(self, neighboor: Cell, where: int, cell: Cell) -> None:
        west = 3
        south = 2
        east = 1
        north = 0
        orientation = -1
        if where == north:
            orientation = south
        elif where == west:
            orientation = east
        neighboor_wall = MazeGenerator.Cell.calculate_bit(neighboor.value, orientation)
        cell_wall = MazeGenerator.Cell.calculate_bit(cell.value, where)
        if neighboor_wall != cell_wall:
            cell.set_bit(where, neighboor_wall)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return
    file = sys.argv[1]
    config = conf.read_config(file)
    maze = MazeGenerator(config)
    maze.show_config()
    print()

    print(maze)
    print()


if __name__ == "__main__":
    main()
