from ann import *
from ann_runner import AnnRunner
import random
from multiprocessing import Process, Queue

"""
    Doesn't work if the neural network achieves sufficient intelligence to modify its source code

        -- Johnny Depp
"""

class Hat:

    def __init__(self, population):
        self.tickets = []
        for member in population:
            for i in range(member.fitness):
                self.tickets.append(member)

    def pull(self):
        return self.tickets[random.randint(0, len(self.tickets) -1)]

    def size(self):
        return len(self.tickets)

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

    def iterate(self, num_iterations=10, threadnum=5):
        self.random_seed()
        for i in xrange(num_iterations):
            print "evaluating generation %d" % (i + 1)
            print self.eval_fitness(threadnum)
            self.cull()
            self.breed()

    def eval_fitness(self, threadnum):
        q = Queue()
        counter = 0
        for iteration in range(0, len(self.members), threadnum):
            processes = []
            while len(processes) < threadnum and counter + len(processes) + 1 < len(self.members):
                print 'evaluating members %d - %d of %d' % (counter, counter + threadnum - 1, len(self.members))
                member = self.members[iteration + len(processes)]
                p = Process(target=member.calculate_fitness, args=(q,))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
            while not q.empty():
                self.members[counter].fitness = q.get()
                counter += 1
        fitnesses = [member.fitness for member in self.members]
        fitnesses.sort()
        return fitnesses

    def cull(self):
        self.members.sort(key=lambda x: x.fitness)
        self.members = self.members[self.replacement_number:] #cull the population

    def breed(self):
        hat = Hat(self.members)
        children = []
        for i in range(self.replacement_number):
            current_member = hat.pull()
            child = Member(self)
            child.crossover(current_member, self.get_random_other_member(current_member))
            child.mutate()
            children.append(child)
        print len(children)
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

    def calculate_fitness(self, q):
        phenotype = self.express()
        fitness = phenotype.width * phenotype.height #init fitness to max fitness
        for ideal_row, actual_row in zip(self.population.goal.grid, phenotype.grid):
            for ideal, actual in zip(ideal_row, actual_row):
                if ideal == 1 and actual == 0:
                    fitness -= 3
                elif ideal == 0 and actual == 1:
                    fitness -= 1
        self.fitness = fitness
        q.put(fitness)

    def express(self):
        self.ann.allConnections = self.weights
        runner = AnnRunner(self.population.goal)
        return runner.run(self.ann, iterations=3000, x=325, y=175)
