#!/usr/bin/env python3


import config as conf
import utils
import random as rand
import sys
from mazegen.display import MazeDisplay


class MazeGenerator:
    def __init__(self, config: conf.Config, hex_map: str = "") -> None:
        self.width = config.width
        self.height = config.height
        # self.entry = config.entry # Original use
        # self.exit = config.exit
        self.entry = self.generate_random_entry_exit()  # Test random entries
        self.exit = self.generate_random_entry_exit()
        # self.entry = (2, 1)  # Fixed entry/exit
        # self.exit = (1, 1)
        self.output_file = config.output_file
        self.perfect = config.perfect
        self.rows: list[list[utils.Cell]] = []
        self.initial_state = ""
        self.map_hex = hex_map
        self.solution: list[utils.Cell] = []
        self.path = ""
        self.paths: list[list[utils.Cell]] = []
        self.current_solution: list[utils.Cell] = []
        self.visited: list[utils.Cell] = []
        # self.iters = 0
        self.logo_42: list[tuple[int, int]] = []
        self.setup()

    def __str__(self) -> str:
        return '\n'.join([self.map_hex, self.path, self.draw_map()])

    def setup(self) -> None:
        # self.generate_random_entry_exit()   # Testing purposes only
        self.generate_map()
        self.initial_state += self.generate_hex() + '\n'
        self.initial_state += self.draw_map()
        self.enclose_map()
        self.find_path()
        self.connect_paths()
        self.map_hex = self.generate_hex()
        self.generate_path()
        self.generate_output()

    def generate_random_entry_exit(self) -> tuple[int, int]:
        res = (rand.randrange(0, self.width),
               rand.randrange(0, self.height))
        return res

    def generate_42(self) -> None:
        min_height = 5
        min_width = 7
        four: list[tuple[int, int]] = []
        two: list[tuple[int, int]] = []
        logo: list[tuple[int, int]] = []
        forbiden: list[tuple[int, int]] = []
        if self.width > min_width and self.height > min_height:
            half = int(self.height / 2)
            if self.height % 2 == 0:
                center_y = half - 1
            else:
                center_y = half + 1

            half = int(self.width / 2)
            if self.width % 2 == 0:
                center_x = half - 1
            else:
                center_x = half + 1

            four = self.generate_4(center_x, center_y)
            two = self.generate_2(center_x, center_y)

            logo.extend(four)
            logo.extend(two)
            forbiden.extend([(center_x + 1, center_y - 1), (center_x + 3, center_y + 1)])
        for x, y in logo:
            self.logo_42.append((x, y))
            print(f"({y}, {x}), ", end='')
        print()
        self.draw_42(forbiden)

    def draw_42(self, forbidden: list[tuple[int, int]]) -> None:
        min_height = 5
        min_width = 7
        try:
            for x, y in self.logo_42:
                cell = self.get_cell(x, y)
                self.visited.append(cell)
                if self.exit in (forbidden):
                    raise conf.ConfigError("'EXIT' position will lead "
                                           "to isolated cells")
                elif self.exit in self.logo_42 or self.entry in self.logo_42:
                    raise conf.ConfigError("'ENTRY'/'EXIT' will overwrite "
                                           "42 pattern")
                elif self.height <= min_height + 1:
                    raise conf.ConfigError("Labirinth size is too small")
                elif self.width <= min_width + 1:
                    raise conf.ConfigError("Labirinth size is too small")
                for direction in range(4):
                    self.update_wall(cell, direction, 1)
        except conf.ConfigError as err:
            self.visited.clear()
            print(f"[Warning] 42 pattern ommited due to forbidden "
                  f"placement: {err}.")

    def generate_4(self, center_x: int,
                   center_y: int) -> list[tuple[int, int]]:
        return [(center_x - 3, center_y - 2), (center_x - 3, center_y - 1),
                (center_x - 3, center_y), (center_x - 2, center_y),
                (center_x - 1, center_y), (center_x - 1, center_y + 1),
                (center_x - 1, center_y + 2)]

    def generate_2(self, center_x: int,
                   center_y: int) -> list[tuple[int, int]]:
        return [(center_x + 1, center_y - 2), (center_x + 2, center_y - 2),
                (center_x + 3, center_y - 2), (center_x + 3, center_y - 1),
                (center_x + 3, center_y), (center_x + 2, center_y),
                (center_x + 1, center_y), (center_x + 1, center_y + 1),
                (center_x + 1, center_y + 2), (center_x + 2, center_y + 2),
                (center_x + 3, center_y + 2)]

    def generate_map(self) -> None:
        hex_str = self.map_hex
        rows: list[list[int]] = []
        if hex_str:
            rows = self.hex_str_to_value_list(hex_str)
            self.height = len(rows)
            self.width = len(rows[0])
        self.generate_map_from_config(rows)
        self.generate_42()

    def generate_map_from_config(self, values: list[list[int]] = []) -> None:
        for y in range(self.height):
            columns: list[utils.Cell] = []
            self.rows.append(columns)
            for x in range(self.width):
                if self.map_hex:
                    value = values[y][x]    # Cell based on hex_map provided
                else:
                    value = 0   # Create empty cells
                cell = utils.Cell(value, x, y)
                columns.append(cell)

    def hex_str_to_value_list(self, hex_str: str) -> list[list[int]]:
        hex_rows: list[list[int]] = []
        for row in hex_str.split('\n'):
            hex_row: list[int] = []
            hex_rows.append(hex_row)
            for char in row:
                hex_row.append(int(char, 16))
        return hex_rows

    def enclose_map(self) -> None:
        for row in self.rows:
            for cell in row:
                self.generate_borders(cell)

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
        upper_neigh = utils.Neighbour(cell, dir.north)
        left_neigh = utils.Neighbour(cell, dir.west)
        lower_neigh = utils.Neighbour(cell, dir.south)
        right_neigh = utils.Neighbour(cell, dir.east)
        if upper_neigh.y >= 0:
            upper_cell = self.get_cell(upper_neigh.x, upper_neigh.y)
            self.enforce_shared_wall(upper_cell,
                                     dir.north, cell)
        if left_neigh.x >= 0:
            left_cell = self.get_cell(left_neigh.x, left_neigh.y)
            self.enforce_shared_wall(left_cell,
                                     dir.west, cell)
        if lower_neigh.y <= self.height - 1:
            lower_cell = self.get_cell(lower_neigh.x, lower_neigh.y)
            self.enforce_shared_wall(lower_cell,
                                     dir.south, cell)
        if right_neigh.x <= self.width - 1:
            right_cell = self.get_cell(right_neigh.x, right_neigh.y)
            self.enforce_shared_wall(right_cell,
                                     dir.east, cell)

    def enforce_shared_wall(self, reference: utils.Cell, wall: int,
                            target: utils.Cell) -> None:
        dir = utils.Directions()
        neighbour_wall = reference.calculate_bit(dir.opposite(wall))
        cell_wall = target.calculate_bit(wall)
        if neighbour_wall != cell_wall:
            target.set_bit(wall, neighbour_wall)

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

    def generate_path(self) -> None:
        dir = utils.Directions()
        solution = self.solution.copy()
        while len(solution) >= 2:
            direction = dir.between(solution[0], solution[1])
            self.path += dir.get_orientation(direction)
            solution.pop(0)

    def generate_output(self) -> None:
        output = ""
        output += self.map_hex + "\n\n"
        output += self.path + '\n'
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
        self.setup()

    def draw_map(self) -> str:
        """
        Generates a clean ASCII visual grid representation of the maze,
        accounting for shared walls, entry (O), and exit (X).
        """
        if not self.rows:
            return ""

        dir = utils.Directions()
        map_lines = []

        # 1. Build the top boundary line of the entire maze
        top_line = "+"
        for cell in self.rows[0]:
            top_line += "---+" if cell.calculate_bit(dir.north) else "   +"
        map_lines.append(top_line)

        # 2. Build the body row-by-row
        for y, row in enumerate(self.rows):
            mid_line = ""  # Represents the cell centers and West/East walls
            bot_line = "+"  # Represents the South walls and corners

            for x, cell in enumerate(row):
                coord = (cell.x, cell.y)
                # --- Determine the West (left) Wall ---
                if x == 0:
                    mid_line += "|" if cell.calculate_bit(dir.west) else " "
                # --- Determine Center Content (Path, Entry, or Exit) ---
                if coord == self.entry:
                    center = " O "
                elif coord == self.exit:
                    center = " X "
                else:
                    center = "   "
                mid_line += center

                # --- Determine the East (right) Wall ---
                mid_line += "|" if cell.calculate_bit(dir.east) else " "

                # --- Determine the South (bottom) Wall & Corner ---
                bot_line += "---" if cell.calculate_bit(dir.south) else "   "
                bot_line += "+"

            map_lines.append(mid_line)
            map_lines.append(bot_line)

        return "\n".join(map_lines)

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

    def get_free_neighbours(self, curr: utils.Cell,
                            prev: utils.Cell) -> list[utils.Cell]:
        free: list[utils.Cell] = []
        for direction in range(4):
            neighbour = utils.Neighbour(curr, direction)
            if neighbour.x < 0 or neighbour.x >= self.width:
                continue
            elif neighbour.y < 0 or neighbour.y >= self.height:
                continue
            last_visiteds = reversed(self.visited)
            is_free = True
            for coord in ((cell.x, cell.y) for cell in last_visiteds):
                if (neighbour.x, neighbour.y) == coord:
                    is_free = False
                    break
            if is_free:
                free.append(self.rows[neighbour.y][neighbour.x])
        return free

    def within_map(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width:
            return False
        elif y < 0 or y >= self.height:
            return False
        return True

    def draw_walls(self, prev: utils.Cell, curr: utils.Cell,
                   next: utils.Cell) -> None:
        dir = utils.Directions()
        # print(f"Cell: {curr.get_bits()}")
        self.validate_walls(curr)   # Sync with existing walls
        # print(f"Validated: {curr.get_bits()}")
        # bit = curr.calculate_bit
        for direction in range(dir.west + 1):  # Clear between prev curr next
            # print(f"dir: {direction}")
            wall_curr_next = dir.between(curr, next)
            if (next.x, next.y) == self.exit:   # Isolate path to exit
                # print(f"        Updating next: {next.get_bits()}")
                if direction != dir.opposite(wall_curr_next):
                    # print(f"        Raising wall {direction}")
                    self.update_wall(next, direction, 1)
                # print(f"        Updating next: {next.get_bits()}")
            if not curr.calculate_bit(direction):
                # print(f"dir: {direction} (bit: "
                #       f"{curr.calculate_bit(direction)}) | wall_curr_next: "
                #       f"{wall_curr_next} (bit: "
                #       f"{curr.calculate_bit(wall_curr_next)})")
                if curr == prev:
                    if direction != wall_curr_next:
                        self.update_wall(curr, direction, 1)
                else:
                    wall_curr_prev = dir.between(curr, prev)
                    # print(f"curr_prev: {wall_curr_prev} - "
                    #       f"{curr.calculate_bit(wall_curr_prev)}")
                    if direction not in [wall_curr_prev, wall_curr_next]:
                        # neigh = utils.Neighbour(curr.x, curr.y, direction)
                        neigh = utils.Neighbour(curr, direction)
                        print(f"Updating cell {curr.coord} for direction "
                              f"{direction}")
                        visited = not all(node.coord != neigh.coord
                                          for node in self.visited)
                        if visited:
                            continue
                        self.update_wall(curr, direction, 1)
                # print(f"dir: {direction} "
                #       f"(bit: {curr.calculate_bit(direction)}) | "
                #       f"wall_curr_next: {wall_curr_next} (bit: "
                #       f"{curr.calculate_bit(wall_curr_next)})")
            else:
                if direction == wall_curr_next:
                    self.update_wall(curr, direction, 0)
            # print(f"Updating: {curr.get_bits()}")
        # print(f"Updated: {curr.get_bits()}")
        print()
        print(self.draw_map())

    def update_wall(self, cell: utils.Cell, wall: int, value: int) -> None:
        dir = utils.Directions()
        neigh = utils.Neighbour(cell, wall)
        if self.within_map(neigh.x, neigh.y):
            print(f"Removing wall {wall} from {(cell.y, cell.x)}")
            # print(f"Neighbour: ({neigh.y}, {neigh.x})")
            # print(f"Visited - {len(self.visited)}:")
            # for node in self.visited:
            #     print(f"{(node.y, node.x)} -> ", end='')
            #     if node.coord == neigh.coord:
            #         print(f"\nCoords ({node.y}, {node.x}) are equal\n")
            # print()
            cell.set_bit(wall, value)
            self.enforce_shared_wall(cell, dir.opposite(wall),
                                     self.rows[neigh.y][neigh.x])

    def connect_cell(self, cell: utils.Cell, solution: bool = False) -> bool:
        dir = utils.Directions()
        walls: list[int] = []
        # checked: list[int] = []
        for direction in range(dir.west + 1):
            if cell.calculate_bit(direction):
                walls.append(direction)
        rand.shuffle(walls)
        for wall in walls:
            neigh = utils.Neighbour(cell, wall)
            # print(f"Trying to remove wall {wall} from {(cell.y, cell.x)} | "
            #       f"({neigh.y}, {neigh.x})")
            # if wall in checked:
            if self.within_map(neigh.x, neigh.y):
                if solution:
                    solutions = self.paths
                    if self.get_cell(neigh.x, neigh.y) not in solutions[0]:
                        continue
                if (neigh.x, neigh.y) != self.exit:
                    if (neigh.x, neigh.y) not in self.logo_42:
                        self.update_wall(cell, wall, 0)
                        return True
            # checked.append(wall)
        return False

    def connect_to_path(self, path: list[utils.Cell],
                        solut_path: bool = False) -> None:
        while path:
            # print(f"    Path cells: {len(path)}")
            cell = rand.choice(path)
            removed = self.connect_cell(cell, solut_path)
            for i, solution in enumerate(self.paths):
                print(f"Solution [{i}]/[{len(self.paths)}] - "
                      f"{len(solution)}: ")
                #   f"{[(cell.y, cell.x) for cell in solution]}")
            if removed:
                if solut_path:
                    path = self.paths[0]
                path_to_merge = -1
                for solution in self.paths:
                    if cell in solution:
                        path_to_merge = self.paths.index(solution)
                path.extend(self.paths[path_to_merge])
                self.paths.pop(path_to_merge)
                print(f"NEW_Solution: {[(cell.y, cell.x) for cell in path]}")
                print(f"{len(self.paths[0])}/{len(self.visited)}: "
                      f"{[(cell.y, cell.x) for cell in self.visited if cell not in self.paths[0]]}")
                break
            path.remove(cell)

    def connect_paths(self) -> None:
        print(f"{len(self.visited)} cells visited out of "
              f"{len(self.rows) * len(self.rows[0])}")
        for i, path in enumerate(self.paths[1:]):
            print()
            print(f"Solution [{i + 1}] - {len(path)}:")
            [print(f"{(cell.y, cell.x)} -> ", end='') for cell in path]
            print()
            connectable_cells: list[utils.Cell] = []
            for cell in path:
                for direction in range(4):
                    neigh = utils.Neighbour(cell, direction)
                    if self.within_map(neigh.x, neigh.y):
                        if self.get_cell(neigh.x, neigh.y).coord != self.exit:
                            if self.rows[neigh.y][neigh.x] in self.paths[0]:
                                connectable_cells.append(cell)
                                break
            # print(f"Connectable cells: {len(connectable_cells)}")
            if not connectable_cells:
                self.connect_to_path(path)
            else:
                self.connect_to_path(connectable_cells, True)

    def find_path(self) -> None:
        x, y = self.entry
        self.backtracking(self.rows[y][x], self.rows[y][x])
        for row in self.rows:
            for cell in row:
                if cell not in self.visited:
                    self.backtracking(cell, cell)

    def get_cell(self, x: int, y: int) -> utils.Cell:
        return self.rows[y][x]

    def backtracking(self, curr: utils.Cell,
                     prev: utils.Cell):
        """
        Add cell to path, draw and sync neighbours,
        remove if leads to dead end and repeat
        """
        # self.iters += 1     # [Testing Only] Avoid infinite loop if
        # if self.iters > 20: # something goes wrong
        #     return
        if len(self.current_solution) > 0:
            prev = self.current_solution[-1]
        self.visited.append(curr)
        self.current_solution.append(curr)
        if (curr.x, curr.y) == self.exit and len(self.paths) == 0:
            self.paths.append(self.current_solution.copy())
            self.solution = self.current_solution.copy()
            print("Solution found")
            self.current_solution.clear()
            return
        # print("visited: "
        #       f"{[(cell.y, cell.x) for cell in self.current_solution]}")
        print("solution: "
              f"{[(cell.y, cell.x) for cell in self.current_solution]}")
        free = self.get_free_neighbours(curr, prev)
        if free:
            back = self.backtracking    # Alias to shorten function call
            while free:
                choice = rand.choice(free)  # Select random next cell
                print("    free: ", end='')
                [print(f"{(neighbour.y, neighbour.x)}",
                       end=', ') for neighbour in free]
                print()
                print(f"            choice: {(choice.y, choice.x)}")
                self.draw_walls(prev, curr, choice)
                back(self.rows[choice.y][choice.x], curr)
                if len(self.paths) > 0:
                    if len(self.current_solution) > 0:
                        print("Another solution found")
                        self.paths.append(self.current_solution.copy())
                        self.current_solution.clear()
                    return
                # print("Free: "
                #       f"{[(cell.y, cell.x) for cell in free]}")
                # print("visited: "
                #       f"{[(cell.y, cell.x) for
                #           cell in self.current_solution]}")
                free = [cell for cell in free if cell not in self.visited]
                print()
                print(f"         Removing {(choice.y, choice.x)}")
                self.current_solution.remove(choice)
        else:
            print(f"        Part of dead-end ({curr.y}, {curr.x})")
            if len(self.paths) > 0:
                if len(self.current_solution) > 0:
                    print("Another solution found")
                    self.paths.append(self.current_solution.copy())
                    self.current_solution.clear()
            print("             ----------")


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
    # hex_map = "b93d3\nc2c3a\n9696a\nabed2\nc4556"  # NENWNWSSWSSEN
    # maze = MazeGenerator(config, hex_map)
    maze = MazeGenerator(config)
    print(f"\n--- Creating maze based on {file} data")

    print("- Maze initial map")
    print(maze.initial_state)
    print("\n- Maze normalized map")
    print(maze)

    if len(maze.paths) > 0:
        for solution in maze.paths:
            print(f"Solution - {len(solution)}:")
            [print(f"{(cell.y, cell.x)} -> ", end='') for cell in solution]
            print()
    else:
        print("None")

    print()
    print(maze)
    # print(f"Entry: {maze.entry}")
    # print(f"Exit: {maze.exit}")

    # print("\n------------------------\n")
    # test_map_regen(maze)

    # print("\n------------------------\n")
    # test_all_walls_synced(maze)
    # grid: list[list[int]] = []
    # for row in maze.rows:
    #     line: list[int] = []
    #     grid.append(line)
    #     for cell in row:
    #         line.append(cell.value)
    # path: list[tuple[int, int]] = []
    # for cell in maze.solution:
    #     path.append(cell.coord)
    # print(f"Entry: {maze.entry} | Exit {maze.exit}")

    # display = MazeDisplay(grid, maze.entry, maze.exit, path)
    # display.render_terminal()
    # display.run()


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
