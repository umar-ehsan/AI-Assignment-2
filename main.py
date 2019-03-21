from Tkinter import *
import math
import random
from collections import OrderedDict

# canvas dimensions 
canvas_width = 210
canvas_height = 210

# drawing class for tkinter gui
class tsp_ui(Frame):
    def __init__(self, master):
        self.canvas = Canvas(master, width = canvas_width, height = canvas_height)
        self.canvas.pack(expand = YES, fill = BOTH)

    def draw_dots(self, dot):
        self.canvas.create_oval(dot[0] - 3, dot[1] - 3, dot[0] + 3, dot[1] + 3, fill = "red")
        self.canvas.pack(expand = YES, fill = BOTH)
    
    def draw_lines(self, population, coords):
        for index in range(0, len(population) - 1):
            self.canvas.create_line(coords[population[index]][0], coords[population[index]][1], coords[population[index + 1]][0], coords[population[index + 1]][1])
        self.canvas.create_line(coords[population[len(population) - 1]][0], coords[population[len(population) - 1]][1], coords[population[0]][0], coords[population[0]][1])
        self.canvas.pack(expand = YES, fill = BOTH)

# mutate function. Swaps the city in a tour if the current random number is less than mutation rate
def mutate(tour):
    mutation = 0.025
    for index in range(0, len(tour)):
        if (random.random() < mutation):
            new_val = (int)(random.random() * len(tour))
            p_1 = tour[index]
            p_2 = tour[new_val]
            tour[index] = p_2
            tour[new_val] = p_1
    return tour

# gets euclidean distance
def distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0]) * (coord2[0] - coord1[0]) + (coord2[1] - coord1[1]) * (coord2[1] - coord1[1]))

# returns fitness of a given tour
def get_fitness(pop, edges):
    distance = 0
    for index in range(0, len(pop) - 1):
        distance += edges[pop[index]][pop[index + 1]]
    return (float)(1 / distance)

# ranks the population by its fitness value
def rank_population(pop, edges):
    fitness_array = {}
    for index in range(len(pop)):
        fitness_array[index] = get_fitness(pop[index], edges)
    return sorted(fitness_array.items(), key = lambda x: x[1], reverse = True)

# mates two individuals and returns the mutated offspring (if mutation occured)
def get_offspring(mate1, mate2):

    second_cut = len(mate1) - 4
    first_cut = second_cut - 4
    offspring = []
    for i in range(0, len(mate1)):
        offspring.append(-1)
    for i in range(first_cut , second_cut):
        offspring[i] = mate1[i]
    start = second_cut
    curr_index = start
    counter = 0
    while (counter < len(mate1)):
        matched = False
        for i in range(0, len(offspring)):
            if (mate2[start] == offspring[i]):
                matched = True
        if (matched == False and offspring[curr_index] == -1):
            offspring[curr_index] = mate2[start]
            curr_index += 1
            if (curr_index == len(mate2)):
                curr_index = 0
        
        start += 1
        if (start == len(mate2)):
            start = 0
        counter += 1

    offspring = mutate(offspring)
    return offspring

# main program
def main():
    root = Tk()
    root.title("Travelling Salesman Problem")
    tsp_window = tsp_ui(root)
    edges = []
    population = []
    new_pop = []
    generation = 1
    population_size = 500

    # problem definition
    coords = [(20, 20), (20, 40), (60, 20), (100, 40), (60, 80), (40, 120), (20, 160), (60, 200), (100, 120), (100, 160), (80, 180), (140, 180), (180, 200), (200, 160), (180, 100), (120, 80), (180, 60), (200, 40), (160, 20)]
    cities = []
    for i in range(0, len(coords)):
        cities.append(i)

    # create distances
    for i in range (0, len(coords)):
        edges.append([])
        for j in range(0, len(coords)):
            if (i != j):
                edges[i].append(distance(coords[i], coords[j]))
            else:
                edges[i].append(0)
        tsp_window.draw_dots(coords[i])

    # generate initial population
    for index in range(population_size):
        permutation = [x for x in cities]
        random.shuffle(permutation)
        population.append(permutation)
 
    # genetic algorithm runs for 500 generations
    for generation in range(1, 500):
        for index in range(0, population_size):
            mate1 = []
            mate2 = []
            for i in range(0, len(population[index])):
                mate1.append(-1)
                mate2.append(-1)

            parents = []
            for i in range(0, 10):
                pick = random.randint(0, len(population) - 1)
                parents.append(population[pick])

            max = 0 
            for i in range(0, 10):
                fitness_val = get_fitness(parents[i], edges)
                if (fitness_val > max):
                    max = fitness_val
                    for j in range(0, len(parents[i])):
                        mate1[j] = parents[i][j]
            
            parents = []
            for i in range(0, 10):
                pick = random.randint(0, len(population) - 1)
                parents.append(population[pick])

            max = 0
            for i in range(0, 10):
                fitness_val = get_fitness(parents[i], edges)
                if (fitness_val > max):
                    max = fitness_val
                    for j in range(0, len(parents[i])):
                        mate2[j] = parents[i][j]

            if (generation == 1):
                new_pop.append(get_offspring(mate1, mate2))
            else:
                new_pop[index] = get_offspring(mate1, mate2)

    # get the top offspring from the latest generation
    sorted_pop = rank_population(new_pop, edges)
    sorted_pop = OrderedDict(sorted_pop)
    result = list(sorted_pop.keys())[0]
    tsp_window.draw_lines(new_pop[result], coords)
    print("Path:")
    print(new_pop[result])
    print("Distance:")
    print((float)(1 / get_fitness(new_pop[result], edges)))
    root.mainloop()

main()