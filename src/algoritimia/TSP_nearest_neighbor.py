#!/usr/bin/env python3
import json
import os
from src.files_management.file_names import product_distances_file, optimized_route_file, pedidos_file

from src.files_management.json_management import load_file, save_file



def get_distance(distances, a, b):
    """
    Returns the distance between nodes 'a' and 'b' using the distances dictionary.
    Checks both directions and, if not found, returns float('inf').
    """
    if a in distances and b in distances[a]:
        return distances[a][b]
    elif b in distances and a in distances[b]:
        return distances[b][a]
    else:
        return float('inf')


def forced_nearest_neighbor_tsp(product_list, distances):
    """
    Solves the TSP using a nearest neighbor heuristic, forcing the route to begin
    with 'starting_point' and end with 'finishing_point'.
    
    Parameters:
      product_list: List of product nodes to visit.
      distances: Nested dictionary with distances between nodes.
      
    Returns:
      A tuple (route, total_distance) where:
        - route: Ordered list of nodes, starting with 'starting_point' and ending with 'finishing_point'.
        - total_distance: Total distance of the computed route.
    """
    # At this point, we assume the product_list already includes the two special nodes.
    if "starting_point" not in product_list or "finishing_point" not in product_list:
        raise ValueError("Both 'starting_point' and 'finishing_point' must be in the product list.")

    # Remove the special nodes from the set of nodes to be optimized.
    middle_nodes = set(product_list)
    middle_nodes.discard("starting_point")
    middle_nodes.discard("finishing_point")

    # Initialize route with the starting point.
    route = ["starting_point"]
    total_distance = 0
    current = "starting_point"

    # While there are nodes left in the middle, pick the nearest one.
    while middle_nodes:
        next_node = min(middle_nodes, key=lambda x: get_distance(distances, current, x))
        d = get_distance(distances, current, next_node)
        total_distance += d
        route.append(next_node)
        middle_nodes.remove(next_node)
        current = next_node

    # Finally, go from the last middle node to the finishing point.
    d = get_distance(distances, current, "finishing_point")
    total_distance += d
    route.append("finishing_point")

    return route, total_distance


def find_best_route(order, output_file, product_distances_file=product_distances_file):


    order_id = order.get("order_id", "N/A")
    product_list = order.get("products", [])

    print(f"Optimizing route for order {order_id} with {len(product_list)} products.")

    # Ensure that the special nodes are in the product list.
    if "starting_point" not in product_list:
        product_list.insert(0, "starting_point")
    if "finishing_point" not in product_list:
        product_list.append("finishing_point")

    product_distances = load_file(product_distances_file)


    try:
        route, total_distance = forced_nearest_neighbor_tsp(product_list, product_distances)
    except ValueError as ve:
        print(f"Error: {ve}")
        return

    result = {
        "order_id": order_id,
        "route": route,
        "total_distance": total_distance
    }

    # Create the output directory if necessary.
    """
    directory = os.path.dirname(output_file)
    if directory:
        os.makedirs(directory, exist_ok=True)
    """

    save_file(output_file, result)

    print("Route:", route)
    print("Total distance:", total_distance)

    return route, total_distance


def main():


    orders = load_file(pedidos_file)

    if not orders:
        print("No orders found in the file.")
        return

    # For this example, we take the first order.
    print(orders)
    order = orders[0]

    find_best_route(order=order, output_file=optimized_route_file)



if __name__ == '__main__':
    main()
