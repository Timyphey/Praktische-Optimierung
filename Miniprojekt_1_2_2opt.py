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



# Schreibe eine 2-opt Heuristik. Teile Deine Implementierung in drei Funktionen auf.
# 1. Implementiere die Funktion two_opt_xchg(tour, I, k), die die Reihenfolge der Städte i,..., k in tour umdreht und die neue Rundreise zurückgibt.
def two_opt_xchg(tour, i, k):
	prefix = tour[:i]
	reversed_sub_tour = tour[i:k+1][::-1]
	suffix = tour[k+1:]
	new_tour = prefix + reversed_sub_tour + suffix

	return new_tour

# 2. Implementiere danach die Funktion two_opt_step(tour), die die best-improvement Strategie realisiert. Dafür muss two_opt_step alle sinnvollen 2-opt Vertauschungen von tour durchführen und die kürzeste neue Rundreise sich merken sowie zurückgeben. Es sollte beachtet werden, dass ein 2-opt Tausch (two_opt_xchg) bei der best-improvement Strategie immer auf die original-tour angewendet wird. Zähle auch die Anzahl der ausgewerteten Rundreiselängen und lasse auch diese Größe zurückgeben.
def two_opt_step(tour, distances):
  n = len(tour)
  
  # initialize the best tour, best length and evaluations
  best_tour = tour
  best_length = measurePath(tour, distances)
  evaluations = 0

  # while loop until no further improvement
  improved = True
  while improved:
    improved = False
    
    # iterate through each pair of edges in the tour
    for i in range(1, n - 1):
      for k in range(i + 1, n):
        # apply 2-opt exchange to get a new tour and calc its length
        new_tour = two_opt_xchg(tour, i, k)
        new_length = measurePath(new_tour, distances)
        evaluations += 1
        # check if new tour is shorter than current best tour
        if new_length < best_length:
          best_length = new_length
          best_tour = new_tour
          improved = True

  return best_tour, evaluations

# 3. Implementiere einen Hill Climber, der, ausgehend von einer zufälligen Startlösung, two_opt_step(tour) solange aufruft, solange eine Verbesserung der Rundreise möglich ist. Kann die Rundreise nicht mehr verbessert werden, lasse die Länge der Rundreise, die Anzahl berechneter Rundreiselängen und die Rechenzeit ausgeben.
def hill_climber(maximalNoOfCities, distances):
  # save starting time
  start_time = time.perf_counter()
  
  # Generate a random initial tour
  start_tour = list(range(maximalNoOfCities))
  random.shuffle(start_tour)
  current_tour = start_tour
  current_length = measurePath(current_tour, distances)
  
  total_evaluations = 0
  
  # while loop until no further improvement
  improved = True
  while improved:
      improved = False
      # apply 2-opt step to get a new tour and number of evaluations
      new_tour, evaluations = two_opt_step(current_tour, distances)
      new_length = measurePath(new_tour, distances)
      total_evaluations += evaluations
      
      # check if new tour is shorter than current best tour
      if new_length < current_length:
          current_tour = new_tour
          current_length = new_length
          improved = True

  # calc runtime
  end_time = time.perf_counter()
  runtime = end_time - start_time

  return runtime, current_length, total_evaluations

########################################################

# load the distance matrix and city names
(cities, distances) = loadDistances()

# 4. Berechne für n = 5,...,16 die Rundreisen mit 2-opt.
print("starting hill climber for 2-opt for n = 5,...,16")
for n in range(5,17):
  runtime, current_length, total_evaluations = hill_climber(n, distances)
  print("{} cities\t runtime: {:.10f} s -> shortest length: {}\t Total Evaluations: {}".format(n, runtime, current_length, total_evaluations))

# 5. Da 2-opt ein nichtdeterministischer (randomisierter) Algorithmus ist, lasse ihn fünf Mal laufen und berichte die Rundreiselängen, die durchschnittliche Anzahl der Berechnungen einer Rundreiselänge und die durchschnittliche Rechenzeit. Trage die Werte in die Tabelle ein.
print("starting hill climber for 2-opt for n = 5,...,16 with averages over 5 cycles")
for n in range(5,17):
  total_runtime = 0
  total_evaluations = 0
  lengthList = []
  for i in range(5):
    runtime, current_length, evaluations = hill_climber(n, distances)
    total_runtime += runtime
    total_evaluations += evaluations
    lengthList.append(current_length)

  average_runtime = total_runtime/5
  average_evaluations = total_evaluations/5
  average_length = sum(lengthList)/5

  print("5 cycles with {} cities\t avg_runtime: {:.5f} s\t -> avg_length: {}\t lengthList: {}\t avg_Evaluations: {}".format(n, average_runtime, average_length, lengthList, average_evaluations))
  
  # 6. Für bekannte kürzeste Rundreisen: Findet 2-opt auch immer die kürzeste Rundreise? Wenn nicht, wie nahe kommt 2-opt an eine beste Lösung?
  # Bei kleinem n wird immer die kürzeste Rundreise gefunden, aber je größer n wird, desto unwahrscheinlicher wird dies. Ansonsten kommt es ziemlich nah ran.
  
  # 7. Nimmt die 2-opt Rechenzeit mit größer werdenden n zu?
  # Ja, die Rechenzeit nimmt leicht zu.
  
  
  
  