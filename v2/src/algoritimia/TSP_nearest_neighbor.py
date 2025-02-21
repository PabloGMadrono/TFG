#!/usr/bin/env python3
from itertools import permutations
import time
from v2.src.files_management.file_names import product_distances_file, optimized_route_file, pedidos_file
from v2.src.files_management.json_management import load_file, save_file



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

def brute_force_tsp(product_list, distances):
    """
    Solves the TSP exactly by checking all permutations of the middle nodes.
    The route must start with 'starting_point' and end with 'finishing_point'.
    Returns the route with minimal total distance and that distance.
    """
    if "starting_point" not in product_list or "finishing_point" not in product_list:
        raise ValueError("Both 'starting_point' and 'finishing_point' must be in the product list.")

    # Build list of middle nodes (all nodes except starting_point and finishing_point)
    middle_nodes = [node for node in product_list if node not in ("starting_point", "finishing_point")]

    best_route = None
    best_distance = float('inf')
    for perm in permutations(middle_nodes):
        route = ["starting_point"] + list(perm) + ["finishing_point"]
        total_distance = 0
        for i in range(len(route) - 1):
            d = get_distance(distances, route[i], route[i + 1])
            total_distance += d
            if total_distance >= best_distance:
                # Early stopping: no need to continue this permutation.
                break
        if total_distance < best_distance:
            best_distance = total_distance
            best_route = route

    return best_route, best_distance

def find_best_route(order, output_file, product_distances_file=product_distances_file):
    order_id = order.get("order_id", "N/A")
    product_list = order.get("products", [])

    print(f"Optimizing route for order {order_id} with {len(product_list)} products and {len(product_list) + 2} nodes.")

    # Ensure that the special nodes are in the product list.
    if "starting_point" not in product_list:
        product_list.insert(0, "starting_point")
    if "finishing_point" not in product_list:
        product_list.append("finishing_point")

    product_distances = load_file(product_distances_file)

    # Use brute-force if the number of nodes is small (< 12), else use nearest neighbor.
    # Numero de productos <= 12
    if len(product_list) < 15:
        print("Using brute-force TSP solver.")
        route, total_distance = brute_force_tsp(product_list, product_distances)
    else:
        print("Using nearest neighbor TSP solver.")
        route, total_distance = forced_nearest_neighbor_tsp(product_list, product_distances)

    result = {
        "order_id": order_id,
        "route": route,
        "total_distance": total_distance
    }

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
    start_time = time.time()
    find_best_route(order=order, output_file=optimized_route_file)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")


if __name__ == '__main__':
    main()
