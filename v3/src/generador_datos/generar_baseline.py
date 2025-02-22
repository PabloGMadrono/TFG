#!/usr/bin/env python3

from v3.src.visualizaciones.visualizacion_ruta_obstaculos import generate_visualizacion_route
"""
sys.path.insert(0, "/Users/pablo/Documents/TFG/TFG/src/algoritimia")
from TSP_nearest_neighbor import find_best_route
"""
from v3.src.algoritimia.find_best_route import find_best_route
from v3.src.files_management.json_management import save_file, load_file
from v3.src.files_management.file_names import products_file, baseline1_order_file, baseline1_route_file


def generate_baseline_1_order(products_file, baseline1_order_file):
    """Generates a full route through the whole supermarket."""


    products_data = load_file(products_file)

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

    save_file(baseline1_order_file, orders)

def generate_baseline1_route(baseline1_order_file, output_file):
    orders = load_file(baseline1_order_file)

    if not orders:
        print("No orders found in the file.")
        return
    order = orders[0]

    find_best_route(order=order)


def main():

    generate_baseline_1_order(products_file=products_file, baseline1_order_file=baseline1_order_file)
    generate_baseline1_route(baseline1_order_file, output_file=baseline1_route_file)
    generate_visualizacion_route(baseline1_route_file, products_file)


if __name__ == "__main__":
    main()
