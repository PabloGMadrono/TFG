from itertools import permutations
from v3.src.algoritimia.get_distance import get_distance


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



def main():
    ...

if __name__ == '__main__':
    main()
