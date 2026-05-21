from typing import List, Any
from mlx import Mlx

class MazeDisplay:
    def __init__(self) -> None:
        self.grid: List[List[int]] = [
            [9, 2, 3],
            [12, 0, 2],
            [5, 4, 6]
        ]
        self.m: Mlx = Mlx()
        self.mlx_ptr: Any = self.m.mlx_init()
        self.win_ptr: Any = self.m.mlx_new_window(self.mlx_ptr, 800, 600, "A-Maze-ing")
    
    def render_terminal(self) -> None:
        print("=== Test Maze ===")
        for row in self.grid:
            formated_line = " ".join(f"{cell:X}" for cell in row)
            print(formated_line)

    def run(self) -> None:
        print("A abrir a janela gráfica...")
        self.m.mlx_loop(self.mlx_ptr)
