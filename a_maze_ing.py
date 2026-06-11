#!/usr/bin/env python3

import sys
from src.io import Config, ConfigError
from src.logic import MazeGenerator
from src.ui import MazeDisplay


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
    print()
    gen = MazeGenerator(config)
    display = MazeDisplay(gen)
    # display.render_terminal()
    display.run()


if __name__ == "__main__":
    main()
