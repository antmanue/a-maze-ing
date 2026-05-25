from typing import List, Any
from mlx import Mlx
import os

class MazeDisplay:
    def __init__(self) -> None:
        self.grid: List[List[int]] = [
            [600, 600, 600],
            [600, 600, 600],
            [600, 600, 600]
        ]
        self.block_size: int = 64
        self.m: Mlx = Mlx()
        self.mlx_ptr: Any = self.m.mlx_init()
        self.win_ptr: Any = self.m.mlx_new_window(self.mlx_ptr, 800, 600, "A-Maze-ing")
        self.m.mlx_hook(self.win_ptr, 33, 0, self.close_window, 0)
        self.m.mlx_hook(self.win_ptr, 2, 1, self.handle_keypress, 0)
        self.m.mlx_hook(self.win_ptr, 12, 0, self.draw_maze_expose, 0)

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
        elif keycode == 109:
            print(f"A desenhar o labirinto...")
            self.draw_maze()
        return 0

    def draw_maze_expose(self, *args: Any) -> int:
            self.draw_maze()
            self.drawn = True

    def draw_maze(self) -> None:
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = col * self.block_size
                y = row * self.block_size

                cell_value = self.grid[row][col]

                if cell_value & 1:
                    for pixel_x in range(x, (x + self.block_size)):
                        self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,pixel_x, y, 0xFFFFFFFF)
                if cell_value & 2:
                    for pixel_y in range(y, (y + self.block_size)):
                        self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,x + self.block_size, pixel_y, 0xFFFFFFFF)        
                if cell_value & 4:
                    for pixel_x in range(x, (x + self.block_size)):
                        self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,pixel_x, y + self.block_size, 0xFFFFFFFF)
                if cell_value & 8:
                    for pixel_y in range(y, (y + self.block_size)):
                        self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr,x, pixel_y, 0xFFFFFFFF)
              #  self.draw_block(x, y, 0xFFFFFF)

    

    #def draw_block(self, start_x: int, start_y: int, color: int) -> None:
     #   for y in range(start_y, (start_y + self.block_size)):
      #      for x in range(start_x, (start_x + self.block_size)):
       #         self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)