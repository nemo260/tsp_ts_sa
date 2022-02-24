import random
from tkinter import *
import time
import math

def generate_places(number, places):
    for i in range(number):
        new = []
        x = random.randrange(1, 201)
        y = random.randrange(1, 201)
        new.append(x)
        new.append(y)
        places.append(new)


def create_matrix_of_distances(places, matrix):
    for i in places:
        new = []
        for j in places:
            if i == j:
                distance = 0
            else:
                distance = ((j[0] - i[0]) ** 2 + (j[1] - i[1]) ** 2) ** 0.5
            new.append(distance)
        matrix.append(new)


def randomSolution(matrix_of_distances):
    cities = list(range(len(matrix_of_distances)))
    solution = []

    for i in range(len(matrix_of_distances)):
        randomPlace = cities[random.randint(0, len(cities) - 1)]
        solution.append(randomPlace)
        cities.remove(randomPlace)

    return solution


def routeLength(mod, currentSolution):
    routeLength = 0

    for i in range(len(currentSolution)):
        jedna = currentSolution[i - 1]
        dva = currentSolution[i]
        routeLength += mod[jedna][dva]

    return routeLength


def getMixedSolutions(currentSolution):
    next_solutions = []
    for i in range(number_of_places * 4):
        one = random.randrange(0, len(currentSolution))
        two = random.randrange(0, len(currentSolution))
        mixed = currentSolution.copy()
        mixed[one] = currentSolution[two]
        mixed[two] = currentSolution[one]
        if mixed not in next_solutions:
            next_solutions.append(mixed)
    return next_solutions


def tabu_search(matrix_of_distances, tabu_list, currentSolution):
    bestSolution = currentSolution
    d = 0

    while d != 10000:
        d += 1

        next_solutions = getMixedSolutions(currentSolution)

        next_solutions_distances = []
        for i in range(len(next_solutions)):
            next_solutions_distances.append(routeLength(matrix_of_distances, next_solutions[i]))

        new = []
        while next_solutions_distances:
            new.append(next_solutions[next_solutions_distances.index(min(next_solutions_distances))])
            del next_solutions[next_solutions_distances.index(min(next_solutions_distances))]
            del next_solutions_distances[next_solutions_distances.index(min(next_solutions_distances))]

        if tabu_list:
            for i in new:
                if i not in tabu_list:
                    currentSolution = i
                    tabu_list.append(i)
                    if len(tabu_list) > 50:
                        tabu_list.remove(tabu_list[0])
                    break
        else:
            tabu_list.append(new[0])
            currentSolution = new[0]

        if routeLength(matrix_of_distances, currentSolution) < routeLength(matrix_of_distances, bestSolution):
            bestSolution = currentSolution

    return bestSolution


def simulated_annealing(matrix_of_distances, currentSolution):
    temp = 40
    bestSolution = currentSolution
    count = 0
    while temp > 0:
        for k in range(10000):

            next_solutions = getMixedSolutions(currentSolution)

            randomSol = random.choice(next_solutions)

            if routeLength(matrix_of_distances, randomSol) <= routeLength(matrix_of_distances, currentSolution):
                currentSolution = randomSol
            else:
                delta = routeLength(matrix_of_distances, currentSolution) - routeLength(matrix_of_distances, randomSol)
                u = random.uniform(0, 1)

                if u < math.e**(delta/temp):
                    currentSolution = randomSol
                    count += 1

            if routeLength(matrix_of_distances, currentSolution) < routeLength(matrix_of_distances, bestSolution):
                bestSolution = currentSolution
        temp -= 3
    #print("Kolkokrat vzalo riešenie, ktore je horšie: " + str(count))
    return bestSolution


number_of_places = 20
places = []
matrix_of_distances = []
tabu_list = []
x = 0

root = Tk()
canvas = Canvas(root, bg='white', width=900, height=500)
canvas.pack(fill=BOTH, expand=1)

#generate_places(number_of_places, places)
#places = [[27, 128], [14, 196], [23, 191], [80, 128], [91, 168], [133, 87], [27, 174], [24, 91], [87, 153], [161, 39], [130, 28], [6, 74], [108, 118], [27, 157], [155, 198], [157, 163], [143, 63], [16, 139], [55, 156], [14, 136], [71, 96], [140, 7], [123, 107], [115, 107], [13, 26], [69, 100], [98, 69], [144, 6], [91, 150], [67, 110], [168, 173], [137, 1], [180, 166], [52, 29], [42, 99], [110, 160], [110, 122], [118, 61], [44, 143], [147, 78]]
places = [[27, 128], [14, 196], [23, 191], [80, 128], [91, 168], [133, 87], [27, 174], [24, 91], [87, 153], [161, 39], [130, 28], [6, 74], [108, 118], [27, 157], [155, 198], [157, 163], [143, 63], [16, 139], [55, 156], [14, 136]]
#places = [[162, 82],[18, 135],[14, 68],[139, 88],[82, 16],[199, 146],[145, 69],[27, 118],[200, 39],[156, 50],[138, 96],[14, 30],[88, 42],[1, 40],[142, 63],[111, 115],[65, 87],[76, 53],[24, 106],[193, 180]]
create_matrix_of_distances(places, matrix_of_distances)

currentSolution = randomSolution(matrix_of_distances)

start_tabu = time.time()
tabu_solution = tabu_search(matrix_of_distances, tabu_list, currentSolution)
end_tabu = time.time()

start_sa = time.time()
annealing_solution = simulated_annealing(matrix_of_distances, currentSolution)
end_sa = time.time()


print(tabu_solution)
print("Route cost - tabu search: " + str(routeLength(matrix_of_distances, tabu_solution)))
print(annealing_solution)
print("Route cost - simulated annealing: " + str(routeLength(matrix_of_distances, annealing_solution)))

print("Time of tabu search: " + str(end_tabu - start_tabu) + "s")
print("Time of simulated annealing " + str(end_sa - start_sa) + "s")

#print(places)

canvas.create_line(450, 0, 450, 500, width="5")
canvas.create_text(220, 450, text="Tabu search", font="15")
canvas.create_text(680, 450, text="Simulated annealing", font="15")

for i in range(len(places)):
    canvas.create_oval(places[i][0] * 2, places[i][1] * 2, (places[i][0] + 7) * 2, (places[i][1] + 6) * 2,
                       fill='black')
for i in range(len(places)):
    param = tabu_solution[i]
    param2 = tabu_solution[i - 1]
    x = places[param]
    y = places[param2]
    canvas.create_line(x[0] * 2 + 3, x[1] * 2 + 3, y[0] * 2 + 3, y[1] * 2 + 3)

for i in range(len(places)):
    canvas.create_oval((places[i][0] * 2) + 450, (places[i][1] * 2), ((places[i][0] + 7) * 2) + 450,
                       ((places[i][1] + 6) * 2),
                       fill='black')

for i in range(len(places)):
    param = annealing_solution[i]
    param2 = annealing_solution[i - 1]
    x = places[param]
    y = places[param2]
    canvas.create_line((x[0] * 2 + 3) + 450, (x[1] * 2 + 3), (y[0] * 2 + 3) + 450, (y[1] * 2 + 3))


root.mainloop()
# print(places)
# print(matrix_of_distances)
# print(randomSolution(matrix_of_distances))
