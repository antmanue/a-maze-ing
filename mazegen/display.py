from typing import List, Any, Tuple
from mlx import Mlx
import os

class MazeDisplay:
    def __init__(self,
                 grid: List[List[int]] = None,
                 start: Tuple[int, int] = (0, 0),
                 end: Tuple[int, int] = (2, 2),
                 path: List[Tuple[int, int]] = None) -> None:

        # Data
        self.grid = grid if grid is not None else [
            [9, 2, 3],
            [12, 0, 2],
            [5, 4, 6],
        ]

        self.start = start
        self.end = end
        self.path = path if path is not None else [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]
        
        self.block_size: int = 64
        # Grid
        self.window_width = len(self.grid[0]) * self.block_size
        self.window_height = len(self.grid) * self.block_size
        # Init
        self.m: Mlx = Mlx()
        self.mlx_ptr: Any = self.m.mlx_init()
        self.win_ptr: Any = self.m.mlx_new_window(self.mlx_ptr, self.window_width, self.window_height, "A-Maze-ing")
        # State
        self.needs_update: bool = True
        self.show_path: bool = True

        # Wall Colors Index
        self.wall_colors: List[int] = [0xFFFFFFFF, 0xFF00FF00, 0xFF0000FF, 0XFFFFFF00]
        self.color_index: int = 0


        # Event hook
        self.m.mlx_hook(self.win_ptr, 33, 0, self.close_window, 0)
        self.m.mlx_hook(self.win_ptr, 2, 1, self.handle_keypress, 0)
        self.m.mlx_hook(self.win_ptr, 12, 0, self.draw_maze_expose, 0)
        self.m.mlx_loop_hook(self.mlx_ptr, self.draw_maze_hook, 0)
        self.drawn: bool = False
        self.show_path: bool = True
        self.wall_colors: list[int] = [
            0xFFFFFFFF, #branco
            0xFF00FF00, #verde
            0xFF0000FF, #azul
            0xFFFFFF00, #amarelo
            0xFFF88379 #coral
        ]
        self.color_index: int = 0

    def render_terminal(self) -> None:
        print("=== Test Maze ===")
        for row in self.grid:
            formated_line = " ".join(f"{cell:X}" for cell in row)
            print(formated_line)

    def run(self) -> None:
        print("Opening A-Maze-ing graphic window...")
        self.m.mlx_loop(self.mlx_ptr)

    def close_window(self, *args: Any) -> int:
            print("Closing A-Maze-ing...")
            #self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            os._exit(0)

    def handle_keypress(self, keycode: int, param: int) -> int:
        print(f"Pressed key: {keycode}")
        if keycode == 65307:
            os._exit(0)
        # Tecla 'C' Change color    
        elif keycode == 99:
            self.color_index = (self.color_index + 1) % len(self.wall_colors)
            self.needs_update = True
        # Tecla 'P' Liga/Desliga o caminho da solucao
        elif keycode == 112:
            self.show_path = not self.show_path
            self.needs_update = True
        return 0

    def draw_maze_expose(self, *args: Any) -> int:
            self.draw_maze()
            self.drawn = True
    
    def draw_block(self, start_x: int, start_y: int, color: int) -> None:
            for y in range(start_y, (start_y + self.block_size)):
                for x in range(start_x, (start_x + self.block_size)):
                    self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def draw_maze(self) -> None:

        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)

        if self.show_path:
            for row, col in self.path:
                x = col * self.block_size
                y = row * self.block_size
                self.draw_block(x, y, 0xFF289D8C)
        
        start_row, start_col = self.start
        start_x = start_col * self.block_size
        start_y = start_row * self.block_size
        self.draw_block(start_x, start_y, 0xF500FF00)
        
        end_row, end_col = self.end
        end_x = end_col * self.block_size
        end_y = end_row * self.block_size
        self.draw_block(end_x, end_y, 0xFFFF0000)
        
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = col * self.block_size
                y = row * self.block_size

                cell_value = self.grid[row][col]

                if cell_value & 1:
                    for pixel_x in range(x, (x + self.block_size)):
                        self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,pixel_x, y, self.wall_colors[self.color_index])
                if cell_value & 2:
                    for pixel_y in range(y, (y + self.block_size)):
                        self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,x + self.block_size, pixel_y, self.wall_colors[self.color_index])        
                if cell_value & 4:
                    for pixel_x in range(x, (x + self.block_size)):
                        self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,pixel_x, y + self.block_size, self.wall_colors[self.color_index])
                if cell_value & 8:
                    for pixel_y in range(y, (y + self.block_size)):
                        self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,x, pixel_y, self.wall_colors[self.color_index])
        
    def draw_maze_hook(self, *args: Any) -> int:
        if self.needs_update is True:
            self.draw_maze()
            self.needs_update = False
        return 0
        
    