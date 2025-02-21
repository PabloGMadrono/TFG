import random
from v2.src.files_management.file_names import products_file, product_types_file
from v2.src.files_management.json_management import load_file, save_file


def generate_product_categories(products_file, product_types_file):

    products = load_file(products_file)
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

    save_file(product_types_file, categories)



def main():
    generate_product_categories(products_file, product_types_file)



if __name__ == '__main__':
    main()