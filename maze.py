#!/usr/bin/env python3


import config as conf
import random as rand


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

    def show(self) -> None:
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

    def print_maze(self) -> None:
        for row in self.rows:
            if row[0].y == 0:   # first_row
                print(' ', end='')
                for cell in row:
                    if cell.y == 0 and cell.north:
                        print('_ ', end='')
                print()
            for cell in row:
                cell.print_if(cell.west, '|')
                cell.print_if(cell.south, '_')
                if cell.x == self.width - 1:
                    cell.print_if(cell.east, '|')
                    print()

def main() -> None:
    config = conf.read_config("config.txt")
    maze = MazeGenerator(config)
    maze.show()
    print()

    rows: list[list[conf.Cell]] = []
    for y in range(maze.height):
        columns: list[conf.Cell]= []
        for x in range(maze.width):
            west = 3
            south = 2
            east = 1
            north = 0
            value = rand.randint(0, 15)
            cell = conf.Cell(value, x, y)
            # print(f"value: {cell.value} - ", end='')
            # cell.get_bits()
            if y == 0:
                cell.set_bit(north, 1)
            if y == maze.height - 1:
                cell.set_bit(south, 1)
            if x == 0:
                cell.set_bit(west, 1)
            if x == maze.width - 1:
                cell.set_bit(east, 1)
            # print(f"        value: {cell.value} - ", end='')
            # cell.get_bits()
            # print()
            # columns.append(cell)
            columns.append(cell)
            print(hex(cell.value).split('0x')[1].upper(), end='')
        print()
        # rows.append(columns)
        maze.rows.append(columns)
    # maze.rows[0][0].get_bits()
    maze.print_maze()



if __name__ == "__main__":
    main()
