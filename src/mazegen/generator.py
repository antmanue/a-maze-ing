
import src.config as conf
import src.utils as utils
import random as rand
from typing import Generator


class MazeGenerator:
    def __init__(self, config: conf.Config, hex_map: str = "") -> None:
        self.seed: str = config.seed
        rand.seed(self.seed)
        self.width = config.width
        self.height = config.height
        self.entry = config.entry  # Original use
        self.exit = config.exit
        self.output_file = config.output_file
        self.perfect = config.perfect
        self.rows: list[list[utils.Cell]] = []
        self.grid: list[list[int]] = []
        self.initial_state = ""
        self.map_hex: str = hex_map
        self.solution: list[utils.Cell] = []
        self.path: str = ""
        self.paths: list[list[utils.Cell]] = []
        self.current_solution: list[utils.Cell] = []
        self.visited: set[utils.Cell] = set()
        self.all: set[utils.Cell] = set()
        self.logo_42: set[tuple[int, int]] = set()
        self.render_initial_map()
        self.needs_update = True

    def render_initial_map(self) -> None:
        self.seed = conf.Config.generate_seed()
        self.generate_map()
        self.enclose_map()

    def prepare_map_to_visual(self) -> list[list[int, int]]:
        grid: list[list[int]] = []
        for row in self.rows:
            line: list[int] = []
            grid.append(line)
            for cell in row:
                line.append(cell.value)
        return grid

    def prepare_solution_to_visual(self) -> Generator[tuple[int, int],
                                                      None, None]:
        for cell in self.solution:
            yield cell.coord

    def generate_42(self) -> None:
        min_height = 5
        min_width = 7
        four: list[tuple[int, int]] = []
        two: list[tuple[int, int]] = []
        logo: list[tuple[int, int]] = []
        forbiden: list[tuple[int, int]] = []
        if self.width > min_width and self.height > min_height:
            half = int(self.height / 2)
            center_y = half

            half = int(self.width / 2)
            center_x = half

            four = self.generate_4(center_x, center_y)
            two = self.generate_2(center_x, center_y)

            logo.extend(four)
            logo.extend(two)
            forbiden.extend([(center_x + 1, center_y - 1),
                             (center_x, center_y - 1),
                             (center_x + 3, center_y + 1),
                             (center_x + 4, center_y + 1)])
        for x, y in logo:
            self.logo_42.add((x, y))
        self.draw_42(forbiden)

    def draw_42(self, forbidden: list[tuple[int, int]]) -> None:
        min_height = 5
        min_width = 7
        try:
            for x, y in self.logo_42:
                cell = self.get_cell(x, y)
                self.visited.add(cell)
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
            self.all.clear()
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
        rows: list[list[int]] = []
        self.generate_map_from_config(rows)
        self.generate_42()

    def generate_map_from_config(self, values: list[list[int]] = []) -> None:
        for y in range(self.height):
            columns: list[utils.Cell] = []
            self.rows.append(columns)
            columns_int: list[int] = []
            self.grid.append(columns_int)
            for x in range(self.width):
                if self.map_hex:
                    value = values[y][x]    # Cell based on hex_map provided
                else:
                    value = 0   # Create empty cells
                cell = utils.Cell(value, x, y)
                self.all.add(cell)
                columns_int.append(cell.value)
                columns.append(cell)

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
        output += str(self.entry) + '\n'
        output += str(self.exit) + '\n'
        output += self.path
        with open(self.output_file, 'w') as file:
            file.write(output)

    def erase_map(self) -> None:
        self.rows.clear()
        self.map_hex = ""
        self.path = ""

    def clear_solutions(self) -> None:
        self.current_solution.clear()
        self.paths.clear()
        self.solution.clear()
        self.visited.clear()
        self.all.clear()
        logo_42_cells = [self.get_cell(x, y) for x, y in self.logo_42]
        self.visited.union(logo_42_cells)

    def regenerate_map(self) -> None:
        self.clear_solutions()
        self.erase_map()
        self.render_initial_map()

    def get_free_neighbours(self, curr: utils.Cell) -> list[utils.Cell]:
        free: list[utils.Cell] = []
        for direction in range(4):
            neighbour = utils.Neighbour(curr, direction)

            if not self.within_map(neighbour.x, neighbour.y):
                continue
            if self.get_cell(neighbour.x, neighbour.y) in self.visited:
                continue
            free.append(self.rows[neighbour.y][neighbour.x])
        return free

    def within_map(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width:
            return False
        elif y < 0 or y >= self.height:
            return False
        return True

    def draw_walls(self, prev: utils.Cell, curr: utils.Cell) -> None:
        dir = utils.Directions()
        self.validate_walls(prev)
        wall_between = dir.between(prev, curr)
        for wall in range(4):
            if not prev.calculate_bit(wall):
                neigh = utils.Neighbour(prev, wall)
                if self.get_cell(neigh.x, neigh.y) not in self.visited:
                    self.update_wall(prev, wall, 1)
        if curr.calculate_bit(dir.opposite(wall_between)):
            self.update_wall(curr, dir.opposite(wall_between), 0)

    def update_wall(self, cell: utils.Cell, wall: int, value: int) -> None:
        dir = utils.Directions()
        neigh = utils.Neighbour(cell, wall)
        if self.within_map(neigh.x, neigh.y):
            cell.set_bit(wall, value)
            self.enforce_shared_wall(cell, dir.opposite(wall),
                                     self.rows[neigh.y][neigh.x])

    def get_cell(self, x: int, y: int) -> utils.Cell:
        return self.rows[y][x]

    def transform_to_imperfect_maze(self) -> Generator[None, None, None]:
        size = self.height * self.width
        remove_amount = int(size * 0.50)
        for _ in range(remove_amount):
            x = rand.randrange(self.width)
            y = rand.randrange(self.height)
            cell = self.get_cell(x, y)
            direction = rand.randrange(4)
            neigh = utils.Neighbour(cell, direction)
            if cell.coord in self.logo_42 or cell.coord == self.exit:
                continue
            elif neigh.coord in self.logo_42:
                continue
            self.update_wall(self.get_cell(x, y), direction, 0)
            yield

    def look_for_invalid_neighbours(self) -> Generator[None, None, None]:
        for row in self.rows:
            for cell in row:
                if self.invalid_surrounding_neighbours(cell):
                    yield
                    self.correct_neighbours(cell)

    def invalid_surrounding_neighbours(self, cell: utils.Cell) -> bool:
        corners_diff = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        corner_bits = [[1, 2], [2, 3], [0, 1], [0, 3]]
        sides_diff = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        side_bits = [[0, 1, 2], [0, 2, 3], [1, 2, 3], [0, 1, 3]]
        neigh_coords = corners_diff.copy()
        neigh_coords.extend(sides_diff)
        for x, y in neigh_coords:
            if cell.value != 0:
                return False
            if self.within_map(cell.x + x, cell.y + y):
                neigh = self.rows[cell.y + y][cell.x + x]
                if (x, y) in corners_diff:
                    for bit in corner_bits[corners_diff.index((x, y))]:
                        if neigh.calculate_bit(bit):
                            return False
                elif (x, y) in sides_diff:
                    for bit in side_bits[sides_diff.index((x, y))]:
                        if neigh.calculate_bit(bit):
                            return False
            else:
                return False
        return True

    def correct_neighbours(self, cell: utils.Cell) -> bool:
        free = [dir for dir in range(4)]
        while free:
            dir = rand.randint(0, 3)
            neigh = utils.Neighbour(cell, dir)
            if neigh in self.solution:
                free = [dir for dir in range(4) if dir != dir]
                continue
            else:
                self.update_wall(cell, dir, 1)
                return True
        return False

    def a_star(self) -> None:
        entry = self.get_cell(self.entry[0], self.entry[1])
        exit = self.get_cell(self.exit[0], self.exit[1])

        open_list: list[utils.Cell] = [entry]
        closed_list: set[utils.Cell] = set()

        entry.g = 0
        entry.h = abs(entry.x - exit.x) + abs(entry.y - exit.y)
        entry.f = entry.g + entry.h

        while open_list:
            curr = min(open_list, key=lambda cell: cell.f)

            if curr == exit:
                self.solution = []
                while curr is not None:
                    self.solution.append(curr)
                    if not curr.parent:
                        break
                    curr = curr.parent
                self.solution.reverse()
                self.paths.append(self.solution.copy())
                return

            open_list.remove(curr)
            closed_list.add(curr)

            for direction in range(4):
                # Check if path is free
                if curr.calculate_bit(direction):
                    continue

                neigh_coord = utils.Neighbour(curr, direction)
                # Check if neighbour is valid
                if not self.within_map(neigh_coord.x, neigh_coord.y):
                    continue

                neigh = self.get_cell(neigh_coord.x, neigh_coord.y)

                if neigh in closed_list:
                    continue

                attempt_g = curr.g + 1
                if neigh not in open_list:
                    open_list.append(neigh)
                if attempt_g >= neigh.g:
                    continue
                neigh.parent = curr
                neigh.g = attempt_g
                neigh.h = abs(neigh.x - exit.x) + abs(neigh.y - exit.y)
                neigh.f = neigh.g + neigh.h

    def backtracking(self, start: utils.Cell) -> Generator[None, None, None]:
        """
        Add cell to path, draw and sync neighbours,
        remove if leads to dead end and repeat
        """
        stack: list[utils.Cell] = [start]
        dir = utils.Directions()
        self.visited.add(start)
        self.paths.append(stack)
        while stack:
            curr = stack[-1]
            if curr.coord == self.exit:
                self.solution = stack.copy()
                yield
                stack.pop()
                curr = stack[-1]
            free = self.get_free_neighbours(curr)
            if free:
                neigh = rand.choice(free)
                if neigh not in self.visited:
                    stack.append(neigh)
                    self.visited.add(neigh)
                    if neigh.coord == self.exit:
                        wall_neigh_curr = dir.between(neigh, curr)
                        for wall in range(4):
                            if wall == wall_neigh_curr:
                                self.update_wall(neigh, wall, 0)
                            self.update_wall(neigh, wall, 1)
                            yield
                    self.draw_walls(curr, neigh)
                    yield
                free.remove(neigh)
            else:
                stack.pop()
                yield
