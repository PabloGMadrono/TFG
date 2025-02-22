import math
from v2.src.algoritimia.get_distance import get_distance



def held_karp_tsp(product_list, distances):
    """
    Solves the TSP exactly using dynamic programming (Held-Karp algorithm)
    for a route that starts with "starting_point" and ends with "finishing_point".

    It assumes product_list is a list of nodes where:
      - product_list[0] == "starting_point"
      - product_list[-1] == "finishing_point"
      - The middle nodes (indices 1 .. n-2) are the ones to be permuted.

    Returns:
      A tuple (optimal_route, best_cost) where:
        - optimal_route is a list of node names in order.
        - best_cost is the total distance.
    """
    # Let n = total number of nodes, and M = number of middle nodes.
    n = len(product_list)
    if n < 3:
        # Only start and finish exist.
        return product_list, get_distance(distances, product_list[0], product_list[-1])

    M = n - 2  # indices 1 ... n-2 are middle nodes.
    # Map middle node indices: 0,..., M-1 correspond to product_list[1] ... product_list[n-2]
    # We'll use dp[mask][j] where mask is a bitmask of length M and j in [0, M-1] is the last visited middle.
    dp = [[math.inf] * M for _ in range(1 << M)]
    parent = [[None] * M for _ in range(1 << M)]

    # Base case: for each middle node j, route from start to product_list[j+1]
    for j in range(M):
        dp[1 << j][j] = get_distance(distances, product_list[0], product_list[j + 1])

    # Iterate over all subsets of middle nodes.
    for mask in range(1 << M):
        for j in range(M):
            if mask & (1 << j):  # if j is in the current mask
                # Try to extend the path by visiting a new node k not in mask.
                for k in range(M):
                    if mask & (1 << k) == 0:  # if k is not visited yet
                        next_mask = mask | (1 << k)
                        new_cost = dp[mask][j] + get_distance(distances, product_list[j + 1], product_list[k + 1])
                        if new_cost < dp[next_mask][k]:
                            dp[next_mask][k] = new_cost
                            parent[next_mask][k] = j

    # Final step: from one of the middle nodes, go to finishing_point.
    full_mask = (1 << M) - 1
    best_cost = math.inf
    best_last = None
    for j in range(M):
        cost = dp[full_mask][j] + get_distance(distances, product_list[j + 1], product_list[-1])
        if cost < best_cost:
            best_cost = cost
            best_last = j

    # Reconstruct the path for the middle nodes.
    path_middle = []
    mask = full_mask
    j = best_last
    while j is not None:
        path_middle.append(j)
        next_j = parent[mask][j]
        mask = mask & ~(1 << j)
        j = next_j
    path_middle.reverse()

    # Build the complete route: start, then middle nodes (translated back to product_list indices), then finish.
    optimal_route = [product_list[0]]  # starting_point
    for j in path_middle:
        optimal_route.append(product_list[j + 1])
    optimal_route.append(product_list[-1])  # finishing_point

    return optimal_route, best_cost
