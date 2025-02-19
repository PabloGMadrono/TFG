#!/usr/bin/env python3
import numpy as np
import pandas as pd
import json
import heapq
import os

# --- A* Algorithm Implementation ---

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
            # Cell is traversable if it's not an obstacle (i.e., not 1)
            if grid[nr, nc] != 1:
                neighbors.append((nr, nc))
    return neighbors

def astar(grid, start, goal):
    """
    Compute shortest path distance between start and goal on the grid using A*.
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
            tentative_g = current_g + 1  # each move has a cost of 1
            if neighbor in g_score and tentative_g >= g_score[neighbor]:
                continue
            g_score[neighbor] = tentative_g
            heapq.heappush(open_set, (tentative_g + heuristic(neighbor, goal), tentative_g, neighbor))
    
    # Return infinity if no path is found
    return float('inf')

# --- Main Script ---
def main():
    # Paths to input files
    map_file = 'data/mapaTFG.csv'
    products_file = 'data/products.json' 

    # Load the map as a NumPy array.
    # Make sure the delimiter here matches your CSV file's actual delimiter.
    try:
        grid = pd.read_csv(map_file, delimiter=",", dtype=int, encoding="utf-8-sig", header=None).to_numpy()

        print("Map loaded successfully. Grid shape:", grid.shape)
    except Exception as e:
        print(f"Error loading map: {e}")
        return

    # Load gondola information from the JSON file.
    try:
        with open(products_file, 'r') as f:
            # The JSON is expected to be a list of gondola dictionaries.
            data = json.load(f)
        print(f"Products JSON loaded successfully. Number of gondolas: {len(data)}")
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    # Build a dictionary mapping each gondola_id to its (row, col) coordinate.
    # Here we assume: y_coordinate -> row, x_coordinate -> col.
    gondola_coords = {}
    for gondola in data:
        try:
            gondola_id = gondola["gondola_id"]
            # If your grid's coordinate system is reversed relative to your JSON,
            # swap the following assignments.
            row = gondola["y_coordinate"]
            col = gondola["x_coordinate"]
            # Print a warning if the coordinate appears out-of-bound.
            if not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]):
                print(f"Warning: Gondola {gondola_id} coordinate {(row, col)} is out of grid bounds {grid.shape}.")
                # If you suspect the coordinates are swapped, try:
                # row, col = gondola["x_coordinate"], gondola["y_coordinate"]
                # print(f"  -> After swapping, gondola {gondola_id} coordinate becomes {(row, col)}")
            gondola_coords[gondola_id] = (row, col)
            print(f"Gondola {gondola_id} located at {(row, col)}")
        except KeyError as e:
            print(f"Missing key {e} in gondola data: {gondola}")

    # Compute pairwise distances using the A* algorithm.
    distances = {}
    gondola_ids = list(gondola_coords.keys())
    n = len(gondola_ids)
    for i in range(n):
        id1 = gondola_ids[i]
        distances[id1] = {}
        for j in range(i, n):
            id2 = gondola_ids[j]
            if i == j:
                # Distance from a node to itself is 0.
                dist = 0
            else:
                start = gondola_coords[id1]
                goal = gondola_coords[id2]
                dist = astar(grid, start, goal)
            distances[id1][id2] = dist
            # Ensure symmetry: distance from id2 to id1 is the same.
            distances.setdefault(id2, {})[id1] = dist
            #print(f"Distance between gondola {id1} and {id2}: {dist}")

    # Save the computed distances for later use (e.g., by a TSP optimizer).
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'gondola_distances.json')
    try:
        with open(output_file, 'w') as f:
            json.dump(distances, f, indent=4)
        print(f"\nPairwise gondola distances have been saved to {output_file}")
    except Exception as e:
        print(f"Error saving output JSON: {e}")

if __name__ == '__main__':
    main()
