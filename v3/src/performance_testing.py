# Import from algoritmia

# Import from calcular_distancias
from v3.src.calcular_distancias.calcular_distancias_gondolas import *
from v3.src.calcular_distancias.calcular_distancias_productos_from_gondolas import *

# Import from files_management
from v3.src.files_management.file_names import *

# Import from generador_datos
from v3.src.generador_datos.generar_baseline import *
from v3.src.generador_datos.generar_pedidos import *
from v3.src.generador_datos.gondola_generation import *
from v3.src.generador_datos.product_categorization import *

# Import from visualizaciones
from v3.src.visualizaciones.visualizacion_ruta_obstaculos import *

from v3.src.algoritimia.find_best_route import *

from v3.src.validadores.analizar_rutas import *

from v3.src.validadores import *
import time



def performance_testing(mapa_file, name):
    generate_gondolas(mapa_file, products_file)

    # PERFORMANCE TESTING
    lengths = [3, 5, 7, 10, 12, 13, 15, 17, 19, 21, 23, 25, 30, 40, 50, 60, 70]
    generate_pedidos_for_lengths(products_file, pedidos_file, lengths, 10)

    extract_product_categories(products_file, product_types_file)

    calcular_distancias_gondolas(mapa_file, products_file, gondolas_distances_file)
    calcular_distancias_productos(products_file, gondolas_distances_file, product_distances_file, product_types_file, regla_obj_pesados=False)

    orders = load_file(pedidos_file)

    reset = True
    start_total_time = time.time()

    output_file = f"{str(optimized_route_levels)}_{name}.json"

    for order in orders:
        start_time = time.time()
        route, total_distance, order_id = find_best_route(order=order)
        end_time = time.time()
        execution_time = end_time - start_time

        if reset:
            save_route_order_to_file(order_id, route, total_distance, execution_time, output_file=output_file, mode='r')
            reset = False
        else:
            save_route_order_to_file(order_id, route, total_distance, execution_time, output_file=output_file)
    end_total_time = time.time()

    total_time = end_total_time - start_total_time
    print(f"The total execution time was: {total_time}")

    generate_statistics(products_file, output_file, name)
    generate_visualizacion_route(output_file, products_file, mapa_file, name)



def main():
    performance_testing(map_file, "lvl1")
    performance_testing(map_file_lvl2, "lvl2")
    performance_testing(map_file_lvl3, "lvl3")

if __name__ == '__main__':
    main()