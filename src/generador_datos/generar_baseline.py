#!/usr/bin/env python3
import json
import os

import sys
"""
sys.path.insert(0, "/Users/pablo/Documents/TFG/TFG/src/algoritimia")
from TSP_nearest_neighbor import find_best_route
"""
from src.algoritimia.TSP_nearest_neighbor import find_best_route

def main():
    products_file = "../../data/products.json"
    output_file = "../../data/baseline.json"

    # Load products from the JSON file.
    with open(products_file, "r", encoding="utf-8") as f:
        products_data = json.load(f)

    # Create an order that includes one product from each gondola.
    # If you want to ignore special nodes (e.g., starting_point or finishing_point),
    # you can skip gondolas with such IDs.
    order_products = []
    for gondola in products_data:
        gondola_id = gondola.get("gondola_id")
        # Skip special nodes if desired. Uncomment the following lines if you want to skip them:
        # if gondola_id in ("starting_point", "finishing_point"):
        #     continue
        
        # If the gondola has at least one product, choose one (here we choose the first).
        products = gondola.get("list_of_products", [])
        if products:
            order_products.append(products[0])
        else:
            # Optionally, handle gondolas with an empty product list.
            print(f"Warning: Gondola {gondola_id} has no products; skipping.")

    # Create the order dictionary.
    orders = []
    order = {
        "order_id": 0,
        "products": order_products
    }
    orders.append(order)
    # Save the order to a JSON file.
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4)

    print(f"Order created with {len(order_products)} products and saved to '{output_file}'.")


    ## Ejecutar TSP para encontrar ruta optima que visita todas las gondolas

    find_best_route(orders_file=output_file, product_distances_file="../../data/product_distances.json", output_file="../../output/baseline_full_route.json")

if __name__ == "__main__":
    main()
