#!/usr/bin/env python3
from v3.src.files_management.file_names import (
    products_file,
    gondolas_distances_file,
    product_distances_file,
    product_types_file  # assuming you have this defined in file_names
)
from v3.src.files_management.json_management import save_file, load_file
import math

def calcular_distancias_productos(products_file, gondolas_distances_file, output_file, type_products_file, regla_obj_pesados=True):
    """
    Calcula la distancia entre todos los productos en base a la distancia entre sus góndolas,
    aplicando una penalización extra al ir de un producto congelado a uno no congelado.
    """

    # Load the products JSON.
    products_data = load_file(products_file)

    # Load the precomputed gondola distances.
    gondola_distances = load_file(gondolas_distances_file)

    # Load the type products JSON and build sets for each category.
    type_products_data = load_file(type_products_file)
    frozen_set = set(type_products_data.get("frozen products", []))
    heavy_set = set(type_products_data.get("heavy products", []))
    normal_set = set(type_products_data.get("normal products", []))

    # Build a mapping from each product to its gondola_id.
    # Also, collect a list of all product identifiers.
    # Special nodes (starting_point and finishing_point) are added as product nodes.
    product_to_gondola = {}
    product_list = []
    for gondola in products_data:
        try:
            gid = gondola["gondola_id"]
            if gid in ["starting_point", "finishing_point"]:
                product_to_gondola[gid] = gid
                product_list.append(gid)
            else:
                for product in gondola["list_of_products"]:
                    # Extract the product name from the dictionary.
                    product_name = product["name"]
                    product_to_gondola[product_name] = gid
                    product_list.append(product_name)
        except KeyError as e:
            print(f"Missing key {e} in gondola data: {gondola}")

    print(f"Total product nodes found: {len(product_list)}")

    # Define a penalty value (adjust as needed).
    PENALTY = 10000

    # Preinitialize the product_distances dictionary.
    product_distances = {prod: {} for prod in product_list}
    n = len(product_list)

    # Compute pairwise distances.
    for i in range(n):
        prod1 = product_list[i]
        for j in range(i, n):
            prod2 = product_list[j]
            # Base distance is 0 for the same product.
            if prod1 == prod2:
                base_d = 0
            else:
                # Get gondola IDs for each product.
                gid1 = product_to_gondola[prod1]
                gid2 = product_to_gondola[prod2]
                if gid1 == gid2:
                    base_d = 0  # Same gondola => zero distance.
                else:
                    base_d = None
                    if str(gid1) in gondola_distances and str(gid2) in gondola_distances[str(gid1)]:
                        base_d = gondola_distances[str(gid1)][str(gid2)]
                    elif str(gid2) in gondola_distances and str(gid1) in gondola_distances[str(gid2)]:
                        base_d = gondola_distances[str(gid2)][str(gid1)]
                    if base_d is None:
                        base_d = float('inf')

            # ENFORCE REGLA DE ORO CONGELADOS
            # From prod1 to prod2:
            d_forward = base_d
            if prod1 in frozen_set and prod2 not in frozen_set and prod2 != "finishing_point":
                d_forward += PENALTY

            # From prod2 to prod1:
            d_reverse = base_d
            if prod2 in frozen_set and prod1 not in frozen_set and prod1 != "finishing_point":
                d_reverse += PENALTY

            # ENFORCE REGLA DE ORO ART. PESADOS
            if regla_obj_pesados:
                # From prod1 to prod2:
                if prod1 in normal_set and prod2 in heavy_set and prod2 != "finishing_point":
                    d_forward += PENALTY

                # From prod2 to prod1:
                if prod2 in normal_set and prod1 in heavy_set and prod1 != "finishing_point":
                    d_reverse += PENALTY

            product_distances[prod1][prod2] = d_forward
            product_distances[prod2][prod1] = d_reverse

    # Remove the starting_point from each product's dictionary.
    for prod in product_distances:
        product_distances[prod].pop("starting_point", None)

    # Save the product distances to the output JSON file.
    save_file(output_file, product_distances)


def main():
    calcular_distancias_productos(
        products_file,
        gondolas_distances_file,
        output_file=product_distances_file,
        type_products_file=product_types_file
    )


if __name__ == '__main__':
    main()
