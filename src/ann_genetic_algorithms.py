from ann import *
import ann_io
from genetic_algorithms import Genotype, Population
from ann_runner import AnnRunner
import random
import os

class AnnPopulation(Population):

    def __init__(self, random_seed, printer_runtime, printer_speed, size, mutation_rate, mutation_range, replacement_number, num_input, num_hidden, num_output, goal, outputfolder='gens/', is_visual=True, dump_to_files=False):
        super(AnnPopulation, self).__init__(random_seed, size, mutation_rate, mutation_range, replacement_number, num_input, num_hidden, num_output, goal, outputfolder='gens/')
        self.printer_runtime = printer_runtime
        self.printer_speed = printer_speed
        random.seed(random_seed)
        self.is_visual = is_visual
        self.dump_to_files = dump_to_files
        self.genotype_factory = AnnGenotypeFactory(self)

    def output(self, gen):
        if self.dump_to_files:
            self.sort_by_fitness()
            filename = self.outputfolder + 'best-gen-'+str(gen)+'.ann'
            member = self.members[-1]
            ann_io.save(member.ann, filename)
            
            cmdstring = 'ln -f ' + filename + ' ' + self.outputfolder + 'curbest.ann'
            print cmdstring
            os.system(cmdstring)


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
            rand_num = random.randint(0, 99)
            if rand_num < rate:
                lower, upper = self.population.mutation_range
                self.values[i] = random.randrange(lower, upper)

    def calculate_fitness(self, q=None):
        phenotype = self.express()
        fitness = 0
        for ideal_grid, actual_grid in phenotype:
            for ideal_row, actual_row in zip(ideal_grid, actual_grid):
                for ideal, actual in zip(ideal_row, actual_row):
                    if ideal == 1 and actual == 1:
                        fitness += 20
                    elif ideal == 0 and actual == 1:
                        fitness -= 1
        if q:
            q.put((self.values, fitness))

    def express(self):
        result = []
        self.ann.allConnections = self.values
        for world in self.population.goal:
            if self.population.is_visual:
                from gui_ann_runner import GuiAnnRunner
                runner = GuiAnnRunner(world)
            else:
                runner = AnnRunner(world)
            ideal_grid, actual_grid = runner.run(self.ann, iterations=self.population.printer_runtime, printer_speed=self.population.printer_speed, x=10, y=4)
            result.append((ideal_grid.grid, actual_grid.grid))
        return result
