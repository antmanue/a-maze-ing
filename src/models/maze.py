from ..io.config import Config, ConfigError
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
        self.logo_42: set[tuple[int, int]] = set()

    # render_initial_map
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

    def validate_42(self, forbidden: list[tuple[int, int]]) -> bool:
        valid = False
        min_height = 5
        min_width = 7
        maze = self
        try:
            for coord in maze.logo_42:
                if maze.exit in (forbidden):
                    raise ConfigError("'EXIT' position will lead "
                                      "to isolated cells")
                elif maze.exit in maze.logo_42 or maze.entry in maze.logo_42:
                    raise ConfigError("'ENTRY'/'EXIT' will overwrite "
                                      "42 pattern")
                elif maze.height <= min_height + 1:
                    raise ConfigError("Labirinth size is too small")
                elif maze.width <= min_width + 1:
                    raise ConfigError("Labirinth size is too small")
        except ConfigError as err:
            print(f"[Warning] 42 pattern ommited due to forbidden "
                  f"placement: {err}.")
            valid = False
        return valid

    def generate_seed(self) -> str:
        seed = ''
        for _ in range(15):
            seed += f'{rand.randrange(16):X}'
        return seed
