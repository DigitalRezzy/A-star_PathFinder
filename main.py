import pygame
from queue import PriorityQueue

# Window Setup
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# RGB colours used to colour-code the grid/node states
RED = (255, 0, 0) # Closed Node
GREEN = (0, 255, 0) # Open Node (queued to be evaluated)
WHITE = (255, 255, 255) # Empty Node
BLACK = (0, 0, 0) # Barrier
PURPLE = (128, 0, 128) # Final path
ORANGE = (255, 128, 0) # Starting node
GREY = (128, 128, 128) # Grid line borders
TURQUOISE = (64, 224, 208) # End/Target node

class Node:
    # Represents one cell/square on the grid
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # Getters

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    # Setters that make the colors of the nodes/tiles different

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE


    def draw(self, win):
        # Draws the node onto the pygame display surface
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        # Checks orthogonal adjacent nodes (Down, Up, Right, Left) and adds valid non-barriers
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #Left
            self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        # Less-than comparator fallback required by PriorityQueue when F-scores tie
        return False

def h(p1, p2):
    # Calculates Manhattan distance heuristic H(n) between two points
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    # Backtracks from destination to start using the came_from map to draw the shortest path
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    # Core A* Pathfinding implementation
    count = 0 # Tie-breaker counter for PriorityQueue insertions
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # Tuple structure: (f_score, insertion_index, node)

    came_from = {} # Tracks previous node in the optimal path

    # Initialize G-scores (exact path cost from start) to infinity
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    # Initialize F-scores (estimated total path cost: G + H) to infinity
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # Set mirror to keep track of items inside PriorityQueue (PriorityQueue doesn't support 'in' lookup easily)
    open_set_hash = {start}

    while not open_set.empty():
        # Keep Pygame responsive while algorithm runs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Pop node with lowest F-score
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # Target reached — reconstruct final path
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        # Evaluate adjacent valid nodes
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 # Distance to adjacent neighbor is 1 step

            # If a shorter path to this neighbor is discovered
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw() # Redraw visualization frame

        # Mark current node as evaluated (closed set)
        if current != start:
            current.make_closed()

    return False # No valid path exists

def make_grid(rows, width):
    # Constructs a 2D array populated with Node instances
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    # Draws grid lines on top of nodes for clear grid boundaries
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    # Main rendering function: fills canvas, draws nodes, grid lines, and updates window
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    # Converts screen mouse coordinates (x, y) into grid matrix coordinates (row, col)
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # Left mb to place start/end/barriers
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # Right mb to erase nodes
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                # Press 'Space' to begin search
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # Press 'C' to clear the grid
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)

    pygame.quit()

main(WIN, WIDTH)





