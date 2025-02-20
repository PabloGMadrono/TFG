#!/usr/bin/env python3
import json
import os

def load_json(file_path):
    """Carga y retorna el contenido de un archivo JSON."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_distance(distances, a, b):
    """
    Devuelve la distancia entre los productos 'a' y 'b' utilizando el diccionario 'distances'.
    Revisa ambas direcciones y, si no se encuentra, retorna float('inf').
    """
    if a in distances and b in distances[a]:
        return distances[a][b]
    elif b in distances and a in distances[b]:
        return distances[b][a]
    else:
        return float('inf')

def nearest_neighbor_tsp(product_list, distances):
    """
    Resuelve el TSP de forma heurística (vecino más cercano) utilizando la función get_distance.
    
    Parámetros:
      product_list: Lista de productos a visitar.
      distances: Diccionario anidado con distancias entre productos.
      
    Retorna:
      Una tupla (ruta, distancia_total), donde:
        - ruta: Lista ordenada de productos en el orden de visita.
        - distancia_total: Suma de las distancias a lo largo de la ruta.
    """
    if not product_list:
        return [], 0

    start = product_list[0]
    route = [start]
    unvisited = set(product_list[1:])
    total_distance = 0
    current = start

    while unvisited:
        # Selecciona el vecino no visitado más cercano usando get_distance.
        next_product = min(unvisited, key=lambda x: get_distance(distances, current, x))
        d = get_distance(distances, current, next_product)
        total_distance += d
        route.append(next_product)
        unvisited.remove(next_product)
        current = next_product

    # Opcional: sumar la distancia de regreso al inicio para un circuito cerrado.
    # total_distance += get_distance(distances, current, start)
    return route, total_distance

def main():
    orders_file = "data/pedidos.json"
    product_distances_file = "data/product_distances.json"
    output_file = "output/optimized_route.json"  # O puedes especificar un directorio, por ejemplo: "output/optimized_route.json"

    try:
        orders = load_json(orders_file)
    except Exception as e:
        print(f"Error al cargar {orders_file}: {e}")
        return

    if not orders:
        print("No se encontró ningún pedido en el archivo.")
        return

    # Para este ejemplo, tomamos el primer pedido.
    order = orders[0]
    order_id = order.get("order_id", "N/A")
    product_list = order.get("products", [])

    print(f"Optimizando ruta para el pedido {order_id} con {len(product_list)} productos.")

    try:
        product_distances = load_json(product_distances_file)
    except Exception as e:
        print(f"Error al cargar {product_distances_file}: {e}")
        return

    route, total_distance = nearest_neighbor_tsp(product_list, product_distances)

    result = {
        "order_id": order_id,
        "route": route,
        "total_distance": total_distance
    }

    # Solo creamos el directorio si se especifica uno.
    directory = os.path.dirname(output_file)
    if directory:
        os.makedirs(directory, exist_ok=True)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)
        print(f"\nRuta optimizada guardada en {output_file}")
    except Exception as e:
        print(f"Error al guardar {output_file}: {e}")

    print("Ruta:", route)
    print("Distancia total:", total_distance)

if __name__ == '__main__':
    main()
