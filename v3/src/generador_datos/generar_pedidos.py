#!/usr/bin/env python3
import random
from v3.src.files_management.json_management import load_file, save_file
from v3.src.files_management.file_names import pedidos_file, products_file


def generarate_pedidos(products_file, pedidos_file, num_orders, min_length, max_length):
    """
        Function that generates a list of pedidos and saves it to a file based on the parameters.
    """
    # Path to the products file produced earlier.

    product_data = load_file(products_file)

    # Collect all available product IDs (names) from the product data.
    # Each entry in product_data is expected to be a dict with key "list_of_products".
    available_products = []
    for entry in product_data:
        available_products.extend(entry["list_of_products"])

    print(f"Total available products: {len(available_products)}")

    # Generate 50 simulated orders.
    simulated_orders = []

    for order_id in range(num_orders):
        # Determine a random order length.
        order_length = random.randint(min_length, max_length)

        # If order_length is less than or equal to the number of available products,
        # pick unique products. Otherwise, allow duplicates.
        if order_length <= len(available_products):
            order_products = random.sample(available_products, order_length)
        else:
            order_products = random.choices(available_products, k=order_length)

        order_entry = {
            "order_id": order_id,
            "products": order_products
        }
        simulated_orders.append(order_entry)

    save_file(pedidos_file, simulated_orders)



def main():
    # Path to the products file produced earlier.
    #products_file = "../../data/products.json"
    num_orders = 50
    min_length = 8
    max_length = 40
    #output_file = "../../data/pedidos.json"
    generarate_pedidos(products_file, pedidos_file, num_orders, min_length, max_length)




if __name__ == '__main__':
    main()
