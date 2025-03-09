def get_distance(distances, a, b):
    """
    Returns the distance between nodes 'a' and 'b' using the distances dictionary.
    Checks both directions and, if not found, returns float('inf').
    If a or b is a dictionary (e.g. a product node), extract its 'name' field.
    """
    # Check if 'a' is a dict before extracting the name.
    if isinstance(a, dict):
        a = a.get("name", a)
    # Check if 'b' is a dict before extracting the name.
    if isinstance(b, dict):
        b = b.get("name", b)

    if a in distances and b in distances[a]:
        return distances[a][b]
    elif b in distances and a in distances[b]:
        return distances[b][a]
    else:
        return float('inf')
