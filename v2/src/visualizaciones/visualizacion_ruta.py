import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import networkx as nx
import itertools

from v2.src.files_management.file_names import map_file, optimized_route_file, products_file, product_distances_file
from v2.src.files_management.json_management import load_file, save_file

def main():
    # Load the grid map
    grid = pd.read_csv(map_file, delimiter=",", header=None, dtype=int).to_numpy()

    # Load the optimized route JSON
    route_data = load_file(optimized_route_file)
    route_list = route_data.get("route", [])

    # Load the products JSON
    products_data = load_file(products_file)

    # Build a dictionary mapping each product (or special node) to its (row, col) coordinate
    product_coords = {}
    for gondola in products_data:
        row = gondola["y_coordinate"]
        col = gondola["x_coordinate"]
        gid = gondola["gondola_id"]
        if gid in ("starting_point", "finishing_point"):
            product_coords[gid] = (row, col)
        else:
            for product in gondola["list_of_products"]:
                product_coords[product] = (row, col)

    # Load the products distances JSON
    distances = load_file(product_distances_file)

    # Create a NetworkX graph
    G = nx.Graph()

    # Add nodes using the route list. Positions are stored as (x, y) = (col, row)
    for node in route_list:
        if node in product_coords:
            row, col = product_coords[node]
            G.add_node(node, pos=(col, row))
        else:
            print(f"Warning: node '{node}' not found in product_coords.")

    # Add edges between every pair of nodes in route_list with weights from the distances file
    for n1, n2 in itertools.combinations(route_list, 2):
        if n1 in product_coords and n2 in product_coords:
            try:
                weight = distances[n1][n2]
            except KeyError:
                try:
                    weight = distances[n2][n1]
                except KeyError:
                    print(f"Warning: weight for edge {n1} - {n2} not found in both orders. Setting weight=0.")
                    weight = 0
            G.add_edge(n1, n2, weight=weight)
        else:
            print(f"Warning: edge between '{n1}' and '{n2}' has missing node coordinates.")

    print(G.number_of_nodes(), G.number_of_edges())

    # Extract node positions for drawing
    pos = nx.get_node_attributes(G, 'pos')

    # Create the plot
    plt.figure(figsize=(12, 12))
    plt.imshow(grid, cmap="Greys", alpha=0.3)

    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_color="red", node_size=300)

    # Draw all edges in blue
    nx.draw_networkx_edges(G, pos, edge_color="blue", width=1)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    # Highlight the selected TSP route in a different color
    # This is the ordered list of edges from the route
    selected_route_edges = [(route_list[i], route_list[i+1]) for i in range(len(route_list)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=selected_route_edges, edge_color="orange", width=2)

    plt.title("Complete Graph with TSP Nodes and Highlighted Route")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
