#!/usr/bin/env python3
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

def main():
    # 1. Load the supermarket map as a NumPy array
    # Adjust delimiter if your CSV uses a semicolon or something else
    map_file = "data/mapaTFG.csv"
    grid = pd.read_csv(map_file, delimiter=",", header=None, dtype=int).to_numpy()

    # 2. Load the optimized route (from TSP)
    # The JSON is expected to have a structure like:
    # {
    #   "order_id": 0,
    #   "route": ["product 3", "product 10", ...],
    #   "total_distance": ...
    # }
    optimized_route_file = "output/optimized_route.json"
    with open(optimized_route_file, "r", encoding="utf-8") as f:
        route_data = json.load(f)

    route_list = route_data.get("route", [])
    print(f"Loaded route with {len(route_list)} products: {route_list}")

    # 3. Load product data (gondolas + products)
    # Each entry in products.json is something like:
    # {
    #   "gondola_id": 0,
    #   "x_coordinate": 5,
    #   "y_coordinate": 12,
    #   "list_of_products": ["product 1", "product 2", ...]
    # }
    products_file = "data/products.json"
    with open(products_file, "r", encoding="utf-8") as f:
        products_data = json.load(f)

    # Build a dict to map product -> (row, col)
    product_coords = {}
    for gondola in products_data:
        row = gondola["y_coordinate"]
        col = gondola["x_coordinate"]
        for product in gondola["list_of_products"]:
            product_coords[product] = (row, col)

    # Convert the route (list of products) into coordinates
    route_coords = []
    for product in route_list:
        if product in product_coords:
            route_coords.append(product_coords[product])
        else:
            print(f"Warning: product '{product}' not found in product_coords.")

    # 4. Plot the supermarket map and overlay the route
    plt.figure(figsize=(10, 10))
    # Show the map; a simple approach is to display the grid as an image.
    # You can experiment with different colormaps like 'Blues', 'gray', etc.
    plt.imshow(grid, cmap="Blues")

    # Overlay the route in red
    # We'll connect consecutive coordinates in the route with a line.
    for i in range(len(route_coords) - 1):
        (r1, c1) = route_coords[i]
        (r2, c2) = route_coords[i + 1]
        # Note that plt.plot expects x-coordinates first, so we use columns as x and rows as y.
        plt.plot([c1, c2], [r1, r2], color="red", linewidth=2)

    # Optionally, mark each route point with a red dot
    for (r, c) in route_coords:
        plt.scatter(c, r, color="red", s=30)

    plt.title("Supermarket Map with Optimized Route")
    plt.xlabel("Columns (x)")
    plt.ylabel("Rows (y)")

    # Optionally invert the y‐axis if you want (since in images y=0 is at the top).
    # plt.gca().invert_yaxis()

    plt.show()

if __name__ == "__main__":
    main()
