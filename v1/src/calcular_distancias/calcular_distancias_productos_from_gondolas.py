#!/usr/bin/env python3
from v1.src.files_management.file_names import products_file, gondolas_distances_file, product_distances_file
from v1.src.files_management.json_management import save_file, load_file

def calcular_distancias_productos(products_file, gondolas_distances_file, output_file):
    """Calcula la distancia entre todos los productos en base a la distancia que hay entre sus gondolas"""

    # Load the products JSON.
    products_data = load_file(products_file)

    # Load the precomputed gondola distances.
    gondola_distances = load_file(gondolas_distances_file)

    # Build a mapping from each product to its gondola_id.
    # Also, collect a list of all product identifiers.
    # For special nodes (starting_point and finishing_point), add them as product nodes.
    product_to_gondola = {}
    product_list = []
    for gondola in products_data:
        try:
            gid = gondola["gondola_id"]
            if gid == "starting_point" or gid == "finishing_point":
                # Add the special node as a product identifier.
                product_to_gondola[gid] = gid
                product_list.append(gid)
            else:
                for product in gondola["list_of_products"]:
                    product_to_gondola[product] = gid
                    product_list.append(product)
        except KeyError as e:
            print(f"Missing key {e} in gondola data: {gondola}")

    print(f"Total product nodes found: {len(product_list)}")

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
                    d = None
                    # Try with string keys:
                    if str(gid1) in gondola_distances and str(gid2) in gondola_distances[str(gid1)]:
                        d = gondola_distances[str(gid1)][str(gid2)]
                    elif str(gid2) in gondola_distances and str(gid1) in gondola_distances[str(gid2)]:
                        d = gondola_distances[str(gid2)][str(gid1)]

                    if d is None:
                        d = float('inf')
            product_distances[prod1][prod2] = d
            product_distances.setdefault(prod2, {})[prod1] = d
            # Optionally, print debug info:
            # print(f"Distance between '{prod1}' and '{prod2}': {d}")

    # Save the product distances to the output JSON file.
    #os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    save_file(output_file, product_distances)


def main():

    calcular_distancias_productos(products_file, gondolas_distances_file, output_file=product_distances_file)

if __name__ == '__main__':
    main()
