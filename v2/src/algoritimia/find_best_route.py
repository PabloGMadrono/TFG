import time
from v2.src.files_management.file_names import product_distances_file, optimized_route_file, pedidos_file
from v2.src.files_management.json_management import load_file, save_file
from v2.src.algoritimia.brute_force_TSP import brute_force_tsp
from v2.src.algoritimia.nearest_neighbor_TSP import forced_nearest_neighbor_tsp
from v2.src.algoritimia.DP_TSP import held_karp_tsp



def find_best_route(order, output_file, product_distances_file=product_distances_file):
    order_id = order.get("order_id", "N/A")
    product_list = order.get("products", [])

    print(f"Optimizing route for order {order_id} with {len(product_list)} products and {len(product_list) + 2} nodes.")

    # Ensure that the special nodes are in the product list.
    if "starting_point" not in product_list:
        product_list.insert(0, "starting_point")
    if "finishing_point" not in product_list:
        product_list.append("finishing_point")

    product_distances = load_file(product_distances_file)

    # Use brute-force if the number of nodes is small (< 12), else use nearest neighbor.
    # Numero de productos <= 12
    if len(product_list) < 14:
        print("Using brute-force TSP solver.")
        route, total_distance = brute_force_tsp(product_list, product_distances)
    elif len(product_list) < 25:
        print("Using Dynamic programming TSP solver.")
        route, total_distance = held_karp_tsp(product_list, product_distances)
    else:
        print("Using nearest neighbor TSP solver.")
        route, total_distance = forced_nearest_neighbor_tsp(product_list, product_distances)

    result = {
        "order_id": order_id,
        "route": route,
        "total_distance": total_distance
    }

    save_file(output_file, result)

    print("Route:", route)
    print("Total distance:", total_distance)

    return route, total_distance


def main():


    orders = load_file(pedidos_file)

    if not orders:
        print("No orders found in the file.")
        return

    # For this example, we take the first order.
    print(orders)
    order = orders[1]
    start_time = time.time()
    find_best_route(order=order, output_file=optimized_route_file)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")


if __name__ == "__main__":
    main()