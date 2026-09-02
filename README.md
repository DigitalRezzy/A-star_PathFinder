# A* Pathfinding Algorithm Visualizer

An interactive desktop application built with **Python** and **Pygame** that visualizes how the **A* (A-Star) Pathfinding Algorithm** calculates the shortest path between two points around user-defined barriers in real-time.

---

## 1. Project Overview

> I built this application to gain hands-on experience with pathfinding algorithms, priority queues, and graph traversal in Python. It provides a visual interface for understanding how search algorithms evaluate nodes in real-time. I have always had a particular interest with path-finding algorithms due to how satisfying it is to view a computer use maths to find the shortest path between two points so quickly.

---

## 2. Visual Demonstrations & Screenshots

| Initial Setup & Barriers | Algorithm In Progress | Final Shortest Path |
| :---: | :---: | :---: |
| ![Setup Screenshot](screenshots/setup.png) | ![In Progress Screenshot](screenshots/in_progress.png) | ![Final Path Screenshot](screenshots/final_path.png) |
| *Placing start, end, and wall nodes* | *Open (Green) and Closed (Red) sets* | *Reconstructed path (Purple)* |

---

## 3. What is an A* Search Algorithm?

A* is an **informed search algorithm** (also known as a best-first search) designed to find the shortest path between a starting node and a target node on a weighted graph or grid. Unlike uniform searches like Dijkstra’s algorithm (which explores blindly in all directions) or Greedy Best-First search (which aggressively chases the target and can get stuck in dead ends), A* strikes an optimal balance between past path cost and estimated remaining distance.

### The Mathematics Behind A*
A* evaluates candidate nodes using the cost function:

$$F(n) = G(n) + H(n)$$

* **$G(n)$ — Exact Past Cost:** The total distance accumulated traveling from the start node to the current node $n$. In this grid implementation, moving orthogonally to an adjacent tile increases $G(n)$ by $1$.
* **$H(n)$ — Heuristic Future Estimate:** An educated guess of the remaining distance from node $n$ to the goal. This program uses the **Manhattan Distance** heuristic, which calculates distance along vertical and horizontal grid lines ignoring barriers:
  $$H(p_1, p_2) = |x_1 - x_2| + |y_1 - y_2|$$
* **$F(n)$ — Total Score:** The estimated total cost of the complete route passing through node $n$. 

### Priority Queue Expansion
1. The algorithm maintains an **Open Set** (a priority queue) containing all candidate nodes to be evaluated.
2. At each iteration, A* pops the node with the lowest $F(n)$ score from the priority queue.
3. If $H(n)$ is **admissible** (it never overestimates the actual distance to the goal), A* is mathematically guaranteed to return the shortest possible path once the target node is reached.

---

## 4. Codebase & Software Architecture

### Key Classes and Functions

* **`Node` (Class):** Represents an individual cell on the grid matrix. Handles node state (start, end, barrier, open, closed, path), draws the grid cell rectangle on screen, and updates valid adjacent neighbors (up, down, left, right).
* **`algorithm()`:** The main A* execution loop. Manages the priority queue (`open_set`), evaluates neighboring nodes, updates minimum $G$ and $F$ scores, and triggers visual updates frame-by-frame.
* **`reconstruct_path()`:** Backtracks from the destination node to the start using a `came_from` dictionary map, coloring the optimal path purple.
* **`make_grid()` & `draw()`:** Constructs a 2D $50 \times 50$ array of `Node` instances and handles frame rendering (nodes and grid overlay lines).
* **`get_clicked_pos()`:** Translates screen pixel mouse coordinates $(x, y)$ into grid matrix indices $(\text{row}, \text{col})$.

### Color Code Legend

| Color | State / Role | Description |
| :--- | :--- | :--- |
| 🟧 **Orange** | Start Node | Origin point for the pathfinding search |
| 🩵 **Turquoise** | Target Node | Destination endpoint |
| ⬛ **Black** | Barrier / Wall | Impassable obstacle nodes |
| 🟩 **Green** | Open Set | Candidate nodes discovered and queued in the `PriorityQueue` |
| 🟥 **Red** | Closed Set | Nodes already evaluated |
| 🟪 **Purple** | Final Path | The optimal shortest path constructed by A* |
| ⬜ **White** | Empty Space | Unvisited navigable grid tiles |

---

## 5. How to Run & Controls

### Prerequisites
* **Python 3.x**
* **Pygame** library

```bash
pip install pygame
