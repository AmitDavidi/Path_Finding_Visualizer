
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/AmitDavidi/Path_Finding_Visualizer)

# Path-Finding Algorithm Visualizer

This is a simple path-finding algorithm visualizer using the Pygame library. It allows you to draw barriers on the grid and visualize path-finding algorithms like A* and Dijkstra's algorithm.

## Requirements
- Python 3.x
- Pygame library

## Usage

1. Install Python and the Pygame library if you don't have them already.
   ```bash
   pip install pygame
   ```

2. Copy and paste the provided code into a Python file (e.g., `path_finding_visualizer.py`).

3. Run the Python script.
   ```bash
   python path_finding_visualizer.py
   ```

4. The GUI window will open, showing a grid with start and end points at the top-left and bottom-right corners, respectively. You can draw barriers on the grid using the left mouse button and erase them with the right mouse button.

5. Press `M` or the "Menu" button to open the menu, where you can choose the algorithm (A* or Dijkstra) and other options.

6. To visualize the chosen algorithm, click the "Start" button or press `Space`.

7. To generate a random maze, press `D`.

8. To clear the board, press `C`.

## Features

- Left-click on the grid to draw barriers.
- Right-click on the grid to remove barriers.
- Middle-click (scroll wheel) on the grid to set weighted paths.
- Press `M` or the "Menu" button to open the menu and select the algorithm.
- Press `Space` or the "Start" button to visualize the chosen algorithm.
- Press `C` to clear the board.
- Press `D` to generate a random maze.

## Controls

- Left mouse button: Draw barriers
- Right mouse button: Remove barriers
- Middle mouse button (scroll wheel): Set weighted paths
- `M`: Open the menu
- `Space`: Start the algorithm visualization
- `C`: Clear the board
- `D`: Generate a random maze

## Notes

- The available algorithms are A* and Dijkstra's algorithm.
- The visualization will show the path found by the chosen algorithm from the start point (top-left) to the end point (bottom-right).

Have fun visualizing different path-finding algorithms!
