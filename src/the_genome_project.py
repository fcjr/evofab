from ann import *
from ann_runner import AnnRunner
import random

"""
    Doesn't work if the neural network achieves sufficient intelligence to modify its source code

        -- Johnny Depp
"""

class Population:

    def __init__(self, size, mutation_rate, replacement_number, num_input, num_hidden, num_output, goal):
        self.size = size
        self.replacement_number = replacement_number
        self.mutation_rate = mutation_rate
        self.goal = goal
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.members = []

    def random_seed(self):
        for i in range(self.size):
            new_member = Member(self)
            new_member.randomize()
            self.members.append(new_member)

    def iterate(self, num_iterations=10):
        self.random_seed()
        for i in xrange(num_iterations):
            print self.eval_fitness()
            self.cull()
            self.breed()

    def eval_fitness(self):
        for num, member in enumerate(self.members):
            print 'expressing %d of %d' % (num + 1, len(self.members))
            member.calculate_fitness()
            print 'fitness: %d/%d' % (member.fitness, self.goal.width * self.goal.height)
        fitnesses = [member.fitness for member in self.members]
        fitnesses.sort(reverse=True)
        return fitnesses

    def cull(self):
        self.members.sort(key=lambda x: x.fitness)
        self.members = self.members[:self.replacement_number] #cull the population

    def breed(self):
        total_fitness = sum([member.fitness for member in self.members])
        children = []
        for member in self.members:
            breed_weight = member.fitness/total_fitness
            for i in range(int(round(breed_weight * self.replacement_number))):
                child = Member(self)
                child.crossover(member, self.get_random_other_member(member))
                child.mutate()
                children.append(child)
        self.members += children

    def get_random_other_member(self, to_ignore):
        """ returns a random member of the population other than the member specified
        """
        members = [member for member in self.members if member != to_ignore]
        choice = random.choice(members)
        return choice
        
class Member:

    def __init__(self, population):
        self.population = population
        self.ann = Network(population.num_input, population.num_hidden, population.num_output)
        self.weights = [ 0 for x in self.ann.allConnections ]
        self.fitness = 0

    def randomize(self):
        self.weights = [ random.randint(-10, 10) for x in self.weights]

    def crossover(self, p1, p2):
        location1 = random.randint(0, len(self.weights)/2)
        location2 = location1 + len(self.weights)/2
        self.weights = p1.weights[:location1] + p2.weights[location1:location2] + p1.weights[location2:]

    def mutate(self):
        rate = self.population.mutation_rate * 100
        for i in range(len(self.weights)):
            rand_num = random.randint(0, 99)
            if rand_num < rate:
                self.weights[i] = random.randint(-10, 10) #TODO: this is gonna break. Decide weight range

    def calculate_fitness(self):
        phenotype = self.express()
        fitness = phenotype.width * phenotype.height #init fitness to max fitness
        for ideal_row, actual_row in zip(self.population.goal.grid, phenotype.grid):
            for ideal, actual in zip(ideal_row, actual_row):
                if ideal == 1 and actual == 0:
                    fitness -= 1
                elif ideal == 0 and actual == 1:
                    fitness -= 0.5
        self.fitness = fitness

    def express(self):
        self.ann.allConnections = self.weights
        runner = AnnRunner(self.population.goal)
        return runner.run(self.ann, iterations=5000, x=400, y=150)
