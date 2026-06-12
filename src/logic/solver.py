from ..models import Maze
from ..models import Cell
from enum import IntEnum


class Solver:
    """Handles maze solving computations using search algorithms."""
    def __init__(self, maze: Maze):
        """Initializes the maze solver with a target maze layout."""
        self.maze = maze

    def use_algorithm(self, algorithm: int) -> list[Cell]:
        """Executes a maze-solving pipeline using specified algorithm."""
        try:
            if algorithm == Algorithms.A_STAR:
                name = "A*"
                return self.a_star()
            else:
                raise SolverError("No solution found with "
                                  f"'{name}' algorithm.")
        except SolverError as err:
            print(f"SolverError found: {err}")
        return []

    def a_star(self) -> list[Cell]:
        """Finds optimal paths from entry to exit using A* search."""
        entry = self.maze.get_cell(self.maze.entry)
        exit = self.maze.get_cell(self.maze.exit)

        open_list: list[Cell] = [entry]
        closed_list: set[Cell] = set()

        entry.g = 0
        entry.h = abs(entry.x - exit.x) + abs(entry.y - exit.y)
        entry.f = entry.g + entry.h

        while open_list:
            curr = min(open_list, key=lambda cell: cell.f)

            if curr == exit:
                solution: list[Cell] = []
                while curr is not None:
                    solution.append(curr)
                    if not curr.parent:
                        break
                    curr = curr.parent
                solution.reverse()
                return solution.copy()

            open_list.remove(curr)
            closed_list.add(curr)

            for direction in range(4):
                if curr.calculate_bit(direction):
                    continue

                neigh_coord = curr.get_neighbour_coords(direction)
                if not self.maze.within_map(neigh_coord):
                    continue

                neigh = self.maze.get_cell(neigh_coord)

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
        return []


class Algorithms(IntEnum):
    """Enumeration of supported maze solving algorithms."""
    A_STAR = 0


class SolverError(Exception):
    """Custom exception thrown for layout solving errors."""
    def __init__(self, message: str = "Unknown Solver error"):
        """Initializes the solver exception with an error message."""
        self.message = message
        super().__init__(self.message)
