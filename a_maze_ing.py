#!/usr/bin/env python3


import config as conf
import utils
import random as rand
import sys
from mazegen.display import MazeDisplay


class MazeGenerator:
    def __init__(self, config: conf.Config) -> None:
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.output_file = config.output_file
        self.perfect = config.perfect
        self.rows: list[list[utils.Cell]] = []
        self.initial_state = ""
        self.map_hex = ""
        self.generate_map()

    def __str__(self) -> str:
        return '\n'.join([self.map_hex, self.draw_map()])

    def generate_map(self) -> None:
        for y in range(self.height):
            columns: list[utils.Cell] = []
            self.rows.append(columns)
            for x in range(self.width):
                value = rand.randint(0, 15)
                cell = utils.Cell(value, x, y)
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

    def generate_borders(self, cell: utils.Cell) -> None:
        dir = utils.Directions()
        if cell.y == 0:
            cell.set_bit(dir.north, 1)
        if cell.y == self.height - 1:
            cell.set_bit(dir.south, 1)
        if cell.x == 0:
            cell.set_bit(dir.west, 1)
        if cell.x == self.width - 1:
            cell.set_bit(dir.east, 1)

    def validate_walls(self, cell: utils.Cell) -> None:
        dir = utils.Directions()
        up = cell.y - 1
        left = cell.x - 1
        if up >= 0:
            upper_cell = self.rows[up][cell.x]
            self.enforce_shared_wall(upper_cell,
                                     dir.north, cell)
        if left >= 0:
            left_cell = self.rows[cell.y][left]
            self.enforce_shared_wall(left_cell,
                                     dir.west, cell)

    def enforce_shared_wall(self, neighbour: utils.Cell, wall: int,
                            cell: utils.Cell) -> None:
        dir = utils.Directions()
        neighbour_wall = neighbour.calculate_bit(dir.opposite(wall))
        cell_wall = cell.calculate_bit(wall)
        if neighbour_wall != cell_wall:
            cell.set_bit(wall, neighbour_wall)

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
        dir = utils.Directions()
        row_str = self.draw_firs_row()
        map.append(row_str)
        for row in self.rows:
            row_str = ""
            for cell in row:
                coord = (cell.x, cell.y)
                row_str += cell.draw_if(dir.west)
                if coord == self.entry:
                    row_str += cell.draw_if(dir.south, 'O')
                elif coord == self.exit:
                    row_str += cell.draw_if(dir.south, 'X')
                else:
                    row_str += cell.draw_if(dir.south)
                if cell.x == self.width - 1:
                    row_str += cell.draw_if(dir.east)
            map.append(row_str)
        return '\n'.join(map)

    def draw_firs_row(self) -> str:
        row_str = " "
        first_row = self.rows[0]
        for cell in first_row:
            if cell.north:
                row_str += "_ "
        return row_str

    def check_all_boundaries(self) -> bool:
        for row in self.rows:
            for cell in row:
                if not self.is_boundaries_synced(cell):
                    return False
        return True

    def is_boundaries_synced(self, cell: utils.Cell) -> bool:
        dir = utils.Directions()
        up = cell.y - 1
        down = cell.y + 1
        left = cell.x - 1
        right = cell.x + 1
        if up >= 0:
            neighbour_cell = self.rows[up][cell.x]
            if not self.is_wall_synced(neighbour_cell, dir.north, cell):
                return False
        if left >= 0:
            neighbour_cell = self.rows[cell.y][left]
            if not self.is_wall_synced(neighbour_cell, dir.west, cell):
                return False
        if right <= self.width - 1:
            neighbour_cell = self.rows[cell.y][right]
            if not self.is_wall_synced(neighbour_cell, dir.east, cell):
                return False
        if down <= self.height - 1:
            neighbour_cell = self.rows[down][cell.x]
            if not self.is_wall_synced(neighbour_cell, dir.south, cell):
                return False
        return True

    def is_wall_synced(self, neighbour: utils.Cell, wall: int,
                       cell: utils.Cell) -> bool:
        dir = utils.Directions()
        neighbour_wall = neighbour.calculate_bit(dir.opposite(wall))
        cell_wall = cell.calculate_bit(wall)
        if neighbour_wall != cell_wall:
            return False
        return True


def main() -> None:
    print("=== A-Maze-ing ===")
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return
    file = sys.argv[1]
    config = conf.Config(file)
    try:
        config.parse_config(config.content)
    except conf.ConfigError as err:
        print(err)
        return
    print(f"\n--- Reading {file}")
    config.print()
    maze = MazeGenerator(config)
    print(f"\n--- Creating maze based on {file} data")

    print("- Maze initial map")
    print(maze.initial_state)
    print("\n- Maze normalized map")
    print(maze)

    # print("\n------------------------\n")
    # test_map_regen(maze)

    # print("\n------------------------\n")
    # test_all_walls_synced(maze)
    grid: list[list[int]] = []
    for row in maze.rows:
        line: list[int] = []
        grid.append(line)
        for cell in row:
            line.append(cell.value)

    display = MazeDisplay(grid)
    display.render_terminal()
    display.run()


def test_map_regen(maze: MazeGenerator) -> None:
    print("Map after regen:")
    maze.regenerate_map()
    print("\n- Maze initial map")
    print(maze.initial_state)
    print("\n- Maze normalized map")
    print(maze)
    print()


def test_all_walls_synced(maze: MazeGenerator) -> None:
    print("Is all boundaries of all cells in sync? "
          f"{maze.check_all_boundaries()}")
    print("\nModify a cell to break wall sync")
    x, y = input("Modify cell in coordinates (x, y): ").split(' ')
    wall, value = input("Choose a wall and new value: ").split(' ')
    maze.rows[int(y)][int(x)].set_bit(int(wall), int(value))
    print(maze)
    print("Is all boundaries of all cells in sync? "
          f"{maze.check_all_boundaries()}")


if __name__ == "__main__":
    main()
