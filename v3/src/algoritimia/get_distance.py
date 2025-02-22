


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
