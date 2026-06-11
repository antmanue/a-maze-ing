from ..io import Config, MazeExporter
from ..models import Maze, Cell, Directions
from .solver import Solver
import random as rand
from typing import Generator


class MazeGenerator:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.maze = Maze(self.config)
        self.visited: set[Cell] = set()
        self.all: set[Cell] = set()
        self.initial_state = ""
        self.map_hex: str = ""
        self.solution: list[Cell] = []
        self.path: str = ""
        self.paths: list[list[Cell]] = []
        self.needs_update = True
        self.generate_map()
        self.generate_logo()

    def generate_map(self):
        self.maze.create_map()
        self.generate_42()
        self.enclose_map()

    def enclose_map(self) -> None:
        for row in self.maze.rows:
            for cell in row:
                self.generate_borders(cell)

    def generate_borders(self, cell: Cell) -> None:
        if cell.y == 0:
            cell.set_bit(Directions.NORTH, 1)
        if cell.y == self.maze.height - 1:
            cell.set_bit(Directions.SOUTH, 1)
        if cell.x == 0:
            cell.set_bit(Directions.WEST, 1)
        if cell.x == self.maze.width - 1:
            cell.set_bit(Directions.EAST, 1)

    def generate_logo(self) -> None:
        for coord in self.maze.logo_42:
            cell = self.maze.get_cell(coord)
            self.visited.add(cell)
            for direction in range(4):
                self.update_wall(cell, direction, 1)

    def solve_with(self, algorithm: int) -> None:
        solver = Solver(self.maze)
        solution = solver.use_algorithm(algorithm)
        self.solution = solution

    def generate_solution(self) -> Generator[tuple[int, int],
                                             None, None]:
        for cell in self.solution:
            yield cell.coord

    def validate_walls(self, cell: Cell) -> None:
        upper_neigh = cell.get_neighbour_coords(Directions.NORTH)
        left_neigh = cell.get_neighbour_coords(Directions.WEST)
        lower_neigh = cell.get_neighbour_coords(Directions.SOUTH)
        right_neigh = cell.get_neighbour_coords(Directions.EAST)
        x, y = 0, 1
        if upper_neigh[y] >= 0:
            upper_cell = self.maze.get_cell(upper_neigh)
            self.enforce_shared_wall(upper_cell,
                                     Directions.NORTH, cell)
        if left_neigh[x] >= 0:
            left_cell = self.maze.get_cell(left_neigh)
            self.enforce_shared_wall(left_cell,
                                     Directions.WEST, cell)
        if lower_neigh[y] <= self.maze.height - 1:
            lower_cell = self.maze.get_cell(lower_neigh)
            self.enforce_shared_wall(lower_cell,
                                     Directions.SOUTH, cell)
        if right_neigh[x] <= self.maze.width - 1:
            right_cell = self.maze.get_cell(right_neigh)
            self.enforce_shared_wall(right_cell,
                                     Directions.EAST, cell)

    def enforce_shared_wall(self, reference: Cell, wall: int,
                            target: Cell) -> None:
        neighbour_wall = reference.calculate_bit(Directions.opposite(wall))
        cell_wall = target.calculate_bit(wall)
        if neighbour_wall != cell_wall:
            target.set_bit(wall, neighbour_wall)

    def export_generated_data(self):
        exporter = MazeExporter(self.config.output_file,
                                self.maze, self.solution)
        exporter.generate_output()

    def erase_map(self) -> None:
        self.maze.clear_map()
        self.map_hex = ""
        self.path = ""

    def clear_solutions(self) -> None:
        self.paths.clear()
        self.solution.clear()
        self.visited.clear()
        self.all.clear()
        logo_42_cells = [self.maze.get_cell(cell)
                         for cell in self.maze.logo_42]
        self.visited.union(logo_42_cells)

    def regenerate_map(self) -> None:
        self.clear_solutions()
        self.erase_map()
        self.maze = Maze(self.config)
        self.generate_map()
        self.generate_logo()

    def get_free_neighbours(self, curr: Cell) -> list[Cell]:
        free: list[Cell] = []
        for direction in range(4):
            neighbour = curr.get_neighbour_coords(direction)

            if not self.maze.within_map(neighbour):
                continue
            if self.maze.get_cell(neighbour) in self.visited:
                continue
            free.append(self.maze.get_cell(neighbour))
        return free

    def draw_walls(self, prev: Cell, curr: Cell) -> None:
        self.validate_walls(prev)
        wall_between = Directions.between(prev, curr)
        for wall in range(4):
            if not prev.calculate_bit(wall):
                neigh = prev.get_neighbour_coords(wall)
                if self.maze.get_cell(neigh) not in self.visited:
                    self.update_wall(prev, wall, 1)
        if curr.calculate_bit(Directions.opposite(wall_between)):
            self.update_wall(curr, Directions.opposite(wall_between), 0)

    def update_wall(self, cell: Cell, wall: int, value: int) -> None:
        neigh = cell.get_neighbour_coords(wall)
        if self.maze.within_map(neigh):
            cell.set_bit(wall, value)
            self.enforce_shared_wall(cell, Directions.opposite(wall),
                                     self.maze.get_cell(neigh))

    def transform_to_imperfect_maze(self) -> Generator[None, None, None]:
        maze = self.maze
        size = maze.height * maze.width
        remove_amount = int(size * 0.50)
        for _ in range(remove_amount):
            coord = (rand.randrange(maze.width), rand.randrange(maze.height))
            cell = self.maze.get_cell(coord)
            direction = rand.randrange(4)
            neigh = cell.get_neighbour_coords(direction)
            if cell.coord in maze.logo_42 or cell.coord == maze.exit:
                continue
            elif neigh in maze.logo_42:
                continue
            self.update_wall(self.maze.get_cell(coord), direction, 0)
            yield

    def look_for_invalid_neighbours(self) -> Generator[None, None, None]:
        for row in self.maze.rows:
            for cell in row:
                if self.invalid_surrounding_neighbours(cell):
                    yield
                    self.correct_neighbours(cell)

    def invalid_surrounding_neighbours(self, cell: Cell) -> bool:
        corners_diff = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        corner_bits = [[1, 2], [2, 3], [0, 1], [0, 3]]
        sides_diff = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        side_bits = [[0, 1, 2], [0, 2, 3], [1, 2, 3], [0, 1, 3]]
        neigh_coords = corners_diff.copy()
        neigh_coords.extend(sides_diff)
        for x, y in neigh_coords:
            if cell.value != 0:
                return False
            coord = (cell.x + x, cell.y + y)
            if self.maze.within_map(coord):
                neigh = self.maze.get_cell(coord)
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

    def correct_neighbours(self, cell: Cell) -> bool:
        free = [dir for dir in range(4)]
        while free:
            dir = rand.randint(0, 3)
            neigh = cell.get_neighbour_coords(dir)
            if neigh in self.solution:
                free = [dir for dir in range(4) if dir != dir]
                continue
            else:
                self.update_wall(cell, dir, 1)
                return True
        return False

    def backtracking(self, start: Cell) -> Generator[None, None, None]:
        """
        Add cell to path, draw and sync neighbours,
        remove if leads to dead end and repeat
        """
        stack: list[Cell] = [start]
        self.visited.add(start)
        self.paths.append(stack)
        while stack:
            curr = stack[-1]
            if curr.coord == self.maze.exit:
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
                    if neigh.coord == self.maze.exit:
                        wall_neigh_curr = Directions.between(neigh, curr)
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

    def generate_42(self) -> None:
        min_height = 5
        min_width = 7
        four: list[tuple[int, int]] = []
        two: list[tuple[int, int]] = []
        logo: list[tuple[int, int]] = []
        forbiden: list[tuple[int, int]] = []
        if self.maze.width > min_width and self.maze.height > min_height:
            half = int(self.maze.height / 2)
            center_y = half

            half = int(self.maze.width / 2)
            center_x = half

            four = self.generate_4(center_x, center_y)
            two = self.generate_2(center_x, center_y)

            logo.extend(four)
            logo.extend(two)
            forbiden.extend([(center_x + 1, center_y - 1),
                             (center_x, center_y - 1),
                             (center_x + 3, center_y + 1),
                             (center_x + 4, center_y + 1)])
        if self.maze.validate_42(forbiden):
            for coord in logo:
                self.logo_42.add(coord)

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
