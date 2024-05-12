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



# 1. Dein Programm sollte den Parameter n haben, mit dem man angeben kann, wie viele Städte der Handlungsreisende besuchen möchte. Bei n = 3 würde der Handlungsreisende nach der kürzesten Rundreise suchen, die die Städte Kiel (1), Hamburg (2) und Schwerin (3) enthält.
def tryAllPermutations(maximalNoOfCities):
	# save starting time
  startTime = time.perf_counter()
  
  # initialize shortestTourLength and generate all permutations
  shortestTourLength = sum([sum(i) for i in distances])
  allPermutations = permutations(range(maximalNoOfCities))

  # go through all permutations
  for p in allPermutations:
    tourLength = measurePath(p, distances)

    # check if new tour is shorter than current shortest tour
    if tourLength < shortestTourLength:
      shortestTourLength = tourLength
      shortestTour = p
  
  shortestTourCities = [cities[i] for i in shortestTour]

  # calc runtime
  endTime = time.perf_counter()
  runtime = endTime - startTime
  
  # print results
  print("{} cities\t runtime: {:.5f} s\t shortest_length: {}\t tour: {}".format(maximalNoOfCities, runtime, shortestTourLength, shortestTourCities))


########################################################

# load the distance matrix and city names
(cities, distances) = loadDistances()

# 2. Messe die Längen der kürzesten Reisen und die Rechenzeiten für n = 5,6,7,8,9,10,.... Du kannst das n solange erhöhen, bis die Rechenzeit für deinen Computer zu groß wird. Trage die Werte in die unten stehende Tabelle ein (Spalten: Brute Force).
print("starting brute force for n = 5,...,11")
for i in range(5,12):
  tryAllPermutations(i)

#tryAllPermutations(12)

# 3. Extrapoliere die Rechenzeit für n = 16,15,... und trage die extrapolierte Werte auch in die Tabelle ein. Könnte Dein “Brute Force” Programm in diesem Jahr die kürzeste Rundreise durch alle Landeshauptstädte berechnen?
# n = 13 -> 1h
# n = 14 -> 14h
# n = 15 -> 9d
# n = 16 -> 140d
# Ja, es wäre möglich innerhalb dieses Jahres die kürzeste Rundreise durch alle Landeshauptstädte berechnen.