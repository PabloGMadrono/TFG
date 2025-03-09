import pandas as pd
import random
from v3.src.files_management.file_names import map_file, products_file
from v3.src.files_management.json_management import save_file

def generate_gondolas(map_file, products_file):
    # Load CSV file (adjust delimiter if necessary, e.g., ";")
    data = pd.read_csv(map_file, delimiter=",", dtype=int, encoding="utf-8-sig", header=None).to_numpy()

    # Define the product categories
    categories = ["frozen products", "heavy products", "normal products"]

    # Prepare the JSON structure
    product_list = []
    product_id = 1  # Start product ID for normal gondolas
    gondola_id = 0

    # Flag to track if we've found the start/finish point yet
    door_found = False

    # Iterate over the matrix to find gondolas (value=2) and special points (value=99).
    for y, row in enumerate(data):  # y is the row index
        for x, value in enumerate(row):  # x is the column index
            if value == 2:
                # Normal gondola with a list of 3 products
                entry = {
                    "gondola_id": gondola_id,
                    "x_coordinate": x,
                    "y_coordinate": y,
                    "list_of_products": [
                        {
                            "name": f"product {product_id}",
                            "category": random.choice(categories)
                        },
                        {
                            "name": f"product {product_id + 1}",
                            "category": random.choice(categories)
                        },
                        {
                            "name": f"product {product_id + 2}",
                            "category": random.choice(categories)
                        }
                    ]
                }
                product_list.append(entry)
                product_id += 3  # Increment ID for next gondola
                gondola_id += 1

            elif value == 99:
                # Special cell for start or finish
                if not door_found:
                    # First 99 => starting point
                    start_entry = {
                        "gondola_id": "starting_point",
                        "x_coordinate": x,
                        "y_coordinate": y,
                        "list_of_products": []
                    }
                    product_list.append(start_entry)
                    door_found = True

                    # Second 99 => finishing point
                    finish_entry = {
                        "gondola_id": "finishing_point",
                        "x_coordinate": x,
                        "y_coordinate": y,
                        "list_of_products": []
                    }
                    product_list.append(finish_entry)
                else:
                    # Warn if additional 99 values are found
                    print(f"Warning: Additional cell with value 99 found at (row={y}, col={x}) beyond start/finish.")

    save_file(products_file, product_list)

    print(f"JSON file '{products_file}' created successfully with {len(product_list)} entries.")
    print(f"Total gondolas (value=2) found: {gondola_id}")
    if door_found:
        print("Starting point added.")
        print("Finishing point added.")

def main():
    generate_gondolas(map_file, products_file)

if __name__ == '__main__':
    main()
