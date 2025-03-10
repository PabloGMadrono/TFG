import time
from v3.src.files_management.file_names import product_distances_file, optimized_route_file, pedidos_file, product_types_file
from v3.src.files_management.json_management import *
from v3.src.algoritimia.brute_force_TSP import brute_force_tsp
from v3.src.algoritimia.nearest_neighbor_TSP import forced_nearest_neighbor_tsp
from v3.src.algoritimia.simulated_annealing import simulated_annealing_tsp
from v3.src.algoritimia.DP_TSP import held_karp_tsp
from v3.src.validadores.validador_reglas_de_oro import route_respects_frozen_rule
from v3.src.algoritimia.get_distance import get_distance
from v3.src.algoritimia.genetic_algorithm_TSP import genetic_algorithm_tsp


def is_frozen(product, type_products_file):
    type_products_data = load_file(type_products_file)
    frozen_set = set(type_products_data.get("frozen products", []))
    # If product is a dictionary, extract its 'name' field.
    if isinstance(product, dict):
        product = product.get("name", product)
    return product in frozen_set





def save_route_order_to_file(order_id, route, total_distance, execution_time, output_file=optimized_route_file, mode='a'):
    if len(route) < 13:
        algorithm = "Brute Force"
    elif len(route) < 24:
        algorithm = "Dynamic Programming"
    else:
        algorithm = "Simmulated Annealing"
    result = {
        "order_id": order_id,
        "Number of products": str(len(route) - 2),
        "route": route,
        "total_distance": total_distance,
        "algorithm": algorithm,
        "Follows regla de oro" : route_respects_frozen_rule(route),
        "execution_time": execution_time

    }
    # If we want to replace_file uncomment next line
    if mode == 'r':
        save_file(output_file, result)
    else:
        add_to_file(output_file, result)



def find_best_route(order, product_distances_file=product_distances_file):
    order_id = order.get("order_id", "N/A")
    product_list = order.get("products", [])

    print(f"Optimizing route for order {order_id} with {len(product_list)} products and {len(product_list) + 2} nodes.")

    # Ensure that the special nodes are in the product list.
    if "starting_point" not in product_list:
        product_list.insert(0, "starting_point")
    if "finishing_point" not in product_list:
        product_list.append("finishing_point")

    product_distances = load_file(product_distances_file)

    # Use brute-force if the number of nodes is small (< 12)
    # Numero de productos <= 12
    if len(product_list) < 13:
        print("Using brute-force TSP solver.")
        route, total_distance = brute_force_tsp(product_list, product_distances)
    elif len(product_list) < 24:
        print("Using Dynamic programming TSP solver.")
        route, total_distance = held_karp_tsp(product_list, product_distances)
    else:
        print("Using simulated annealing TSP solver.")
        route, total_distance = simulated_annealing_tsp(product_list, product_distances)

        print("Also computing route with genetic algorithm.")
        route1, total_distance1 = genetic_algorithm_tsp(product_list, product_distances)

        if not route_respects_frozen_rule(route):
            print("Simulated annealing solution does not respect the frozen rule.")
            # Split the order into non-frozen and frozen products.
            non_frozen = []
            frozen = []
            for prod in product_list:
                if prod in ("starting_point", "finishing_point"):
                    continue
                if is_frozen(prod, product_types_file):
                    frozen.append(prod)
                else:
                    non_frozen.append(prod)
            # Create two new orders.
            non_frozen_order = {"order_id": str(order_id) + "-nonfrozen", "products": non_frozen}
            frozen_order = {"order_id": str(order_id) + "-frozen", "products": frozen}
            print("Optimizing route for non-frozen products...")
            route_non, dist_non, _ = find_best_route(non_frozen_order)
            print("Optimizing route for frozen products...")
            route_frozen, dist_frozen, _ = find_best_route(frozen_order)
            # Remove the duplicate special nodes:
            # route_non is like ["starting_point", ... , "finishing_point"]
            # route_frozen is like ["starting_point", ... , "finishing_point"]
            merged_route = route_non[:-1] + route_frozen[1:]
            # Compute the merged route's total distance.
            total_distance = 0
            for i in range(len(merged_route) - 1):
                total_distance += get_distance(product_distances, merged_route[i], merged_route[i + 1])
            route = merged_route
            print("Merged route created to respect frozen rule.")

        if total_distance < total_distance1:
            print("Simulated Annealing algorithm was better")
        else:
            print("Genetic algorithm was better")
            route = route1
            total_distance = total_distance1

        print("Route:", route)
        print("Total distance:", total_distance)
        return route, total_distance, order_id

    print("Route:", route)
    print("Total distance:", total_distance)
    #print(f"order: {order_id}, route respects regla de oro congelados:{route_respects_frozen_rule(route)}.")

    return route, total_distance, order_id


def main():


    orders = load_file(pedidos_file)

    if not orders:
        print("No orders found in the file.")
        return

    """
    # For this example, we take the first order.
    print(orders)
    order = orders[4]
    start_time = time.time()
    route, total_distance, order_id = find_best_route(order=order)
    end_time = time.time()

    execution_time = end_time - start_time

    save_route_order_to_file(order_id, route, total_distance, execution_time, output_file=optimized_route_file, mode='r')

    
    print(f"Execution time: {execution_time:.4f} seconds")

    """
    reiniciar = True
    for order in orders:
        #empty_json_file(optimized_route_file, empty_type='list')
        start_time = time.time()
        route, total_distance, order_id = find_best_route(order=order)
        end_time = time.time()
        execution_time = end_time - start_time

        if reiniciar:
            save_route_order_to_file(order_id, route, total_distance, execution_time, output_file=optimized_route_file, mode='r')
            reiniciar = False
        else:
            save_route_order_to_file(order_id, route, total_distance, execution_time, output_file=optimized_route_file)



        print(f"Execution time: {execution_time:.4f} seconds")


if __name__ == "__main__":
    main()