A-Maze-ing 🌀

"A labyrinth is not a place to be lost, but a path to be found." — Anonymous


Description
A-Maze-ing is a Python project that generates mazes procedurally and displays them visually. Given a configuration file, the program produces a valid maze — optionally perfect (with exactly one path between entry and exit) — encodes it in a hexadecimal wall format, writes it to an output file, and renders it either in the terminal (ASCII) or via a graphical window (MiniLibX).
Key features:

Random maze generation with seed-based reproducibility
BFS-based shortest path solver (entry → exit)
Hexadecimal wall encoding per cell (N/E/S/W bitmask)
Terminal ASCII rendering and MiniLibX graphical display
Embedded "42" pattern made of fully closed cells
Reusable mazegen package installable via pip
Full flake8 and mypy compliance


Instructions
Requirements

Python 3.10 or later
pip (or uv, pipx)
MiniLibX (for graphical display)

Installation
Clone the repository and install the package in editable mode:
bashgit clone <repo-url> a-maze-ing
cd a-maze-ing
make install
The make install target runs:
bashpip install -e .
This creates a dynamic link so any changes to mazegen/ take effect immediately without reinstalling.
Running
bashpython3 a_maze_ing.py config.txt
Or via Make:
bashmake run
Debug mode
bashmake debug
Lint
bashmake lint
Runs:
bashflake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
Clean
bashmake clean
Removes __pycache__, .mypy_cache, and other artifacts.

Configuration File Format
The configuration file uses one KEY=VALUE pair per line. Lines starting with # are comments and are ignored.
Mandatory keys
KeyDescriptionExampleWIDTHMaze width (number of cells)WIDTH=20HEIGHTMaze height (number of cells)HEIGHT=15ENTRYEntry coordinates (x,y)ENTRY=0,0EXITExit coordinates (x,y)EXIT=19,14OUTPUT_FILEName of the output fileOUTPUT_FILE=maze.txtPERFECTWhether the maze is perfectPERFECT=True
Optional keys
KeyDescriptionExampleSEEDRandom seed for reproducibilitySEED=42ALGORITHMGeneration algorithm (e.g. recursive_backtracker, prim, kruskal)ALGORITHM=recursive_backtracker
Example config.txt
# A-Maze-ing default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=recursive_backtracker

Output File Format
Each cell is encoded as a single hexadecimal digit where each bit represents a wall:
BitDirection0 (LSB)North1East2South3West
A closed wall sets the bit to 1; an open passage sets it to 0.

Cells are written row by row, one row per line.
After an empty line, three additional lines follow:

Entry coordinates (x,y)
Exit coordinates (x,y)
Shortest path from entry to exit using letters N, E, S, W



Example:
9515...
EBAB...
...

1,1
19,14
SWSESWSE...NENEE

Maze Generation Algorithm
Algorithm chosen: Recursive Backtracker (DFS)
The Recursive Backtracker (also known as the Depth-First Search maze algorithm) was chosen as the primary generation algorithm.
How it works

Start from a random cell and mark it as visited.
Randomly choose an unvisited neighbour, remove the wall between them, and move there.
Repeat recursively until no unvisited neighbours remain.
Backtrack to a previous cell that still has unvisited neighbours.
Continue until all cells have been visited.

Why this algorithm

Perfect mazes by default: DFS naturally produces a spanning tree — exactly one path between any two cells — which directly satisfies the PERFECT=True requirement.
Visual quality: It generates long, winding corridors that look natural and challenging.
Simplicity: Easy to implement, understand, and audit — critical for peer evaluation.
Seed reproducibility: Combined with random.seed(), it produces identical mazes from the same seed.
Well-understood complexity: O(n) time and space, where n is the number of cells.

For the non-perfect variant (PERFECT=False), extra passages are randomly added after generation by removing additional walls, creating loops and multiple valid paths.

Visual Representation
The program supports two display modes:
Terminal (ASCII)
Characters and ANSI colours are used to render walls, the entry point, the exit point, and the solution path directly in the terminal. A menu below the maze offers:
==== A-Maze-ing ====
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze colors
4. Quit
Choice (1-4):
Graphical (MiniLibX)
A pixel-based window renders the maze with coloured walls. Key bindings shown at the bottom of the window:
1: regen;  2: path;  3: color;  4: quit
The "42" pattern is drawn using fully closed cells and can optionally be highlighted in a distinct colour.

Code Reusability — mazegen Package
The maze generation logic is isolated in the mazegen/ module, installable via pip.
Structure
mazegen/
├── __init__.py
├── generator.py    # MazeGenerator class — parsing, generation, BFS solver
└── display.py      # MazeDisplay class — terminal and graphical rendering
Installation
bashpip install mazegen-1.0-py3-none-any.whl
# or from source:
pip install -e .
Basic usage
pythonfrom mazegen.generator import MazeGenerator

# Instantiate with a config file
gen = MazeGenerator("config.txt")

# Access the generated grid (List[List[int]], hex-encoded walls)
grid = gen.get_grid()

# Access entry and exit as (row, col) tuples
entry = gen.get_entry()
exit_  = gen.get_exit()

# Access the BFS shortest path as a list of (row, col) tuples
path = gen.get_solution()
Custom parameters (without config file)
pythonfrom mazegen.generator import MazeGenerator

gen = MazeGenerator.from_params(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    perfect=True,
    seed=42
)

grid   = gen.get_grid()
path   = gen.get_solution()

Note: The grid format used internally by the module is a List[List[int]] where each integer is the same 4-bit wall bitmask as in the output file (N=bit0, E=bit1, S=bit2, W=bit3). This is the same format as the output file.

Building the package from source
bash# In a virtualenv:
python -m venv .venv && source .venv/bin/activate
pip install build
python3 -m build
cp dist/mazegen-1.0-py3-none-any.whl .

Team & Project Management
Team members and roles
MemberRolelogin1Frontend — mazegen/display.py, terminal/MiniLibX rendering, colour system, user interactionslogin2 (Pedro)Backend — mazegen/generator.py, config parser, maze generation algorithm, BFS solver, output file writer
Integration
Both branches (frontend and backend(pedro)) were merged into a shared dev branch following the integration manual. The main entry point a_maze_ing.py connects the backend generator to the frontend display by passing grid, start, end, and path directly to MazeDisplay.
Anticipated planning vs. actual
PhasePlannedActual outcomeBackend: parser + generatorWeek 1Completed on scheduleFrontend: terminal displayWeek 1Completed on scheduleFrontend: MiniLibX displayWeek 2Slightly delayed — MiniLibX Python bindings required additional setupIntegration (merge to dev)Week 2Required conflict resolution in a_maze_ing.pyBFS solver + output fileWeek 2Completed; validated against subject's validation scriptLinting (flake8 + mypy)Week 3All warnings resolved; zero errorsPackage build (.whl)Week 3Completed; file committed to repo rootREADME + documentationWeek 3Completed
What worked well

Separating frontend and backend into distinct branches allowed parallel development without conflicts until integration.
Using pip install -e . eliminated all import path issues across the project.
BFS is straightforward to verify manually, making debugging the solver easy.
The pyproject.toml approach made packaging trivial.

What could be improved

The MiniLibX integration was more complex than expected; a pure Python fallback (e.g. pygame or tkinter) would reduce the setup friction for evaluators.
More unit tests should be written, especially for edge cases in the maze validator (e.g. 2×2 grids, corridors wider than 2 cells).
The "42" pattern placement logic could be more flexible for small maze sizes.

Tools used

Git — version control and branch management
flake8 — PEP 8 style enforcement
mypy — static type checking
pytest — unit tests (not submitted)
build — Python package generation
MiniLibX (mlx_py) — graphical window
Claude (Anthropic) — see AI usage below


Resources
Maze generation references

Maze generation algorithms — Wikipedia
Jamis Buck's Mazes for Programmers blog series
Think Labyrinth — Walter D. Pullen
Breadth-First Search — Wikipedia
Python pyproject.toml packaging guide
MiniLibX documentation

All AI was used to understand procedures and clarifyng some new concepts and help with validations exercices and help for testing some features.