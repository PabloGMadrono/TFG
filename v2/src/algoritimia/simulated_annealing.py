from v2.src.algoritimia.get_distance import get_distance
import random
import math

#For testing purposes
from pathlib import Path
import time
from v2.src.files_management.file_names import product_distances_file, pedidos_file, pruebas_annealing_dir
from v2.src.files_management.json_management import *

def total_route_distance(route, distances):
    """
    Computes the total distance for a given route (a list of node names)
    by summing the distances between consecutive nodes.
    """
    total = 0
    for i in range(len(route) - 1):
        total += get_distance(distances, route[i], route[i + 1])
    return total


def simulated_annealing_tsp(product_list, distances, init_temp=1000, cooling_rate=0.99999, stopping_temp=1e-3,
                            max_iter=1250000):
    """
    Solves the TSP using simulated annealing.

    Parameters:
      - product_list: A list of node names, where the first element is the starting point
                      ("starting_point") and the last element is the finishing point ("finishing_point").
      - distances: A nested dictionary with the distances between nodes.
      - init_temp: Initial temperature for the annealing process.
      - cooling_rate: Factor by which the temperature is reduced each iteration.
      - stopping_temp: Temperature at which to stop the algorithm.
      - max_iter: Maximum number of iterations.

    Returns:
      A tuple (best_route, best_cost) representing the best found route and its total distance.
    """
    # Start with an initial route. Here, we simply use the current order.
    current_route = product_list[:]
    current_cost = total_route_distance(current_route, distances)
    best_route = current_route[:]
    best_cost = current_cost
    T = init_temp
    iteration = 0

    while T > stopping_temp and iteration < max_iter:
        # Generate a new route by swapping two random middle nodes (keeping start and finish fixed)
        new_route = current_route[:]
        # Choose two indices from the middle nodes (i.e., indices 1 to len(route)-2)
        i = random.randint(1, len(new_route) - 2)
        j = random.randint(1, len(new_route) - 2)
        if i != j:
            new_route[i], new_route[j] = new_route[j], new_route[i]

        new_cost = total_route_distance(new_route, distances)
        delta = new_cost - current_cost

        # If the new route is better, or if it is worse but accepted with probability exp(-delta/T)
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_route = new_route
            current_cost = new_cost
            if current_cost < best_cost:
                best_route = current_route[:]
                best_cost = current_cost

        T *= cooling_rate
        iteration += 1

    return best_route, best_cost




def main():
    """For testing and parameter optimization."""
    """
    orders = load_file(pedidos_file)

    if not orders:
        print("No orders found in the file.")
        return

    # For this example, we take the first order.
    print(orders)
    order = orders[10]

    order_id = order.get("order_id", "N/A")
    product_list = order.get("products", [])

    print(f"Optimizing route for order {order_id} with {len(product_list)} products and {len(product_list) + 2} nodes.")

    # Ensure that the special nodes are in the product list.
    if "starting_point" not in product_list:
        product_list.insert(0, "starting_point")
    if "finishing_point" not in product_list:
        product_list.append("finishing_point")
    product_distances = load_file(product_distances_file)

    initial_temp = 1000
    cooling_rate = 0.999
    max_iter = 10000

    for i in range(10):
        print(
            f"Iteration {i + 1}: Using simulated annealing TSP solver with cooling_rate={cooling_rate} and max_iter={max_iter}")

        start_time = time.time()
        route, total_distance = simulated_annealing_tsp(
            product_list,
            product_distances,
            init_temp=initial_temp,
            cooling_rate=cooling_rate,
            max_iter=max_iter
        )
        end_time = time.time()

        result = {
            "order_id": order_id,
            "route": route,
            "total_distance": total_distance,
            "cooling_rate": cooling_rate,
            "max_iter": max_iter,
            "execution_time": end_time - start_time
        }

        # Ensure the path is correctly formatted
        filename = Path(pruebas_annealing_dir) / f"pruebas_annealing_{i}.json"
        save_file(filename, result)

        print("Route:", route)
        print("Total distance:", total_distance)
        print(f"Execution time: {end_time - start_time:.4f} seconds\n")

        # Update parameters for the next iteration
        if i%2==0:
            max_iter *= 5  # Increase max_iter by 5
        else:
            cooling_rate = float(f"{cooling_rate}9")  # Add an extra '9' to the cooling rate

        """
if __name__ == "__main__":
    main()