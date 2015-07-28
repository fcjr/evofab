from ann import *
import ann_io
from genetic_algorithms import Genotype, Population
from ann_runner import AnnRunner
import random

class AnnPopulation(Population):

    def __init__(self, size, mutation_rate, replacement_number, num_input, num_hidden, num_output, goal, outputfolder='gens/', is_visual=True, dump_to_files=False):
        super(AnnPopulation, self).__init__(size, mutation_rate, replacement_number, num_input, num_hidden, num_output, goal, outputfolder='gens/')
        self.is_visual = is_visual
        self.dump_to_files = dump_to_files
        self.genotype_factory = AnnGenotypeFactory(self)

    def output(self, gen):
        if self.dump_to_files:
            self.sort_by_fitness()
            for member_num, member in enumerate(self.members):
                filename = self.outputfolder + 'g%d_m%d' % (gen, member_num)
                ann_io.save(member.ann, filename)

class AnnGenotypeFactory(object):
    def __init__(self, population):
        self.pop = population

    def new(self):
        return AnnGenotype(self.pop)

class AnnGenotype(Genotype):

    def __init__(self, population):
        self.population = population
        self.ann = Network(population.num_input, population.num_hidden, population.num_output)
        size = len(self.ann.allConnections)
        super(AnnGenotype, self).__init__(population, size)

    def mutate(self):
        rate = self.population.mutation_rate * 100
        for i in range(len(self.values)):
            rand_num = random.randint(0, 99) #TODO this is bad. dont hardcode this...
            if rand_num < rate:
                self.values[i] = random.randrange(-10, 10) #TODO: this is gonna break. Decide weight range

    def calculate_fitness(self, q=None):
        phenotype = self.express()
        fitness = 0
        for ideal_row, actual_row in zip(self.population.goal.grid, phenotype.grid):
            for ideal, actual in zip(ideal_row, actual_row):
                if ideal == 1 and actual == 1:
                    fitness += 20
                elif ideal == 0 and actual == 1:
                    fitness -= 1
        self.fitness = fitness
        if q:
            q.put((self.values, fitness))

    def express(self):
        self.ann.allConnections = self.values
        if self.population.is_visual:
            from gui_ann_runner import GuiAnnRunner
            runner = GuiAnnRunner(self.population.goal)
        else:
            runner = AnnRunner(self.population.goal)
        return runner.run(self.ann, iterations=1000, x=325, y=125)
