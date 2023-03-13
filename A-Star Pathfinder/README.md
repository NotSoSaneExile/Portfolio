# A* Pathfinding Algorithm
The A* pathfinding algorithm is a popular and widely used algorithm in the field of Artificial Intelligence and robotics. It is a heuristic search algorithm that is used to find the shortest path between two points in a weighted graph.

In this code, we use the A* algorithm to find the shortest path between two points on a 2D grid. We use Pygame to create a graphical representation of the grid and the search algorithm.

# How to Use
First, make sure you have Python 3.x installed on your computer. Then, you need to install the Pygame and Colorspy library. You can install them using pip by typing the following command in your terminal:

`pip install pygame`
`pip install colorspy`

Once Pygame is installed, you can run the code by typing the following command in your terminal:

`python main.py`

__+ The code will open a Pygame window showing a grid. The start point is marked in blue, the end point is marked in orange, and the obstacles are marked in black.__ 
__+ First two clicks of the left mouse button would apply the start/end nodes. Afterwards you can add obstacles to the grid by clicking on a cell. You can reset the node by clicking on the cell with your right mouse button.__
__+ To start the search algorithm, press the space bar. You can also press the 'C' key to clear the grid and ESC to close the program. Current version locks the mouse inside the grid to prevent indexes crashing.__

# Code Overview
The code consists of several components:

* Node: This class represents a node in the grid. It has properties such as its position in the grid, its color, and whether it is a barrier or not.
* make_grid: This function creates the grid by initializing Node objects for each cell.
* draw_grid: This function draws the grid lines on the Pygame window.
* draw: This function draws the nodes and grid lines on the Pygame window.
* heuristic: This function calculates the heuristic value for a given node. In this case, we use the Manhattan distance as the heuristic value.
* Astar: This function implements the A* algorithm to find the shortest path between two points on the grid.
* get_mouse_cursor_position: This function returns the row and column of the node that the user clicks on.

# Acknowledgments
This program was created with the help of the Tech with Tim tutorial. The tutorial provides a detailed explanation of the A* algorithm and how it can be implemented in Python using Pygame. Special thanks to Tim for creating such an informative and helpful tutorial!

# License:

This program is licensed under the MIT License. Please see the LICENSE file for more details.
