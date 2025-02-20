import json
import random

# Load the existing products.json file
input_file = "../../data/products.json"
output_file = "../../data/typeproducts.json"

with open(input_file, "r", encoding="utf-8") as f:
    products = json.load(f)

# Define category keys
categories = {
    "frozen products": [],
    "heavy products": [],
    "normal products": []
}

# Flatten the product list (get all product IDs)
all_products = [prod_id for product in products for prod_id in product["list_of_products"]]

# Shuffle the product list to ensure randomness
random.shuffle(all_products)

# Distribute products among categories randomly
for product_id in all_products:
    chosen_category = random.choice(list(categories.keys()))
    categories[chosen_category].append(product_id)

# Save to a new JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(categories, f, indent=4)

print(f"Categorized JSON file '{output_file}' created successfully!")