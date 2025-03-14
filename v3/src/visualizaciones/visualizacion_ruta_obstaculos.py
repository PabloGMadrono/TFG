import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import heapq
import os

from v3.src.calcular_distancias.calcular_distancias_gondolas import heuristic, get_neighbors
from v3.src.files_management.file_names import map_file, optimized_route_file, products_file, visualization_dir
from v3.src.files_management.file_names import pruebas_annealing_dir
from v3.src.files_management.json_management import load_file


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



def generate_visualizacion_route(optimized_route_file, products_file, map_file, selected_order_id=None):
    # Clear any previous plots and load the supermarket map
    grid = pd.read_csv(map_file, delimiter=",", header=None, dtype=int).to_numpy()

    # Load orders from JSON (each order is a dict in a list)
    orders = load_file(optimized_route_file)
    if not orders:
        print("No orders found in the file.")
        return

    # If the orders are in a dict (not a list), convert it to a list
    if isinstance(orders, dict):
        orders = [orders]

    # Load product data (for mapping product -> (row, col))
    products_data = load_file(products_file)

    # Create a dictionary mapping product names to coordinates
    product_coords = {}
    for gondola in products_data:
        row = gondola["y_coordinate"]
        col = gondola["x_coordinate"]
        gid = gondola["gondola_id"]
        if gid in ("starting_point", "finishing_point"):
            product_coords[gid] = (row, col)
        else:
            for product in gondola["list_of_products"]:
                # Check if product is a dictionary and extract its 'name'
                if isinstance(product, dict):
                    prod_name = product.get("name")
                else:
                    prod_name = product
                product_coords[prod_name] = (row, col)

    # Determine which orders to process: all orders if selected_order_id is None,
    # otherwise, find the order with the matching order_id.
    if selected_order_id is None:
        orders_to_process = orders
    else:
        selected_order = next((order for order in orders if order.get("order_id") == selected_order_id), None)
        if selected_order is None:
            print(f"Order with id {selected_order_id} not found.")
            return
        orders_to_process = [selected_order]

    # Process each order in the list
    for selected_order in orders_to_process:
        # Extract the route list from the selected order
        route_list = selected_order.get("route", [])
        print(f"Loaded route for order {selected_order.get('order_id')} with {len(route_list)} nodes: {route_list}")

        # Convert route (list of product/special node names) into coordinates.
        # If a node is a dictionary, extract its 'name' before the lookup.
        route_coords = []
        for node in route_list:
            if isinstance(node, dict):
                node_key = node.get("name")
            else:
                node_key = node
            if node_key in product_coords:
                route_coords.append(product_coords[node_key])
            else:
                print(f"Warning: node '{node_key}' not found in product_coords.")

        # Create a discrete colormap (example colors)
        cmap = mcolors.ListedColormap(["lightgrey", "blue", "yellow", "purple"])
        bounds = [-0.5, 0.5, 1.5, 2.5, 99.5]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        fig = plt.figure(figsize=(10, 10))
        plt.imshow(grid, cmap=cmap, norm=norm)

        # For each consecutive pair of route nodes, compute and plot the A* path
        for i in range(len(route_coords) - 1):
            start = route_coords[i]
            goal = route_coords[i + 1]
            path = astar_path(grid, start, goal)
            for j in range(len(path) - 1):
                (r1, c1) = path[j]
                (r2, c2) = path[j + 1]
                plt.plot([c1, c2], [r1, r2], color="red", linewidth=2)

        plt.title("Supermarket Map with Actual Route (Avoiding Obstacles)")
        # Instead of showing, save the visualization to file
        order_id = selected_order.get("order_id", "default")
        output_filename = os.path.join(visualization_dir, f"order_{order_id}_visualization.png")
        fig.savefig(output_filename)
        plt.close(fig)



def main():
    generate_visualizacion_route(optimized_route_file, products_file, map_file)




if __name__ == "__main__":
    main()
