from typing import Any
from mlx import Mlx  # type: ignore
import os
from ..logic import MazeGenerator, Algorithms


class MazeDisplay:
    """Manages window interface graphics and structural animations."""
    def __init__(self, generator: MazeGenerator) -> None:
        """Initializes engine layers, color tables, and screen specs."""

        # Data
        self.gen = generator
        self.grid = self.gen.maze.prepare_map_to_visual()
        self.start = self.gen.maze.entry
        self.end = self.gen.maze.exit
        self.path: list[tuple[int, int]] = []
        maze = self.gen.maze
        self.gen_iter = self.gen.backtracking(maze.get_cell(self.start))
        self.solut_iter = self.gen.generate_solution()
        self.state = "GENERATING_SOLUTION"
        self.count = 0

        self.block_size: int = 16
        # Grid
        self.window_width = self.gen.maze.width * self.block_size
        self.window_height = self.gen.maze.height * self.block_size
        # Init
        self.m: Mlx = Mlx()
        self.mlx_ptr: Any = self.m.mlx_init()
        self.win_ptr: Any = self.m.mlx_new_window(
            self.mlx_ptr, self.window_width,
            self.window_height,
            "A-Maze-ing"
            )
        # State
        self.needs_update: bool = True
        self.show_path: bool = True
        self.drawn: bool = False

        # Event hook
        self.m.mlx_hook(self.win_ptr, 33, 0, self.close_window, 0)
        self.m.mlx_hook(self.win_ptr, 2, 1, self.handle_keypress, 0)
        self.m.mlx_hook(self.win_ptr, 12, 0, self.draw_maze_expose, 0)
        self.m.mlx_loop_hook(self.mlx_ptr, self.draw_maze_hook, 0)

        # Walls
        self.wall_thickness: int = 1
        self.path_thickness: int = 6
        self.wall_colors: list[int] = [
            0xFFFFFFFF,  # branco
            0xFF00FF00,  # verde
            0xFF0000FF,  # azul
            0xFFFFFF00,  # amarelo
            0xFFF88379  # coral
        ]
        self.color_index: int = 0

    def run(self) -> None:
        """Launches execution window render interfaces and input loops."""
        print("Opening A-Maze-ing graphic window...")
        print("Press 'C' to change color")
        print("Press 'R' to re-generate the maze")
        print("Press 'ESC' to exit")

        print("\nFor the following options wait until maze is "
              "fully generated.")
        print("Press 'P' to turn on/off the path")
        print("Press 'I' to toggle between Perfect/Imperfect maze")
        print()
        if self.gen.error_42:
            print(f"[Warning] 42 pattern ommited due to forbidden "
                  f"placement: {self.gen.error_42}.")
        self.m.mlx_loop(self.mlx_ptr)

    def close_window(self, *args: Any) -> int:
        """Destroys active environment setups and cleanly terminates."""
        print("Closing A-Maze-ing...")
        # self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        os._exit(0)

    def handle_keypress(self, keycode: int, param: int) -> int:
        """Map actions based on user key inputs."""
        # Tecla ESC Exit
        if keycode == 65307:
            print()
            os._exit(0)
        # Tecla 'C' Change color
        elif keycode == 99:
            self.color_index = (self.color_index + 1) % len(self.wall_colors)
            self.needs_update = True
        # Tecla 'P' Liga/Desliga o caminho da solucao
        elif keycode == 112:
            if self.path:
                self.show_path = not self.show_path
                self.needs_update = True
        # Tecla 'R' Regen Maze
        elif keycode == 114:
            self.gen.regenerate_map()
            backtracking = self.gen.backtracking
            self.gen_iter = backtracking(self.gen.maze.get_cell(self.start))
            self.grid = self.gen.maze.prepare_map_to_visual()
            self.path = []
            self.needs_update = True
            self.state = "GENERATING_SOLUTION"
        elif keycode == 105:
            if self.path:
                self.gen.config.perfect = not self.gen.config.perfect
                self.needs_update = True
        return 0

    def draw_maze_expose(self, *args: Any) -> int:
        """Triggers refresh cycles under layout window focus events."""
        self.draw_maze()
        self.drawn = True
        return 0

    def draw_rect(
            self,
            start_x: int,
            start_y: int,
            width: int,
            height: int,
            color: int
            ) -> None:
        """Fills target screen quadrants with specific hex color values."""
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def draw_maze(self) -> None:
        """Renders matrix layouts, active paths, and gates cleanly."""

        self.draw_rect(0, 0, self.window_width, self.window_height, 0XFF000000)

        thick = self.wall_thickness

        # Layer 1

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 15:
                    x = col * self.block_size
                    y = row * self.block_size
                    self.draw_rect(
                            x + thick,
                            y + thick,
                            self.block_size - (2 * thick),
                            self.block_size - (2 * thick),
                            0xFFD3D3D3
                            )

        # Layer 2

        if self.show_path and len(self.path) > 0:
            pt = self.path_thickness
            half_block = self.block_size // 2

            for i in range(len(self.path) - 1):
                c1, r1 = self.path[i]
                c2, r2 = self.path[i+1]

                cx1 = c1 * self.block_size + half_block
                cy1 = r1 * self.block_size + half_block
                cx2 = c2 * self.block_size + half_block
                cy2 = r2 * self.block_size + half_block

                lx = min(cx1, cx2) - (pt // 2)
                ly = min(cy1, cy2) - (pt // 2)
                lw = abs(cx1 - cx2) + pt if cx1 != cx2 else pt
                lh = abs(cy1 - cy2) + pt if cy1 != cy2 else pt

                self.draw_rect(lx, ly, lw, lh, 0xFF289D8C)

        # Layer 3
        half_block = self.block_size // 2

        start_col, start_row = self.start
        st_cx = start_col * self.block_size
        st_cy = start_row * self.block_size
        self.draw_rect(st_cx, st_cy, 12, 12, 0xFF00FF00)

        end_col, end_row = self.end
        ed_cx = end_col * self.block_size
        ed_cy = end_row * self.block_size
        self.draw_rect(ed_cx, ed_cy, 12, 12, 0xFFFF0000)

        # Layer 4
        current_color = self.wall_colors[self.color_index]

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = col * self.block_size
                y = row * self.block_size
                cell_value = self.grid[row][col]

                # Wall N
                if cell_value & 1:
                    self.draw_rect(x, y, self.block_size, thick, current_color)
                # Wall E
                if cell_value & 2:
                    self.draw_rect(
                        x + self.
                        block_size - thick,
                        y,
                        thick,
                        self.block_size,
                        current_color
                        )
                # Wall S
                if cell_value & 4:
                    self.draw_rect(
                        x,
                        y + self.block_size - thick,
                        self.block_size,
                        thick,
                        current_color
                        )
                # Wall W
                if cell_value & 8:
                    self.draw_rect(x, y, thick, self.block_size, current_color)

    def draw_maze_hook(self, *args: Any) -> int:
        """Drives background frame transitions across iterative states."""
        size = self.gen.maze.height * self.gen.maze.width
        iter_Step = int(0.05*size)
        if iter_Step <= 1:
            iter_Step = 1
        if self.state == "GENERATING_SOLUTION":
            try:
                for _ in range(iter_Step):
                    next(self.gen_iter)
                self.grid = self.gen.maze.prepare_map_to_visual()
                self.draw_maze()
            except StopIteration:
                self.grid = self.gen.maze.prepare_map_to_visual()
                self.draw_maze()
                if not self.gen.maze.perfect:
                    self.gen_iter = self.gen.transform_to_imperfect_maze()
                    self.state = "BREAKING_WALLS"
                else:
                    self.solut_iter = self.gen.generate_solution()
                    self.state = "SOLVING"
        elif self.state == "BREAKING_WALLS":
            try:
                for _ in range(iter_Step):
                    next(self.gen_iter)
                self.grid = self.gen.maze.prepare_map_to_visual()
                self.draw_maze()
            except StopIteration:
                self.grid = self.gen.maze.prepare_map_to_visual()
                self.draw_maze()
                self.gen_iter = self.gen.look_for_invalid_neighbours()
                self.gen.clear_solutions()
                self.state = "VALIDATING_EMPTY_CELLS"
        elif self.state == "VALIDATING_EMPTY_CELLS":
            try:
                for _ in range(iter_Step):
                    next(self.gen_iter)
                self.grid = self.gen.maze.prepare_map_to_visual()
                self.draw_maze()
            except StopIteration:
                self.grid = self.gen.maze.prepare_map_to_visual()
                self.draw_maze()
                self.gen.solve_with(Algorithms.A_STAR)
                self.solut_iter = self.gen.generate_solution()
                self.state = "SOLVING"
        elif self.state == "SOLVING":
            try:
                for _ in range(iter_Step):
                    next_coord = next(self.solut_iter)
                    self.path.append(next_coord)
                self.grid = self.gen.maze.prepare_map_to_visual()
                self.draw_maze()
            except StopIteration:
                self.grid = self.gen.maze.prepare_map_to_visual()
                self.draw_maze()
                self.gen.export_generated_data()
                self.state = "DONE"
        if self.needs_update:
            if self.gen.config.perfect:
                maze_conf = "'Perfect'  "
            else:
                maze_conf = "'Imperfect'"
            path_status = str(self.show_path)
            if self.count:
                print("\033[F\033[K"
                      "\033[F\033[K"
                      "\033[F\033[K", end='')
            self.count += 1
            print(f"Seed: {self.gen.maze.seed}\n"
                  f"Path: {path_status}\n"
                  f"Maze configuration: {maze_conf}")
            self.draw_maze()
            self.needs_update = False
        return 0
