# typings/mlx/__init__.pyi
from typing import Any


class Mlx:
    def mlx_init(self) -> Any: ...

    def mlx_new_window(self, mlx_ptr: Any, size_x: int, size_y: int,
                       title: str) -> Any: ...

    def mlx_hook(self, win_ptr: Any, x_event: int, x_mask: int, funct: Any,
                 param: Any) -> int: ...

    def mlx_loop(self, mlx_ptr: Any) -> None: ...

    def mlx_pixel_put(self, mlx_ptr: Any, win_ptr: Any, x: int, y: int,
                      color: int) -> int: ...
