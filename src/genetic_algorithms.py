from ann import *
import ann_io
import random
from multiprocessing import Process, Queue

class Hat(object):
    """A hat that is used to select members for fitness-proportional breeding. Members with higher fitness will be pulled from the hat more often"""

    def __init__(self, population):
        self.population = population
        self.weights = [x.fitness for x in population]
        pop_min = min(self.weights)
        self.weights = [x + (-1*pop_min) for x in self.weights]
        self.weight_sum = 0
        for w in self.weights:
            self.weight_sum += w

    def pull(self):
        """Pull a member of the population from the hat. Members with higher fitness will be more likely to be picked"""
        value = random.uniform(0, self.weight_sum)
        for i,w in enumerate(self.weights):
            value -= w
            if value <= 0:
                return self.population[i]

class GenericGenotypeFactory(object):
    """A superclass for GenotypeFactory(ies)"""
    def __init__(self, population):
        self.pop = population

    def new(self):
        return Genotype(self.pop)


class Population(object):
    """ A ``population'' on which to perform optimization through evolution"""

    def __init__(self, random_seed, size, mutation_rate, mutation_range, crossover_rate, replacement_number, outputfolder):
        """Constructs a population on which to perform evolution to optimize to the defined fitness function

        random_seed: the random seed for the stochastic components of the system. Needs to be specified so that we have repeatable experiments
        size: the size of the population
        mutation_rate: the likelyhood of a component of a genotype being randomly changed during mutation (evaluated for each individual component of the encoding
        mutation_range: the range of values for mutation
        crossover_rate: the probability that a new member of the population will be created using crossover (breeding) instead of randomly mutated from a fitness-proportionally-selected parent
        replacement_number: the number of members of the population to cull after fitness ranking. must be even because crossover yields two children
        outputfolder: relative path to the folder where results shouldbe output to
        """

        random.seed(random_seed)
        self.genotype_factory = GenericGenotypeFactory(self)
        self.outputfolder = outputfolder
        self.crossover_rate = crossover_rate
        self.size = size
        self.replacement_number = replacement_number
        self.mutation_rate = mutation_rate
        self.mutation_range = mutation_range
        self.members = []

    def create_initial_population(self):
        """Randomly generate the population"""

        for i in range(self.size):
            new_member = self.genotype_factory.new()
            new_member.randomize()
            self.members.append(new_member)

    def write_stats(self, gen):
        return

    def iterate(self, num_iterations=10, threadnum=5):
        """iterate on the process of evolution, etc"""

        self.create_initial_population()
        print "evaluating initial population"
        self.eval_fitness(self.members, threadnum)
        self.print_fitnesses()
        self.output(0)
        for i in xrange(num_iterations):
            print "evaluating generation %d" % (i + 1)
            self.cull()
            children = self.breed()
            self.eval_fitness(children, threadnum)
            self.print_fitnesses()
            self.output(i)
            self.write_stats(i)

    def print_fitnesses(self):
        fitnesses = [member.fitness for member in self.members]
        fitnesses.sort()
        print fitnesses

    def output(self, gen):
        return

    def eval_fitness(self, members, threadnum):
        """Evaluate the fitness of all of the members of the population"""
        q = Queue()
        counter = 0
        for num, m in enumerate(members):
            print "evaluating member: ", num
            m.calculate_fitness()
        # TODO: um this looks like it might have been causing... Problems.
        # for iteration in range(0, len(members), threadnum):
        #     processes = []
        #     print 'evaluating members %d - %d of %d' % (counter + 1, counter + threadnum, len(members))
        #     while len(processes) < threadnum and counter + len(processes) < len(members):
        #         member = members[iteration + len(processes)]
        #         p = Process(target=member.calculate_fitness, args=(q,))
        #         p.start()
        #         processes.append(p)
        #     for p in processes:
        #         p.join()
        #     while not q.empty():
        #         actual_vals, fitness = q.get()
        #         possible_members = members[counter:counter + threadnum] #might be missing one here
        #         member_num = 0
        #         found = False
        #         while member_num < threadnum and not found:
        #             if actual_vals == possible_members[member_num].values:
        #                 found = True
        #                 possible_members[member_num].fitness = fitness
        #             member_num += 1
        #         members[counter].fitness
        #     counter += threadnum

    def cull(self):
        """cull the *replacement_number* lowest-ranked members of the population"""

        self.sort_by_fitness()
        self.members = self.members[self.replacement_number:] #cull the population

    def sort_by_fitness(self):
        self.members.sort(key=lambda x: x.fitness)

    def should_crossover(self):
        pick = random.randint(0, 99)
        return pick < (self.crossover_rate * 100)

    def breed(self):
        """(this is a bad name for this) do both breeding and crossover (split based on crossover_rate) to replace the culled members of the population.
        """

        assert(self.replacement_number % 2 == 0)
        hat = Hat(self.members)
        children = []
        #for debug
        num_crossover = 0
        num_mutated = 0
        #end for debug
        while len(children) < self.replacement_number:
            p1 = hat.pull()
            p2 = hat.pull()
            c1 = self.genotype_factory.new()
            c2 = self.genotype_factory.new()
            if (self.should_crossover()):
                c1.crossover(p1, p2)
                c2.crossover(p2, p1) #TODO: does this do what i want?
                num_crossover += 2
            else:
                c1.values = [x for x in p1.values] #TODO: should do this in a .clone() in the parent -- not like this...
                c2.values = [x for x in p2.values]
                c1.mutate()
                c2.mutate()
                num_mutated += 2
            children.append(c1)
            children.append(c2)
        self.members += children
        print "crossover rate", self.crossover_rate
        print "num bred", num_crossover
        print "num mutated", num_mutated
        print "total", self.replacement_number
        return children


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
        """Describes crossover for a Genotype that is encoded as a list of values. Does two point crossover for two members of the population. Does kind of a bad job probably(?)"""

        location1 = random.randint(0, len(self.values))
        location2 = random.randint(0, len(self.values))
        while location2 == location1:
            location2 = random.randint(0, len(self.values))
        location1, location2 = min(location1, location2), max(location1, location2)
        self.values = p1.values[:location1] + p2.values[location1:location2] + p1.values[location2:]

    def randomize(self):
        """Randomize this member of the population"""
        self.values = [ random.randrange(-10, 10) for x in self.values]
