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
        self.rows: list[list[conf.Cell]] = []
        self.output = self.generate_map()
        self.map = self.draw_map()
        self.generate_output()

    def __str__(self) -> str:
        return '\n'.join([self.output, self.map])

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
                if coord == self.entry:
                    fill = 'O'
                elif coord == self.exit:
                    fill = 'X'
                row_repr += cell.draw_if(cell.west, '|')
                if coord == self.entry or coord == self.exit:
                    if cell.south:
                        row_repr += cell.draw_if(cell.south, fill + '\u0332')
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
            columns: list[conf.Cell]= []
            row_output = ""
            self.rows.append(columns)
            for x in range(self.width):
                value = rand.randint(0, 15)
                cell = conf.Cell(value, x, y)
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

    def generate_borders(self, cell: conf.Cell) -> None:
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

    def validate_walls(self, cell: conf.Cell) -> None:
        west = 3
        north = 0
        up = cell.y - 1
        left = cell.x - 1
        # print(f"\n{cell.y}, {cell.x}")
        if up >= 0:
            # print(f"UP: {up} -> {up}, {cell.x}")
            upper_cell = self.rows[up][cell.x]
            self.check_wall(upper_cell, north, cell)
            # if conf.calculate_bit(upper_cell.value, south):
            #     cell.set_bit(north, 1)
        if left >= 0:
            # print(f"LEFT: {left} -> {cell.y}, {left}")
            left_cell = self.rows[cell.y][left]
            self.check_wall(left_cell, west, cell)
            # if conf.calculate_bit(left_cell.value, east):
            #     cell.set_bit(west, 1)

    def check_wall(self, neighboor: conf.Cell, where: int, cell: conf.Cell) -> None:
        west = 3
        south = 2
        east = 1
        north = 0
        if where == north:
            orientation = south
        elif where == west:
            orientation = east
        neighboor_wall = conf.calculate_bit(neighboor.value, orientation)
        cell_wall = conf.calculate_bit(cell.value, where)
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


if __name__ == "__main__":
    main()
