#!/usr/bin/env python3
import json
from v3.src.files_management.json_management import load_file  # reusing our JSON load helper
from v3.src.files_management.file_names import optimized_route_file, product_types_file  # assuming these are defined


def route_respects_frozen_rule(route, product_types_file=product_types_file):
    """
    Checks if a given route respects the frozen rule.
    Once a frozen product is encountered, no non-frozen product should come later.

    Special nodes 'starting_point' and 'finishing_point' are ignored.

    Args:
        route (list): List of node names in the route.
        frozen_set (set): Set of product names that are frozen.

    Returns:
        bool: True if the route respects the rule, False otherwise.
    """
    type_products_data = load_file(product_types_file)

    # Build a set of frozen products.
    frozen_set = set(type_products_data.get("frozen products", []))

    encountered_frozen = False
    for node in route:
        # Skip special nodes.
        if node in {"starting_point", "finishing_point"}:
            continue
        # If the node is frozen, mark that we have entered the frozen segment.
        if node in frozen_set:
            encountered_frozen = True
        else:
            # If we've already encountered a frozen product and now find a non-frozen one, rule is violated.
            if encountered_frozen:
                return False
    return True


def check_orders_routes(pedidos_file):
    """
    Reads orders from a JSON file and checks each route against the frozen rule.

    The orders file should contain a list of orders, each with an "order_id" and a "route".
    The type products file is expected to have a key "frozen products" mapping to a list of frozen product names.

    Args:
        pedidos_file (str): Path to the JSON file with orders.
        product_types_file (str): Path to the JSON file with type product definitions.

    Returns:
        list: A list of dictionaries with order_id and whether the route respects the frozen rule.
    """
    # Load orders and type-products data.
    orders_data = load_file(pedidos_file)


    results = []
    for order in orders_data:
        order_id = order.get("order_id", "Unknown")
        route = order.get("route", [])
        valid = route_respects_frozen_rule(route)
        results.append({"order_id": order_id, "respects_frozen_rule": valid})
        print(f"Order {order_id} respects frozen rule: {valid}")
    return results


def main():
    # Assuming pedidos_file and product_types_file are defined in your file_names module.
    check_orders_routes(optimized_route_file)


if __name__ == '__main__':
    main()
