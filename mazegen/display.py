from typing import List, Any
from mlx import Mlx
import os

class MazeDisplay:
    def __init__(self) -> None:
        self.grid: List[List[int]] = [
            [9, 2, 3],
            [12, 0, 2],
            [5, 4, 6]
        ]
        self.block_size: int = 64
        self.m: Mlx = Mlx()
        self.mlx_ptr: Any = self.m.mlx_init()
        self.win_ptr: Any = self.m.mlx_new_window(self.mlx_ptr, 800, 600, "A-Maze-ing")
        self.m.mlx_hook(self.win_ptr, 33, 0, self.close_window, 0)
        self.m.mlx_hook(self.win_ptr, 2, 1, self.handle_keypress, 0)

    def render_terminal(self) -> None:
        print("=== Test Maze ===")
        for row in self.grid:
            formated_line = " ".join(f"{cell:X}" for cell in row)
            print(formated_line)

    def run(self) -> None:
        print("Opening A-Maze-ing graphic window...")
        self.draw_maze()
        self.m.mlx_loop(self.mlx_ptr)

    def close_window(self, *args: Any) -> int:
            print("Closing A-Maze-ing...")
            #self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            os._exit(0)

    def handle_keypress(self, keycode: int, param: int) -> int:
        print(f"Pressed key: {keycode}")
        if keycode == 65307:
            os._exit(0)
        return 0

    def draw_maze(self) -> None:
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = col * self.block_size
                y = row * self.block_size

                cell_value = self.grid[row][col]
                self.draw_block(x, y, 0xFFFFFF)

        