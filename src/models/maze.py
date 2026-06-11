from ..io.config import Config
from ..models.cell import Cell
import random as rand


class Maze:
    def __init__(self, config: Config) -> None:
        self.seed: str = config.seed
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.output_file = config.output_file
        self.perfect = config.perfect
        self.rows: list[list[Cell]] = []

    def create_map(self) -> None:
        if not self.seed:
            self.seed = self.generate_seed()
        rand.seed(self.seed)
        self.populate_map()

    def populate_map(self) -> None:
        for y in range(self.height):
            columns: list[Cell] = []
            self.rows.append(columns)
            columns_int: list[int] = []
            for x in range(self.width):
                value = 0
                cell = Cell(value, x, y)
                columns_int.append(cell.value)
                columns.append(cell)

    def within_map(self, coords: tuple[int, int]) -> bool:
        x, y = coords
        if x < 0 or x >= self.width:
            return False
        elif y < 0 or y >= self.height:
            return False
        return True

    def clear_map(self) -> None:
        self.rows.clear()

    def prepare_map_to_visual(self) -> list[list[int]]:
        grid: list[list[int]] = []
        for row in self.rows:
            line: list[int] = []
            grid.append(line)
            for cell in row:
                line.append(cell.value)
        return grid

    def get_cell(self, coords: tuple[int, int]) -> Cell:
        x, y = coords
        return self.rows[y][x]

    def generate_seed(self) -> str:
        seed = ''
        for _ in range(15):
            seed += f'{rand.randrange(16):X}'
        return seed
