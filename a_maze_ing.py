#!/usr/bin/env python3

import sys
from src.config import Config, ConfigError
from src.mazegen import MazeGenerator
from src.interface import MazeDisplay


def main() -> None:
    print("=== A-Maze-ing ===")
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return
    file = sys.argv[1]
    print(f"\n--- Reading and parsing {file}")
    try:
        config = Config(file)
    except ConfigError as err:
        print(err)
        return
    config.print()
    # hex_map = "b93d3\nc2c3a\n9696a\nabed2\nc4556"  # NENWNWSSWSSEN
    # maze = MazeGenerator(config, hex_map)
    maze = MazeGenerator(config)
    print(f"\n--- Creating maze based on {file} data")

    # print("- Maze initial map")
    # print(maze.initial_state)
    # print("\n- Maze normalized map")
    # print(maze)

    # if len(maze.paths) > 0:
    #     for solution in maze.paths:
    #         print(f"Solution - {len(solution)}:")
    #         [print(f"{(cell.y, cell.x)} -> ", end='') for cell in solution]
    #         print()
    # else:
    #     print("None")

    # print()
    # print(maze)
    # print(f"Entry: {maze.entry}")
    # print(f"Exit: {maze.exit}")

    # print("\n------------------------\n")
    # test_map_regen(maze)

    # print("\n------------------------\n")
    # test_all_walls_synced(maze)
    grid: list[list[int]] = []
    for row in maze.rows:
        line: list[int] = []
        grid.append(line)
        for cell in row:
            line.append(cell.value)
    path: list[tuple[int, int]] = []
    for cell in maze.solution:
        path.append(cell.coord)
    print(f"Entry: {maze.entry} | Exit {maze.exit}")
    print(f"Seed: {maze.seed}")
    # print("Counter: ")
    # [print(f"{item}, ", end='') for item in maze.counter]
    # display = MazeDisplay(grid, maze.entry, maze.exit, path)
    display = MazeDisplay(maze, grid, maze.entry, maze.exit, path)
    display.render_terminal()
    display.run()


def test_map_regen(maze: MazeGenerator) -> None:
    print("Map before regen:")
    print(maze.map_hex)
    maze.regenerate_map()
    print("Map after regen:")
    print(maze.map_hex)
    # print("\n- Maze initial map")
    # print(maze.initial_state)
    # print("\n- Maze normalized map")
    # print(maze)
    # print()


def test_all_walls_synced(maze: MazeGenerator) -> None:
    print("Is all boundaries of all cells in sync? "
          f"{maze.check_all_boundaries()}")
    print("\nModify a cell to break wall sync")
    x, y = input("Modify cell in coordinates (x, y): ").split(' ')
    wall, value = input("Choose a wall and new value: ").split(' ')
    maze.rows[int(y)][int(x)].set_bit(int(wall), int(value))
    print(maze)
    print("Is all boundaries of all cells in sync? "
          f"{maze.check_all_boundaries()}")


if __name__ == "__main__":
    main()
