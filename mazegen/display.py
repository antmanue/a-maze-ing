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
            [15,  2,  15,  2,  15,  15,  15],
            [15, 0,  15,  0,  5,  0,  15],  
            [15, 15, 15, 12, 15,  15,  15],  
            [12, 0, 15,  0, 15,  0,  6],  
            [12, 4,  15,  4,  15,  15,  15],  
            #[9, 2, 3],
            #[12, 0, 2],
            #[15, 4, 6],
        ]
        self.start = start
        self.end = end
        self.path = path if path is not None else [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
        
        self.block_size: int = 16
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
            0xFFFFFFFF, #branco
            0xFF00FF00, #verde
            0xFF0000FF, #azul
            0xFFFFFF00, #amarelo
            0xFFF88379 #coral
        ]
        self.color_index: int = 0

        #Small Maze
        if len(self.grid) < 5 or len(self.grid[0]) < 7:
            print("Maze is too small to draw '42'")

    def render_terminal(self) -> None:
        print("=== Test Maze ===")
        for row in self.grid:
            formated_line = " ".join(f"{cell:X}" for cell in row)
            print(formated_line)

    def run(self) -> None:
        print("Opening A-Maze-ing graphic window...")
        print("Press C to change color")
        print("Press P to turn on/off the path")
        print("Press R to redraw a new maze color")
        self.m.mlx_loop(self.mlx_ptr)

    def close_window(self, *args: Any) -> int:
        print("Closing A-Maze-ing...")
        #self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        os._exit(0)

    def handle_keypress(self, keycode: int, param: int) -> int:
        print(f"Pressed key: {keycode}")
        # Tecla ESC Exit
        if keycode == 65307:
            os._exit(0)
        # Tecla 'C' Change color    
        elif keycode == 99:
            print("Maze color has been changed")
            self.color_index = (self.color_index + 1) % len(self.wall_colors)
            self.needs_update = True
        # Tecla 'P' Liga/Desliga o caminho da solucao
        elif keycode == 112:
            self.show_path = not self.show_path
            self.needs_update = True
        # Tecla 'R' Regen Maze
        elif keycode == 114:
            print("Redrawing maze...")
            self.needs_update = True
        return 0

    def draw_maze_expose(self, *args: Any) -> int:
        self.draw_maze()
        self.drawn = True
        return 0
    
    def draw_rect(self, start_x: int, start_y: int, width: int, height: int, color: int) -> None:
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def draw_maze(self) -> None:

        self.draw_rect(0, 0, self.window_width, self.window_height, 0XFF000000)
        
        thick = self.wall_thickness

        #Layer 1
        for row in range (len(self.grid)):
            for col in range (len(self.grid[row])):
                if self.grid[row][col] == 15:
                    x = col * self.block_size
                    y = row * self.block_size
                    self.draw_rect(x + thick, y + thick, self.block_size - (2 * thick), self.block_size -(2 *thick), 0xFFD3D3D3)

        #Layer 2
        if self.show_path and len(self.path) > 0:
            pt = self.path_thickness
            half_block = self.block_size // 2

            for i in range (len(self.path) - 1):
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

        #Layer 3
        half_block = self.block_size // 2

        start_col, start_row = self.start
        st_cx = start_col * self.block_size
        st_cy = start_row * self.block_size
        self.draw_rect(st_cx, st_cy, 12, 12, 0xFF00FF00)

        end_col, end_row = self.end
        ed_cx = end_col * self.block_size
        ed_cy = end_row * self.block_size
        self.draw_rect(ed_cx, ed_cy, 12, 12, 0xFFFF0000)

        #Layer 4
        current_color = self.wall_colors[self.color_index]

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = col * self.block_size
                y = row * self.block_size
                cell_value = self.grid[row][col]

                #Wall N
                if cell_value & 1:
                    self.draw_rect(x, y, self.block_size, thick, current_color)
                #Wall E
                if cell_value & 2:
                    self.draw_rect(x + self.block_size - thick, y, thick, self.block_size, current_color)
                #Wall S
                if cell_value & 4:
                    self.draw_rect(x, y + self.block_size - thick, self.block_size, thick, current_color)
                #Wall W
                if cell_value & 8:
                    self.draw_rect(x, y, thick, self.block_size, current_color)

    def draw_maze_hook(self, *args: Any) -> int:
        if self.needs_update is True:
            self.draw_maze()
            self.needs_update = False
        return 0
        
    
