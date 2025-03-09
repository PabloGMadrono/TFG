from v3.src.files_management.file_names import products_file, product_types_file
from v3.src.files_management.json_management import load_file, save_file


def generate_product_categories(products_file, product_types_file):
    products = load_file(products_file)

    # Define category keys based on expected categories.
    categories = {
        "frozen products": [],
        "heavy products": [],
        "normal products": []
    }

    # Iterate over each gondola entry in the products file
    for gondola in products:
        for product in gondola["list_of_products"]:
            # Read the category from the product dictionary
            prod_category = product.get("category")
            prod_name = product.get("name")
            if prod_category in categories:
                categories[prod_category].append(prod_name)
            else:
                # If an unexpected category is found, you can choose to handle it as needed.
                print(f"Warning: Unexpected category '{prod_category}' found for product '{prod_name}'.")

    save_file(product_types_file, categories)
    print(f"Product categories saved to {product_types_file}")


def main():
    generate_product_categories(products_file, product_types_file)


if __name__ == '__main__':
    main()
