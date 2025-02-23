import random




def genetic_algorithm_tsp(product_list, product_distances, population_size=100, generations=4000, mutation_rate=0.01):
    """
    Solve the TSP using a genetic algorithm.
    The first and last nodes in product_list are fixed (starting_point and finishing_point).
    """
    # Fix start and end
    start_node = product_list[0]
    end_node = product_list[-1]
    intermediate_nodes = product_list[1:-1]

    def route_distance(route):
        total = 0
        for i in range(len(route) - 1):
            total += product_distances[route[i]][route[i + 1]]
        return total


    # Create initial population: each individual is a route with a random permutation of intermediate_nodes.
    population = []
    for _ in range(population_size):
        perm = intermediate_nodes[:]
        random.shuffle(perm)
        individual = [start_node] + perm + [end_node]
        population.append(individual)

    def tournament_selection(pop):
        tournament_size = 5
        tournament = random.sample(pop, tournament_size)
        tournament.sort(key=lambda r: route_distance(r))
        return tournament[0]

    def order_crossover(parent1, parent2):
        # Operate on the intermediate section only.
        p1 = parent1[1:-1]
        p2 = parent2[1:-1]
        size = len(p1)
        child = [None] * size
        # Choose two random crossover points.
        i, j = sorted(random.sample(range(size), 2))
        child[i:j+1] = p1[i:j+1]
        pos = (j + 1) % size
        for k in range(size):
            candidate = p2[(j + 1 + k) % size]
            if candidate not in child:
                child[pos] = candidate
                pos = (pos + 1) % size
        return [start_node] + child + [end_node]

    def mutate(route):
        # Swap two random positions in the intermediate section.
        r = route[:]
        if len(r) <= 3:
            return r
        i, j = random.sample(range(1, len(r) - 1), 2)
        r[i], r[j] = r[j], r[i]
        return r

    best_route = None
    best_distance = float('inf')
    for gen in range(generations):
        # Elitism: always carry over the best individual.
        population.sort(key=lambda r: route_distance(r))
        if route_distance(population[0]) < best_distance:
            best_distance = route_distance(population[0])
            best_route = population[0]
        new_population = [population[0]]
        while len(new_population) < population_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = order_crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)
        population = new_population
    return best_route, best_distance