# Import from algoritmia

# Import from calcular_distancias
from v2.src.calcular_distancias.calcular_distancias_gondolas import *
from v2.src.calcular_distancias.calcular_distancias_productos_from_gondolas import *

# Import from files_management
from v2.src.files_management.file_names import *

# Import from generador_datos
from v2.src.generador_datos.generar_baseline import *
from v2.src.generador_datos.generar_pedidos import *
from v2.src.generador_datos.gondola_generation import *
from v2.src.generador_datos.product_categorization import *

# Import from visualizaciones
from v2.src.visualizaciones.visualizacion_ruta_obstaculos import *

from v2.src.algoritimia.find_best_route import find_best_route



def main():
    generate_gondolas(map_file, products_file)
    generarate_pedidos(products_file, pedidos_file, 50, 8, 40)
    generate_product_categories(products_file, product_types_file)

    calcular_distancias_gondolas(map_file, products_file, gondolas_distances_file)
    calcular_distancias_productos(products_file, gondolas_distances_file, product_distances_file)

    orders = load_file(pedidos_file)

    if not orders:
        print("No orders found in the file.")
        return

    # For this example, we take the first order.
    print(orders)
    order = orders[0]

    find_best_route(order=order, output_file=optimized_route_file)
    generate_visualizacion_route(optimized_route_file, products_file)

    generate_baseline_1_order(products_file, baseline1_order_file)
    generate_baseline1_route(baseline1_order_file, baseline1_route_file)
    generate_visualizacion_route(baseline1_route_file, products_file)



if __name__ == '__main__':
    main()