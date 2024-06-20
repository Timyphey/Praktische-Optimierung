from city import distance
import time
import random

def calc_tour_length(tsp, tour):
    cities = tsp["CITIES"]
    length = 0
    for i in range(tsp["DIMENSION"]):
        length += distance(cities[tour[i - 1]], cities[tour[i]])
    return length

def node_xchg_step(tour):
    i = random.randint(0, len(tour) - 1)
    k = random.randint(0, len(tour) - 1)
    tour[i], tour[k] = tour[k], tour[i]
    return tour

# implementation of a hill climber
def HC_tour(tsp, max_iterations):
    start_time = time.time()
    tour = [i for i in range(tsp["DIMENSION"])]

    random.shuffle(tour)
    tour_len = calc_tour_length(tsp, tour)
    visited_tours = 1

    # best solution found so far
    best_tour = tour
    best_tour_len = tour_len

    # iterate max_iterations times
    while visited_tours < max_iterations:
        # derive a new tour
        new_tour = node_xchg_step(list(best_tour))
        new_tour_len = calc_tour_length(tsp, new_tour)
        visited_tours += 1

        # found a better one?
        if new_tour_len < best_tour_len:
            print('improved from', best_tour_len, 'to', new_tour_len, 'by', best_tour_len-new_tour_len, 'visited tours', visited_tours)
            best_tour = new_tour
            best_tour_len = new_tour_len

    time_consumed = time.time()-start_time
    print('time consumed', time_consumed, 'tours visited', visited_tours, 'number of tours per second', visited_tours/time_consumed)
    return (best_tour_len)

def calc_HC_tour(tsp):
    return HC_tour(tsp, 100000)


############## implementation of an Evolutionary Algorithm

# Functions
def initialize_population(tsp, population_size):
    population = []
    for _ in range(population_size):
        tour = list(range(tsp["DIMENSION"]))
        random.shuffle(tour)
        population.append(tour)
    return population

def evaluate_population(tsp, population):
    return [calc_tour_length(tsp, tour) for tour in population]


# Selection of Parents: tournament with 4 contenders
def select_parents(population, fitness, tournament_size=4):
    """Select parents using tournament selection."""
    def tournament_selection():
        contenders = random.sample(range(len(population)), tournament_size)
        best = min(contenders, key=lambda idx: fitness[idx])
        return population[best]
    
    parent1 = tournament_selection()
    parent2 = tournament_selection()
    return parent1, parent2


# Crossover functions

def two_point_crossover(parent1, parent2):
    """two-point crossover"""
    size = len(parent1)
    crossover_point1, crossover_point2 = sorted(random.sample(range(1, size - 1), 2))
    offspring = [None] * size

    offspring[crossover_point1:crossover_point2] = parent1[crossover_point1:crossover_point2]

    # Fill remaining slots with elements from parent2 considering order
    for i in range(0, size):
        if offspring[i] is None:
            for j in range(0, size):
                if parent2[j] not in offspring:
                    offspring[i] = parent2[j]
                    break
      
    return offspring

def partially_mapped_crossover(parent1, parent2):
    """Partially Mapped Crossover (PMX)"""
    size = len(parent1)
    crossover_point1, crossover_point2 = sorted(random.sample(range(1, size - 1), 2))
    offspring = [None] * size

    offspring[crossover_point1:crossover_point2] = parent1[crossover_point1:crossover_point2]

    mapping = {parent1[i]: parent2[i] for i in range(crossover_point1, crossover_point2)}

    # Function to resolve conflicts using the mapping
    def resolve_conflict(gene, mapping):
        while gene in mapping:
            gene = mapping[gene]
        return gene

    # Fill remaining slots considering order and resolving conflicts
    for i in range(size):
        if offspring[i] is None:
            if i < crossover_point1 or i >= crossover_point2:
                gene = parent2[i]
                offspring[i] = resolve_conflict(gene, mapping)
    
    return offspring

# Mutation functions
def mutate_swap(tour, mutation_rate):
    """Mutate the tour by swapping two cities with a certain probability."""
    for i in range(len(tour)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(tour) - 1)
            tour[i], tour[j] = tour[j], tour[i]
        
def mutate_reverse_sequence(tour, mutation_rate):
    """Mutate the tour by reversing a subsequence with a certain probability."""
    if random.random() < mutation_rate:
        start, end = sorted(random.sample(range(len(tour)), 2))
        tour[start:end] = reversed(tour[start:end])
        
def mutate_displacement(tour, mutation_rate):
    """Mutate the tour by displacing a subsequence to a new position."""
    if random.random() < mutation_rate:
        size = len(tour)
        start, end = sorted(random.sample(range(size), 2))
        subsequence = tour[start:end]
        remaining_tour = tour[:start] + tour[end:]
        insert_position = random.randint(0, len(remaining_tour))
        tour[:] = remaining_tour[:insert_position] + subsequence + remaining_tour[insert_position:]



##### EA
def EA_tour(tsp, population_size, max_generations):
    start_time = time.time()
    ###### define mutation and crossover operations
    #mutate_reverse_sequence, mutate_displacement, mutate_swap
    mutate_op = mutate_reverse_sequence
    #two_point_crossover, partially_mapped_crossover
    crossover_op = partially_mapped_crossover
    crossover_ops = [two_point_crossover, partially_mapped_crossover]

    # Init
    population = initialize_population(tsp, population_size)
    best_tour = None
    best_tour_len = float('inf')


    for generation in range(max_generations):
        # Evaluate population
        fitness = evaluate_population(tsp, population)
        
        # Find the best tour in the current population
        min_fitness_idx = fitness.index(min(fitness))
        if fitness[min_fitness_idx] < best_tour_len:
            best_tour_len = fitness[min_fitness_idx]
            best_tour = population[min_fitness_idx]
            #print(best_tour_len, len(best_tour), len(set(best_tour)), generation)

        # Generate new population
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, fitness)
            child = crossover_op(parent1, parent2)
            mutate_op(child, mutation_rate=0.15)
            new_population.append(child)
        
        population = new_population

    time_consumed = time.time() - start_time
    print('Time consumed:', time_consumed)
    return (best_tour_len)


def calc_EA_tour(tsp):
    return EA_tour(tsp, 20, 5000)

def calc_EA_tour_txt(tsp):
    file = open("bestresults.txt", "w")
    runs = 30
    tour_len_sum = 0
    for i in range(runs):
        best_tour_len = calc_EA_tour(tsp)
        print("EA LENGTH RUN",i+1,":        {}".format(best_tour_len))
        file.write(str(best_tour_len))
        file.write("\n")
        tour_len_sum += best_tour_len
    avg_tour_len = round(tour_len_sum/runs, 2)
    return avg_tour_len
