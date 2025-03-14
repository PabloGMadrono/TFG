from pathlib import Path

# Get the absolute path of the current script's directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Adjust based on project structure

# Lista de gondolas incluyendo los productos disponibles en cada gondola
products_file = BASE_DIR / "data/products.json"

# Lista de pedidos generados
pedidos_file = BASE_DIR / "data/pedidos.json"

# Mapa en formato CSV
map_file = BASE_DIR / "data/mapaTFG_lvl2.csv"

# Archivo para categorizar productos
product_types_file = BASE_DIR / "data/typeproducts.json"

# Pedido que incluye un producto de cada góndola para generar la ruta completa
baseline1_order_file = BASE_DIR / "data/baseline1.json"

# Archivo de ruta para baseline1
baseline1_route_file = BASE_DIR / "output/baseline1_route.json"

# Archivo que almacena las distancias calculadas entre cada producto
product_distances_file = BASE_DIR / "data/product_distances.json"

# Archivo que almacena las distancias calculadas entre las góndolas
gondolas_distances_file = BASE_DIR / "data/gondolas_distances.json"

# Archivo de la ruta optimizada
optimized_route_file = BASE_DIR / "output/optimized_route.json"  # Ajustar directorio si es necesario.


visualization_dir = BASE_DIR / "output/visualizations/"


statistics_dir = BASE_DIR / "output/statistics/"

"""---- Pruebas------"""

pruebas_annealing_dir = BASE_DIR / "output/pruebas_annealing/"


def main():
    print(BASE_DIR)
    print(pedidos_file)


if __name__ == "__main__":
    main()