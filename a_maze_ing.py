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
        self.initial_state = ""
        self.map_hex = ""
        self.generate_map()

    def __str__(self) -> str:
        return '\n'.join([self.map_hex, self.draw_map()])

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

    def generate_map(self) -> None:
        for y in range(self.height):
            columns: list[conf.Cell] = []
            self.rows.append(columns)
            for x in range(self.width):
                value = rand.randint(0, 15)
                cell = conf.Cell(value, x, y)
                columns.append(cell)
        self.initial_state += self.generate_hex() + '\n'
        self.initial_state += self.draw_map()
        self.normalize_map()
        self.map_hex = self.generate_hex()
        self.generate_output()

    def normalize_map(self) -> None:
        for row in self.rows:
            for cell in row:
                self.generate_borders(cell)
                self.validate_walls(cell)

    def generate_borders(self, cell: conf.Cell) -> None:
        dir = conf.Directions()
        if cell.y == 0:
            cell.set_bit(dir.north, 1)
        if cell.y == self.height - 1:
            cell.set_bit(dir.south, 1)
        if cell.x == 0:
            cell.set_bit(dir.west, 1)
        if cell.x == self.width - 1:
            cell.set_bit(dir.east, 1)

    def validate_walls(self, cell: conf.Cell) -> None:
        dir = conf.Directions()
        up = cell.y - 1
        left = cell.x - 1
        if up >= 0:
            upper_cell = self.rows[up][cell.x]
            self.enforce_shared_walls(upper_cell,
                                      dir.north, cell)
        if left >= 0:
            left_cell = self.rows[cell.y][left]
            self.enforce_shared_walls(left_cell,
                                      dir.west, cell)

    def enforce_shared_walls(self, neighboor: conf.Cell, where: int,
                             cell: conf.Cell) -> None:
        dir = conf.Directions()
        orientation = -1
        if where == dir.north:
            orientation = dir.south
        elif where == dir.west:
            orientation = dir.east
        neighboor_wall = cell.calculate_bit(neighboor.value, orientation)
        cell_wall = cell.calculate_bit(cell.value, where)
        if neighboor_wall != cell_wall:
            cell.set_bit(where, neighboor_wall)

    def generate_hex(self) -> str:
        map_hex: list[str] = []
        for row in self.rows:
            row_str = ''
            for cell in row:
                hex_split = hex(cell.value).split('0x')
                hex_value = hex_split[1]
                row_str += hex_value
            map_hex.append(row_str)
        return '\n'.join(map_hex)

    def generate_output(self) -> None:
        output = ""
        output += self.map_hex + "\n\n"
        output += str(self.entry) + '\n'
        output += str(self.exit)
        with open(self.output_file, 'w') as file:
            file.write(output)

    def erase_map(self) -> None:
        self.rows.clear()
        self.initial_state = ""
        self.map_hex = ""

    def regenerate_map(self) -> None:
        self.erase_map()
        self.generate_map()

    def draw_map(self) -> str:
        map: list[str] = []
        row_str = self.draw_firs_row(self.rows[0])
        map.append(row_str)
        for row in self.rows:
            row_str = ""
            for cell in row:
                coord = (cell.x, cell.y)
                row_str += cell.draw_if(cell.west, '|')
                if coord == self.entry:
                    row_str += self.draw_entry_exit(cell, 'O')
                elif coord == self.exit:
                    row_str += self.draw_entry_exit(cell, 'X')
                else:
                    row_str += cell.draw_if(cell.south, '_')
                if cell.x == self.width - 1:
                    row_str += cell.draw_if(cell.east, '|')
            map.append(row_str)
        return '\n'.join(map)

    def draw_firs_row(self, row: list[conf.Cell]) -> str:
        row_str = " "
        if row[0].y == 0:
            for cell in row:
                if cell.y == 0 and cell.north:
                    row_str += "_ "
        return row_str

    def draw_entry_exit(self, cell: conf.Cell, fill: str) -> str:
        row_str = ""
        start_underline = "\033[4m"
        end_underline = "\033[0m"
        if cell.south:
            row_str += start_underline + fill + end_underline
        else:
            row_str += fill
        return row_str

    # def check_boundaries_sync(self, cell: conf.Cell) -> bool:
    #     up = cell.y - 1
    #     down = cell.y + 1
    #     left = cell.x - 1
    #     right = cell.x + 1
    #     valid = True
    #     if up >= 0:
    #     return valid


def main() -> None:
    print("=== A-Maze-ing ===")
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return
    file = sys.argv[1]
    config = conf.read_config(file)
    print(f"\n--- Reading {file}")
    [print(f"{key}, {value} ({type(value)})") for key, value in config.items()]
    maze = MazeGenerator(config)
    print(f"\n--- Creating maze based on {file} data")
    print("\n- Maze configuration:")
    maze.show_config()

    print("\n- Maze initial map")
    print(maze.initial_state)
    print("\n- Maze normalized map")
    print(maze)

    print("\n------------------------\n")
    print("Map after regen:")
    maze.regenerate_map()
    print("\n- Maze initial map")
    print(maze.initial_state)
    print("\n- Maze normalized map")
    print(maze)
    print()


if __name__ == "__main__":
    main()
