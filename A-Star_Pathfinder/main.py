import pygame
import math
from queue import PriorityQueue
from sys import exit
import colorspy as colors

WIDTH = 600
pygame.init()
pygame.font.init()
WINDOW = pygame.display.set_mode((WIDTH, WIDTH), pygame.NOFRAME)
pygame.event.set_grab(True)

class Node:
    """This class represents the singular node which is gonna be printed on the pygame board"""
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.width = width #the width of the node
        self.x = row * width #x coordinate of the node which we want to generate on the board
        self.y = column * width #y coordinate of the node which we want to generate on the board
        self.color = colors.white
        self.neighbours = []
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.column
    
    def is_closed(self):
        return self.color == colors.red
    
    def is_open(self):
        return self.color == colors.green
    
    def is_barrier(self):
        return self.color == colors.black
        
    def is_start(self):
        return self.color == colors.blue
    
    def is_end(self):
        return self.color == colors.orange
    
    def reset(self):
        self.color = colors.white
        
    def make_closed(self):
        self.color = colors.red
    
    def make_open(self):
        self.color = colors.green
    
    def make_barrier(self):
        self.color = colors.black
    
    def make_start(self):
        self.color = colors.blue
    
    def make_end(self):
        self.color = colors.orange
    
    def make_path(self):
        self.color = colors.cyan
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbours(self, grid):
        """
           Updating the neighbours for each traversed node
           Visually it would look like this:
           X|U|X
           L|C|R
           X|D|X
           Where: C is the current node, N is the neighbour.
           IMPORTANT! Pygame indexes at (0, 0) from the top left corner and starts incrementing going right ->
        """
        self.neighbours = []
        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier(): #Checking the UP neighbour
            self.neighbours.append(grid[self.row - 1][self.column]) 
            
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_barrier(): #Checking the DOWN neighbour
            self.neighbours.append(grid[self.row + 1][self.column])
        
        if self.column > 0 and not grid[self.row][self.column - 1].is_barrier(): #Checking the LEFT neighbour
            self.neighbours.append(grid[self.row][self.column - 1])
                    
        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_barrier(): #Checking the RIGHT neighbour
            self.neighbours.append(grid[self.row][self.column + 1])
    
# Define the heuristic function (in this case, the Manhattan distance/Taxicab geometry)
def heuristic(p1, p2):
    """A taxicab geometry or a Manhattan geometry is a geometry whose usual distance function or metric of Euclidean geometry is replaced by a new metric
       in which the distance between two points is the sum of the absolute differences of their Cartesian coordinates.
       :param p1: first point ex. p1(5, 8)
       :param p2: the second point ex. p2(10, 39)"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + (y1 - y2)

def make_grid(rows, width):
    """Creating the base for the grid"""
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    
    return grid

def draw_grid(window, rows, width):
    gap = width // rows
    # width: The width of our entire grid (ex: 800px)
    # rows: How many rows we have (ex: 50)
    # gap: indicates what the width of each spot (node) should be (ex: 800px/50 = 16px)
    for i in range(rows):
        pygame.draw.line(window, colors.gray, (0, i * gap), (width, i * gap))
        # draws a horizontal line from (x=0, y=i*gap) --> (x=width, y=i*gap)
    for i in range(rows):
        pygame.draw.line(window, colors.gray, (i * gap, 0), (i * gap, width))
        # draws a vertical line from (x=i*gap, y=0) --> (x=i*gap, y=width)
            
def draw(window, grid, rows, width):
    window.fill(colors.white)
    
    for row in grid:
        for node in row:
            node.draw(window)
    
    draw_grid(window, rows, width)
    pygame.display.update()
    
def get_mouse_cursor_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    
    row = y // gap
    col = x // gap
    
    return row, col

# Define the function to draw the path
def draw_path(path, current, draw):
    while current in list(path.keys())[2:]:
        current = path[current]
        current.make_path()
        draw()

def astar(draw, grid, start, end):
    """
    A* algorithm implementation
    :param draw: the draw function
    :param grid: the grid on which the draw function is gonna work
    :param start: the start node
    :param end: the end node
    """
    # Initialize the open set (use a priority queue to get the node with the lowest f-score)
    when_put = 0
    open_set = PriorityQueue()
    open_set.put((0, when_put, start))
    open_set_hash = {start}
    # Initialize the g-score table for nodes
    g_score = {node: float("inf") for row in grid for node in row}
    
    # Initialize the g-score of the start node to 0
    g_score[start] = 0
    
    # Initialize the f-score table for nodes
    f_score = {node: float("inf") for row in grid for node in row}
    
    # Initialize the f-score of the start node to the heuristic estimate of the cost to reach the goal from the start node
    f_score[start] = heuristic(start.get_pos(), end.get_pos())
    
    # Initialize the set of visited nodes
    visited = {}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #! pressing ESC closes the program
                    pygame.quit()
                    return
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            draw_path(path=visited, current=end, draw=draw)
            end.make_end()
            return True
                
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbour]:
                visited[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = heuristic(neighbour.get_pos(), end.get_pos()) + temp_g_score
                if neighbour not in open_set_hash:
                    when_put += 1
                    open_set.put((f_score[neighbour], when_put, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
                    
        draw()

        if current != start:
            current.make_closed()
            
    return False

def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    
    start = None
    end = None
    
    run = True
    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #! pressing ESC closes the program
                    pygame.quit()
                    return
            
            if pygame.mouse.get_pressed()[0]: #! [0] stands for LMB
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_cursor_position(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                    
                elif not end and node != start:
                    end = node
                    end.make_end()
                
                elif node != start and node != end:
                    node.make_barrier()
                         
            elif pygame.mouse.get_pressed()[2]: #! [2] stands for RMB
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_cursor_position(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: #! Pressing the space after start and end nodes are set will begin the algorithm
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                            
                    astar(lambda: draw(window, grid, ROWS, width), grid, start, end)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: #! pressing the 'c' on keyboard clears the screen
                    start = None
                    end = None
                    for row in grid:
                        for node in row:
                            node.reset()

main(WINDOW, WIDTH)