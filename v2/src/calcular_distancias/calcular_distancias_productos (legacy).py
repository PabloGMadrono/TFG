#!/usr/bin/env python3
import numpy as np
import pandas as pd
import json
import heapq
import os


# --- A* Algorithm Implementation ---
'''
def heuristic(a, b):
    """Compute Manhattan distance between points a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos, grid):
    """Return valid neighboring cells (up, down, left, right) that are traversable.
       Traversable cells are those with value 0 (free) or 2 (gondola)."""
    neighbors = []
    rows, cols = grid.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            # Allow cells that are not obstacles (i.e. any cell that is not 1)
            if grid[nr, nc] != 1:
                neighbors.append((nr, nc))
    return neighbors


def astar(grid, start, goal):
    """
    Compute the shortest path distance between start and goal on the grid using A*.
    Returns the distance (number of steps) or float('inf') if no path is found.
    """
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    g_score = {start: 0}
    closed_set = set()

    while open_set:
        f, current_g, current = heapq.heappop(open_set)
        if current == goal:
            return current_g  # path length

        if current in closed_set:
            continue
        closed_set.add(current)

        for neighbor in get_neighbors(current, grid):
            tentative_g = current_g + 1  # each move costs 1
            if neighbor in g_score and tentative_g >= g_score[neighbor]:
                continue
            g_score[neighbor] = tentative_g
            heapq.heappush(open_set, (tentative_g + heuristic(neighbor, goal), tentative_g, neighbor))

    # Return infinity if no path is found
    return float('inf')


# --- Main Script ---
def main():
    # Paths to input files
    map_file = '../../data/mapaTFG.csv'
    products_file = '../../data/products.json'

    # Load the map as a NumPy array.
    # Adjust the delimiter if necessary (e.g., if your CSV uses a comma or semicolon).
    try:
        grid = pd.read_csv(map_file, delimiter=",", header=None, dtype=int, encoding="utf-8-sig").to_numpy()
        print("Map loaded successfully. Grid shape:", grid.shape)
    except Exception as e:
        print(f"Error loading map: {e}")
        return

    # Load product (gondola) information from the JSON file.
    try:
        with open(products_file, 'r', encoding='utf-8') as f:
            # The JSON is expected to be a list of gondola dictionaries.
            data = json.load(f)
        print(f"Products JSON loaded successfully. Number of gondolas: {len(data)}")
    except Exception as e:
        print(f"Error loading products JSON: {e}")
        return

    # Build a dictionary mapping each product to its grid coordinate.
    # Each gondola in the JSON has a list_of_products; all products at the same gondola share its coordinate.
    product_locations = {}
    for gondola in data:
        try:
            # Use y_coordinate as row and x_coordinate as column.
            coord = (gondola["y_coordinate"], gondola["x_coordinate"])
            for product in gondola["list_of_products"]:
                product_locations[product] = coord
        except KeyError as e:
            print(f"Missing key {e} in gondola data: {gondola}")

    print(f"Total products found: {len(product_locations)}")

    # Compute pairwise distances between products using A*.
    distances = {}
    product_names = list(product_locations.keys())
    n = len(product_names)
    for i in range(n):
        prod1 = product_names[i]
        distances[prod1] = {}
        for j in range(i, n):
            prod2 = product_names[j]
            if i == j:
                d = 0  # Distance to itself is 0
            else:
                start = product_locations[prod1]
                goal = product_locations[prod2]
                d = astar(grid, start, goal)
            distances[prod1][prod2] = d
            distances.setdefault(prod2, {})[prod1] = d  # Ensure symmetry
            # print(f"Distance between {prod1} and {prod2}: {d}")

    # Save the computed product distances for later use.
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'product_distances.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(distances, f, indent=4)
        print(f"\nPairwise product distances have been saved to {output_file}")
    except Exception as e:
        print(f"Error saving output JSON: {e}")


if __name__ == '__main__':
    main()
'''