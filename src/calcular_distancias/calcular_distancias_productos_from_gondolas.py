#!/usr/bin/env python3
import json
import os

def main():
    # File paths for input and output.
    products_file = 'data/products.json'
    gondola_distances_file = 'data/gondola_distances.json'
    output_file = 'data/product_distances.json'
    
    # Load the products JSON.
    try:
        with open(products_file, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        print(f"Loaded {len(products_data)} gondola entries from {products_file}.")
    except Exception as e:
        print(f"Error loading products JSON: {e}")
        return

    # Load the precomputed gondola distances.
    try:
        with open(gondola_distances_file, 'r', encoding='utf-8') as f:
            gondola_distances = json.load(f)
        print(f"Loaded gondola distances from {gondola_distances_file}.")
    except Exception as e:
        print(f"Error loading gondola distances JSON: {e}")
        return

    # Build a mapping from each product to its gondola_id.
    # Also, collect a list of all products.
    product_to_gondola = {}
    product_list = []
    for gondola in products_data:
        try:
            gid = gondola["gondola_id"]
            for product in gondola["list_of_products"]:
                product_to_gondola[product] = gid
                product_list.append(product)
        except KeyError as e:
            print(f"Missing key {e} in gondola data: {gondola}")

    print(f"Total products found: {len(product_list)}")
    
    # Compute pairwise product distances based on gondola distances.
    product_distances = {}
    n = len(product_list)
    for i in range(n):
        prod1 = product_list[i]
        product_distances[prod1] = {}
        for j in range(i, n):
            prod2 = product_list[j]
            # Distance from a product to itself is 0.
            if i == j:
                d = 0
            else:
                # Get gondola IDs for each product.
                gid1 = product_to_gondola[prod1]
                gid2 = product_to_gondola[prod2]
                if gid1 == gid2:
                    d = 0  # Same gondola => zero distance.
                else:
                    # Look up the distance between the gondolas.
                    # The keys in gondola_distances might be strings or integers.
                    # We'll attempt both ways.
                    d = None
                    # Try with string keys:
                    if str(gid1) in gondola_distances and str(gid2) in gondola_distances[str(gid1)]:
                        d = gondola_distances[str(gid1)][str(gid2)]
                    elif str(gid2) in gondola_distances and str(gid1) in gondola_distances[str(gid2)]:
                        d = gondola_distances[str(gid2)][str(gid1)]
                    # If not found, try with integer keys:
                    if d is None:
                        if gid1 in gondola_distances and gid2 in gondola_distances[gid1]:
                            d = gondola_distances[gid1][gid2]
                        elif gid2 in gondola_distances and gid1 in gondola_distances[gid2]:
                            d = gondola_distances[gid2][gid1]
                    # If still not found, default to infinity.
                    if d is None:
                        d = float('inf')
            product_distances[prod1][prod2] = d
            product_distances.setdefault(prod2, {})[prod1] = d
            #print(f"Distance between '{prod1}' and '{prod2}': {d}")

    # Save the product distances to the output JSON file.
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(product_distances, f, indent=4)
        print(f"\nPairwise product distances have been saved to {output_file}")
    except Exception as e:
        print(f"Error saving output JSON: {e}")

if __name__ == '__main__':
    main()
