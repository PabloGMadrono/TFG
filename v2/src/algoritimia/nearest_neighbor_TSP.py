from v2.src.algoritimia.get_distance import get_distance


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




def main():
    ...

if __name__ == '__main__':
    main()
