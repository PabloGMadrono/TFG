import numpy as np
import json
import pandas as pd

# Load CSV file and handle potential encoding issues
file_path = "data/mapaTFG.csv"  # Replace with your actual file path
data = pd.read_csv(file_path, delimiter=";", dtype=int, encoding="utf-8-sig").to_numpy()

# Prepare the JSON structure
product_list = []
product_id = 1  # Start product ID

# Iterate over the matrix to find product locations (value = 2)
for y, row in enumerate(data):  # y is the row index
    for x, value in enumerate(row):  # x is the column index
        if value == 2:
            entry = {
                "x_coordinate": x,
                "y_coordinate": y,
                "list_of_products": ["product " + str(product_id), "product " + str(product_id + 1), "product " + str(product_id + 2)]
            }
            product_list.append(entry)
            product_id += 3  # Increment ID for next entry

# Save data to a JSON file
output_file = "data/products.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(product_list, f, indent=4)

print(f"JSON file '{output_file}' created successfully with {len(product_list)} entries and {len(product_list)*3} products.")
