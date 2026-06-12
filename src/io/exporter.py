from ..models import Directions, Cell, Maze


class MazeExporter:
    """Saves maze tracking outputs and path elements to file."""
    def __init__(self,
                 output_file: str,
                 maze: Maze,
                 solution: list[Cell]):
        """Sets export destinations and target maze, solution."""
        self.output_file = output_file
        self.maze = maze
        self.solution = solution

    def generate_hex(self) -> str:
        """Converts live cell scores to flat hexadecimal map layouts."""
        map_hex: list[str] = []
        for row in self.maze.rows:
            row_str = ''
            for cell in row:
                hex_split = hex(cell.value).split('0x')
                hex_value = hex_split[1]
                row_str += hex_value
            map_hex.append(row_str)
        return '\n'.join(map_hex)

    def generate_path(self) -> str:
        """Translates movement into cardinal abbreviations."""
        path = ""
        for i, cell in enumerate(self.solution):
            if i < len(self.solution) - 1:
                next = self.solution[i + 1]
                direction = Directions.between(cell, next)
                path += Directions.get_orientation(direction)
        return path

    def generate_output(self) -> None:
        """Writes string translation of generated system into text file."""
        output = ""
        output += self.generate_hex() + "\n\n"
        output += str(self.maze.entry) + '\n'
        output += str(self.maze.exit) + '\n'
        output += self.generate_path() + '\n'
        with open(self.output_file, 'w') as file:
            file.write(output)
