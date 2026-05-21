from mazegen.display import MazeDisplay

def main() -> None:
    display = MazeDisplay()
    display.render_terminal()
    display.run()

if __name__ == "__main__":
    main()