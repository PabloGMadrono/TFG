#!/usr/bin/env python3
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import heapq

# 1. A* that returns the path, not just the distance.
def heuristic(a, b):
    """Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, grid):
    """Return valid neighbors (up, down, left, right) that are not obstacles (value != 1)."""
    neighbors = []
    rows, cols = grid.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr, nc] != 1:  # Not an obstacle
                neighbors.append((nr, nc))
    return neighbors

def reconstruct_path(came_from, current):
    """Reconstructs the path from 'current' back to the start using the 'came_from' dict."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def astar_path(grid, start, goal):
    """
    A* that returns the actual path (list of (row, col)) from start to goal.
    Returns an empty list if no path is found.
    """
    if start == goal:
        return [start]
    
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    g_score = {start: 0}
    came_from = {}
    closed_set = set()
    
    while open_set:
        f, current_g, current = heapq.heappop(open_set)
        if current == goal:
            # Reconstruct the path
            return reconstruct_path(came_from, goal)
        
        if current in closed_set:
            continue
        closed_set.add(current)
        
        for neighbor in get_neighbors(current, grid):
            tentative_g = current_g + 1
            if neighbor in g_score and tentative_g >= g_score[neighbor]:
                continue
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g
            priority = tentative_g + heuristic(neighbor, goal)
            heapq.heappush(open_set, (priority, tentative_g, neighbor))
    
    return []  # No path found

def main():
    # 2. Load the supermarket map
    map_file = "data/mapaTFG.csv"
    # Adjust delimiter if needed (e.g., ";" instead of ",")
    grid = pd.read_csv(map_file, delimiter=",", header=None, dtype=int).to_numpy()
    
    # 3. Load the optimized route
    optimized_route_file = "output/optimized_route.json"
    with open(optimized_route_file, "r", encoding="utf-8") as f:
        route_data = json.load(f)
    
    route_list = route_data.get("route", [])
    print(f"Loaded route with {len(route_list)} nodes: {route_list}")
    
    # 4. Load product data (for mapping product -> (row, col))
    products_file = "data/products.json"
    with open(products_file, "r", encoding="utf-8") as f:
        products_data = json.load(f)

    # Create a dictionary: product_name -> (row, col)
    # If you have "starting_point" or "finishing_point" as gondola_id,
    # you should also handle those here, e.g.:
    product_coords = {}
    for gondola in products_data:
        row = gondola["y_coordinate"]
        col = gondola["x_coordinate"]
        gid = gondola["gondola_id"]
        if gid in ("starting_point", "finishing_point"):
            product_coords[gid] = (row, col)
        else:
            for product in gondola["list_of_products"]:
                product_coords[product] = (row, col)
    
    # Convert route (list of product/special node names) into coordinates
    route_coords = []
    for node in route_list:
        if node in product_coords:
            route_coords.append(product_coords[node])
        else:
            print(f"Warning: node '{node}' not found in product_coords.")
    
    # 5. Create a discrete colormap so gondolas (2) appear in yellow, etc.
    cmap = mcolors.ListedColormap(["lightgrey", "blue", "yellow", "purple"])
    # The boundaries for each color bin:
    #  - [ -0.5,  0.5) -> color index 0 (lightblue) -> for value 0
    #  - [ 0.5,  1.5) -> color index 1 (black)      -> for value 1
    #  - [ 1.5,  2.5) -> color index 2 (yellow)     -> for value 2
    #  - [ 2.5, 99.5) -> color index 3 (red)        -> for value 3..99
    bounds = [-0.5, 0.5, 1.5, 2.5, 99.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap=cmap, norm=norm)
    
    # 6. For each consecutive pair of route nodes, run A* to get the path around obstacles
    for i in range(len(route_coords) - 1):
        start = route_coords[i]
        goal = route_coords[i + 1]
        path = astar_path(grid, start, goal)
        
        # Plot each step in red
        for j in range(len(path) - 1):
            (r1, c1) = path[j]
            (r2, c2) = path[j + 1]
            plt.plot([c1, c2], [r1, r2], color="red", linewidth=2)
        
        # Optionally mark each path point with a red dot
        # for (r, c) in path:
        #     plt.scatter(c, r, color="red", s=10)
    
    plt.title("Supermarket Map with Actual Route (Avoiding Obstacles)")

    # If you want (0,0) at the bottom-left, uncomment:
    # plt.gca().invert_yaxis()
    
    plt.show()

if __name__ == "__main__":
    main()
