import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

'''
def main():
    map_file = "../../data/mapaTFG.csv"
    grid = pd.read_csv(map_file, delimiter=",", header=None, dtype=int).to_numpy()

    # Load the optimized route JSON
    optimized_route_file = "output/optimized_route.json"
    with open(optimized_route_file, "r", encoding="utf-8") as f:
        route_data = json.load(f)
    route_list = route_data.get("route", [])

    # Load the products JSON
    products_file = "data/products.json"
    with open(products_file, "r", encoding="utf-8") as f:
        products_data = json.load(f)

    # Build a dict to map product -> (row, col) and handle special nodes
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

    # Convert the route into coordinates
    route_coords = []
    for node in route_list:
        if node in product_coords:
            route_coords.append(product_coords[node])
        else:
            print(f"Warning: node '{node}' not found in product_coords.")

    # Create a discrete colormap
    cmap = mcolors.ListedColormap(["lightgrey", "blue", "yellow", "purple"])
    bounds = [-0.5, 0.5, 1.5, 2.5, 99.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # Plot
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap=cmap, norm=norm)

    # Draw the route
    for i in range(len(route_coords) - 1):
        (r1, c1) = route_coords[i]
        (r2, c2) = route_coords[i + 1]
        plt.plot([c1, c2], [r1, r2], color="red", linewidth=2)

    for (r, c) in route_coords:
        plt.scatter(c, r, color="red", s=30)

    plt.title("Supermarket Map with Optimized Route")

    # plt.gca().invert_yaxis()  # Uncomment if needed
    plt.show()


if __name__ == "__main__":
    main()
'''