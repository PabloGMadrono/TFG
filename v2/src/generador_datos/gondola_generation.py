import pandas as pd
from v2.src.files_management.file_names import map_file, products_file
from v2.src.files_management.json_management import save_file

def generate_gondolas(map_file, products_file):
    # Load CSV file (adjust delimiter if necessary, e.g., ";")
    data = pd.read_csv(map_file, delimiter=",", dtype=int, encoding="utf-8-sig", header=None).to_numpy()

    # Prepare the JSON structure
    product_list = []
    product_id = 1  # Start product ID for normal gondolas
    gondola_id = 0

    # Flags to track if we've found start/finish points yet
    door_found = False

    # Iterate over the matrix to find gondolas (value=2) and special points (value=99).
    for y, row in enumerate(data):  # y is the row index
        for x, value in enumerate(row):  # x is the column index
            if value == 2:
                # Normal gondola
                entry = {
                    "gondola_id": gondola_id,
                    "x_coordinate": x,
                    "y_coordinate": y,
                    "list_of_products": [
                        f"product {product_id}",
                        f"product {product_id + 1}",
                        f"product {product_id + 2}"
                    ]
                }
                product_list.append(entry)
                product_id += 3  # Increment ID for next gondola
                gondola_id += 1

            elif value == 99:
                # Initial and final point is the same
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
                    # If there's a third (or more) 99, we warn but ignore it or handle as you prefer
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
