from ann import *
import ann_io
from clean_ann_runner import AnnRunner
import random
from multiprocessing import Process, Queue

class Hat(object):

    def __init__(self, population):
        self.tickets = []
        for member in population:
            for i in range(member.fitness):
                self.tickets.append(member)

    def pull(self):
        return self.tickets[random.randint(0, len(self.tickets) -1)]

    def size(self):
        return len(self.tickets)

class GenericGenotypeFactory(object):
    def __init__(self, population):
        self.pop = population

    def new(self):
        return Genotype(self.pop)

class Population(object):

    def __init__(self, size, mutation_rate, replacement_number, num_input, num_hidden, num_output, goal, outputfolder='gens/'):
        self.genotype_factory = GenericGenotypeFactory(self)
        self.outputfolder = outputfolder
        self.size = size
        self.replacement_number = replacement_number
        self.mutation_rate = mutation_rate
        self.goal = goal
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.members = []

    def create_initial_population(self):
        for i in range(self.size):
            new_member = self.genotype_factory.new()
            new_member.randomize()
            self.members.append(new_member)

    def iterate(self, num_iterations=10, threadnum=5):
        self.create_initial_population()
        for i in xrange(num_iterations):
            print "evaluating generation %d" % (i + 1)
            print self.eval_fitness(threadnum)
            self.cull()
            self.breed()
            for member_num, member in enumerate(self.members):
                filename = self.outputfolder + 'g%d_m%d' % (i, member_num)
                ann_io.save(member.ann, filename)
                    
    def eval_fitness(self, threadnum):
        q = Queue()
        counter = 0
        for iteration in range(0, len(self.members), threadnum):
            processes = []
            while len(processes) < threadnum and counter + len(processes) < len(self.members):
                print 'evaluating members %d - %d of %d' % (counter + 1, counter + threadnum, len(self.members))
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
            child = self.genotype_factory.new()
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
        
class Genotype(object):
    """ Generic genotype for GAs """

    def __init__(self, population, size=0):
        self.population = population
        self.values = [ 0 for x in range(size)]
        self.fitness = None

    def crossover(self, p1, p2):
        location1 = random.randint(0, len(self.values)/2)
        location2 = location1 + len(self.values)/2
        self.values = p1.values[:location1] + p2.values[location1:location2] + p1.values[location2:]

    def randomize(self):
        self.values = [ random.randint(-10, 10) for x in self.values]
