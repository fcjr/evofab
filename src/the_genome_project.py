from ann import *
import random

"""
    Doesn't work if the neural network achieves sufficient intelligence to modify its source code

        -- Johnny Depp
"""

class Population:

    def __init__(self, size, mutation_rate, replacment_number, num_input, num_hidden, num_output):
        self.size = size
        self.replacement_number
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output

    def breed(self):
        #TODO: write this dood
        total_fitness = sum([member.fitness for member in self.members])
        children = []
        for member in members:
            breed_weight = member.fitness/total_fitness
            for i in int(breed_weight * self.replacement_number)
        
class Member:

    def __init__(self, population):
        self.population = population
        self.ann = Network(population.num_input, population.num_hidden, population.num_output)
        self.weights = [ 0 for x in self.ann.allConnections ]
        self.fitness = 0

    def crossover(self, p1, p2):
        location1 = random.randint(0, len(weights/2))
        location2 = location1 + len(weights/2)
        self.weights = p1[:location1] + p2[location1:location2] + p1[location2:]

    def mutate(self):
        rate = self.population.mutation_rate * 100
        for i in range(len(self.weights)):
            rand_num = random.randint(0, 99)
            if rand_num < rate:
                self.weights[i] = random(-10, 10) #TODO: this is gonna break. Decide weight range

    def fitness(self):
        return False
