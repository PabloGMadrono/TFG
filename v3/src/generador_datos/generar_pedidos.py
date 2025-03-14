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


def generate_pedidos_for_lengths(products_file, pedidos_file, lengths, orders_per_length=2):
    """
    Generates orders with fixed lengths.
    """
    # Load the products data.
    product_data = load_file(products_file)

    # Collect all available product IDs (names) from the product data.
    available_products = []
    for entry in product_data:
        available_products.extend(entry["list_of_products"])

    print(f"Total available products: {len(available_products)}")

    simulated_orders = []
    order_id = 0

    # For each desired length, create the specified number of orders.
    for length in lengths:
        for i in range(orders_per_length):
            if length <= len(available_products):
                # Choose unique products if possible.
                order_products = random.sample(available_products, length)
            else:
                # Otherwise, allow duplicates.
                order_products = random.choices(available_products, k=length)

            order_entry = {
                "order_id": order_id,
                "products": order_products
            }
            simulated_orders.append(order_entry)
            order_id += 1

    save_file(pedidos_file, simulated_orders)
    print(f"Generated {len(simulated_orders)} orders and saved to {pedidos_file}.")


def main():
    """
    num_orders = 50
    min_length = 8
    max_length = 40
    generarate_pedidos(products_file, pedidos_file, num_orders, min_length, max_length)
    """
    
    # PERFORMANCE TESTING
    lengths = [3, 5, 7, 10, 12, 13, 15, 17, 19, 21, 23, 25, 30, 40, 50, 60, 70, 80, 90, 100]
    generate_pedidos_for_lengths(products_file, pedidos_file, lengths, 2)





if __name__ == '__main__':
    main()
