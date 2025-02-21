#!/usr/bin/env python3
import pandas as pd
import heapq
from v2.src.files_management.file_names import map_file, products_file, gondolas_distances_file
from v2.src.files_management.json_management import load_file, save_file


# --- A* Algorithm Implementation ---
def heuristic(a, b):
    """Compute Manhattan distance between points a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos, grid):
    """Return valid neighboring cells (up, down, left, right) that are traversable.
       Traversable cells are those with value 0 (free), 2 (normal gondola), or 99 (start/finish)."""
    neighbors = []
    rows, cols = grid.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = pos[0] + dr, pos[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            # A cell is traversable if it's not an obstacle (i.e. not 1)
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
def calcular_distancias_gondolas(map_file, products_file, output_file):


    # Load the map as a NumPy array.
    try:
        grid = pd.read_csv(map_file, delimiter=",", dtype=int, encoding="utf-8-sig", header=None).to_numpy()
        print("Map loaded successfully. Grid shape:", grid.shape)
    except Exception as e:
        print(f"Error loading map: {e}")
        return

    # Load gondola (and special points) information from the JSON file.
    data = load_file(products_file)

    # Build a dictionary mapping each gondola_id to its (row, col) coordinate.
    # We assume: y_coordinate -> row, x_coordinate -> col.
    gondola_coords = {}
    for gondola in data:
        try:
            gondola_id = gondola["gondola_id"]
            row = gondola["y_coordinate"]
            col = gondola["x_coordinate"]
            # Check that the coordinate is within the map bounds.
            if not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]):
                print(f"Warning: Gondola {gondola_id} coordinate {(row, col)} is out of grid bounds {grid.shape}.")
            gondola_coords[gondola_id] = (row, col)
            print(f"Gondola {gondola_id} located at {(row, col)}")
        except KeyError as e:
            print(f"Missing key {e} in gondola data: {gondola}")

    # Optional: Warn if starting or finishing point is missing.
    if "starting_point" not in gondola_coords:
        print("Warning: No starting point found in the products JSON.")
    if "finishing_point" not in gondola_coords:
        print("Warning: No finishing point found in the products JSON.")

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
                dist = 0  # Distance from a node to itself is 0.
            else:
                start_coord = gondola_coords[id1]
                goal_coord = gondola_coords[id2]
                dist = astar(grid, start_coord, goal_coord)
            distances[id1][id2] = dist
            # Ensure symmetry: distance from id2 to id1 is the same.
            distances.setdefault(id2, {})[id1] = dist

    # Remove distance entries from a product to the starting point.
    # That is, for every gondola that is not the starting point, remove the key "starting_point" if it exists.
    for gondola_id in distances:
        if gondola_id != "starting_point":
            if "starting_point" in distances[gondola_id]:
                del distances[gondola_id]["starting_point"]

    # Save the computed distances for later use (e.g., by a TSP optimizer).
    """
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    """

    save_file(output_file, distances)


# --- Main Script ---
def main():

    calcular_distancias_gondolas(map_file, products_file, output_file=gondolas_distances_file)

if __name__ == '__main__':
    main()
