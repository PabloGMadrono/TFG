#!/usr/bin/env python3
import json
import random

def main():
    # Path to the products file produced earlier.
    products_file = "../../data/products.json"
    
    # Load products from the JSON file.
    with open(products_file, "r", encoding="utf-8") as f:
        product_data = json.load(f)
    
    # Collect all available product IDs (names) from the product data.
    # Each entry in product_data is expected to be a dict with key "list_of_products".
    available_products = []
    for entry in product_data:
        available_products.extend(entry["list_of_products"])
    
    print(f"Total available products: {len(available_products)}")
    
    # Generate 50 simulated orders.
    simulated_orders = []
    num_orders = 50
    min_length = 8
    max_length = 40
    
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
    
    # Save the simulated orders to a JSON file named pedidos.json.
    output_file = "../../data/pedidos.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(simulated_orders, f, indent=4)
    
    print(f"Simulated orders saved to {output_file}")

if __name__ == '__main__':
    main()
