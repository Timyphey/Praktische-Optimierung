from itertools import permutations
from random import shuffle
import random
import math
import time

# load the distnace matrix from file
def loadDistances():
	distancesFile = open("citiesAndDistances.txt")
	cities = distancesFile.readline().split()
	del cities[16:]
	numCities = len(cities)
	
	# create an empty 2-dimensional matrix
	cityDistances = [[0.0] * numCities for i in range(numCities)]
	
	# for all cities:
	for i in range(numCities):
		distances = distancesFile.readline().split()
		del distances[0]
		del distances[16:]
		for j in range(len(distances)):
			cityDistances[i][j] = int(distances[j])
	return (cities,cityDistances)

def measurePath(p, distances):
	length = 0
	for i in range(len(p)):
		length += distances[p[i-1]][p[i]]
	return length


# 1. Implementiere den SA Algorithmus.
# 2. Der Perturbationsoperator (OP) soll als ein Kombinationsoperator implementiert werden, der bei jedem Aufruf zufällig eine der folgenden Operationen durchführt 
# • ein Schritt des Algorithmus node exchange, 
# • ein Schritt des Algoirthmus node insertion oder 
# • ein Schritt des Algorithmus two_opt_xchg(tour, i, k).
# 3. Stelle einige Experimente mit verschiedenen Abkühlschemas und deren Parametern an und wähle die beste Kombination.

def node_exchange(tour, i, k):
    new_tour = tour[:]
    new_tour[i], new_tour[k] = new_tour[k], new_tour[i]
    return new_tour
  
def node_insertion(tour, i, k):
    new_tour = tour[:]
    city = new_tour.pop(k)
    new_tour.insert(i, city)

    return new_tour
  
def two_opt_xchg(tour, i, k):
	prefix = tour[:i]
	reversed_sub_tour = tour[i:k+1][::-1]
	suffix = tour[k+1:]
	new_tour = prefix + reversed_sub_tour + suffix

	return new_tour
  
def cool(temperature, cooling_rate):
    return temperature * cooling_rate
  
def sa_algorithm(maximalNoOfCities, distances, initial_temperature, cooling_rate, max_iterations):
    start_time = time.perf_counter()
    
    # init random tour
    start_tour = list(range(maximalNoOfCities))
    random.shuffle(start_tour)
    current_tour = start_tour
    current_length = measurePath(current_tour, distances)

    best_tour = current_tour[:]
    best_length = current_length

    # init temperature and counter variables
    temperature = initial_temperature
    temp_change_iterations = maximalNoOfCities*(maximalNoOfCities - 1) * ((maximalNoOfCities-2)*(maximalNoOfCities-3)/2)
    iteration = 0
    n_wo_improvment = 0
    accepted_worse_solutions = 0

    # while loop until no improvement is made for 5 temp steps or max iterations reached
    while iteration < max_iterations and n_wo_improvment < 5:
        iteration += 1
        
        # randomly select two cities and perturbation operation
        i, k = random.sample(range(maximalNoOfCities), 2)
        perturbation_op = random.choice([node_exchange, node_insertion, two_opt_xchg])
        
        new_tour = perturbation_op(current_tour, i, k)
        new_length = measurePath(new_tour, distances)

        # accept new tour if it's shorter or based on a probability if its worse
        if new_length <= current_length:
            current_tour = new_tour
            current_length = new_length
        elif (random.random() < math.exp(-(new_length - current_length) / temperature)):
            current_tour = new_tour
            current_length = new_length
            accepted_worse_solutions += 1

        # update best tour if a shorter tour is found
        if new_length < best_length:
            best_tour = new_tour
            best_length = new_length
            n_wo_improvment = 0

        # cool down temperature
        if iteration % temp_change_iterations == 0:
            temperature = cool(temperature, cooling_rate)
            n_wo_improvment += 1
        
        # break loop if acceptance rate dips under 2%
        if accepted_worse_solutions / iteration < 0.02 and accepted_worse_solutions > 0:
            break
        
    # calc runtime
    end_time = time.perf_counter()
    runtime = end_time - start_time
    
    return runtime, best_length, iteration

########################################################

# load the distance matrix and city names
(cities, distances) = loadDistances()

# 4. Lasse SA fünf Mal laufen und berichte die Rundreiselängen, die durchschnittliche Anzahl der Berechnungen einer Rundreiselänge und die durchschnittliche Rechenzeit. Trage die Werte in die Tabelle ein.
print("starting Simulated Annealing for n = 5,...,16 with averages over 5 cycles")
for n in range(5,17):
  total_runtime = 0
  total_iterations = 0
  lengthList = []
  for i in range(5):
    runtime, best_length, iterations = sa_algorithm(n, distances, 100, 0.95, 50000)
    total_runtime += runtime
    total_iterations += iterations
    lengthList.append(best_length)

  average_runtime = total_runtime/5
  average_iterations = total_iterations/5
  average_length = sum(lengthList)/5

  print("5 cycles with {} cities\t avg_runtime: {:.5f} s\t -> avg_length: {}\t lengthList: {}\t avg_iterations: {}".format(n, average_runtime, average_length, lengthList, average_iterations))
  
  
  # 5. Für bekannte kürzeste Rundreisen: Findet SA auch immer die kürzeste Rundreise? Wenn nicht, wie nahe kommt SA an eine beste Lösung?
  # SA findet bei größerem n fast nie die kürzeste Rundreise und ist meist sogar ziemlich weit davon entfernt.
  
  # 6. Nimmt die Rechenzeit von SA mit größer werdenden n zu?
  # Ja
  
  # 7. Ist Deine SA Implementierung schneller als 2-opt?
  # Nein
  
  # 8. Erzeugt Dein SA bessere Lösungen als 2-opt?
  # Nein