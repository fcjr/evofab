from ann import *
import ann_io
from genetic_algorithms import Genotype, Population
from ann_runner import AnnRunner
import random
import os
import csv

statsfileheader = ['gen num', 'min', 'max', 'median']
curbest_filename = 'curbest.ann'
statsfile_filename = 'stats.csv'

class AnnPopulation(Population):

    def __init__(self, random_seed, printer_runtime, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, outputfolder, reward_for_correct=None, punishment_for_incorrect=None, goal=None, is_visual=True, dump_to_files=False, units_per_cell=0, recur = 0, time = 1):
        super(AnnPopulation, self).__init__(random_seed, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, outputfolder)
        self.goal = goal
        self.printer_runtime = printer_runtime
        self.units_per_cell = units_per_cell
        self.reward_for_correct = reward_for_correct
        self.punishment_for_incorrect = punishment_for_incorrect
        self.is_visual = is_visual
        self.dump_to_files = dump_to_files
        self.genotype_factory = AnnGenotypeFactory(self, recur, time)
        self.init_csv_writer()

    def init_csv_writer(self):
        if self.dump_to_files:
            print("outputfolder: ", self.outputfolder)
            print("statsfile_filename ", statsfile_filename)
            with open(self.outputfolder + statsfile_filename, 'w') as statsfile:
                writer = csv.writer(statsfile)
                writer.writerow(statsfileheader)

    def write_stats(self, gen):
        if self.dump_to_files:
            with open(self.outputfolder + statsfile_filename, 'a') as statsfile:
                self.sort_by_fitness()
                min_fitness = self.members[0].fitness
                max_fitness = self.members[-1].fitness
                median_fitness = self.members[len(self.members)/2].fitness
                writer = csv.writer(statsfile)
                writer.writerow([gen, min_fitness, max_fitness, median_fitness])

    def output(self, gen):
        if self.dump_to_files:
            self.sort_by_fitness()
            member = self.members[-1]
            ann_io.save(member.ann, self.outputfolder + curbest_filename)

class AnnGenotypeFactory(object):
    def __init__(self, population, recur, time):
        self.pop = population
        self.recur = recur
        self.time = time

    def new(self):
        return AnnGenotype(self.pop, self.recur, self.time)

class AnnGenotype(Genotype):

    def __init__(self, population, recur, time):
        if recur == 1:
            self.ann = Network(population.num_input, population.num_hidden, population.num_output, out_to_in = True, time = time)
        elif recur == 2:
            self.ann = Network(population.num_input, population.num_hidden, population.num_output, in_to_in = True, time = time)
        elif recur == 3:
            self.ann = Network(population.num_input, population.num_hidden, population.num_output, out_to_in = True, in_to_in = True, time = time)
        else:
            self.ann = Network(population.num_input, population.num_hidden, population.num_output, out_to_in = False, in_to_in = False, time = 0)
        self.population = population
        size = len(self.ann.allConnections)
        super(AnnGenotype, self).__init__(population, size)

    def mutate(self):
        rate = self.population.mutation_rate * 100
        lower, upper = self.population.mutation_range
        for i in range(len(self.values)):
            rand_num = random.uniform(-100, 100)
            if rand_num < rate:
                self.values[i] += random.uniform(lower, upper)

    def calculate_fitness(self, q=None):
        phenotype = self.express()
        fitness = 0
        for ideal_grid, actual_grid in phenotype:
            for ideal_row, actual_row in zip(ideal_grid, actual_grid):
                for ideal, actual in zip(ideal_row, actual_row):
                    if ideal == 1 and actual == 1:
                        fitness += self.population.reward_for_correct
                    elif ideal == 0 and actual == 1:
                        fitness -= self.population.punishment_for_incorrect
        if q:
            q.put((self.values, fitness))
        else:
            self.fitness = fitness

    def express(self):
        result = []
        self.ann.allConnections = self.values
        for world in self.population.goal:
            if self.population.is_visual:
                from gui_ann_runner import GuiAnnRunner
                runner = GuiAnnRunner(world, self.population.units_per_cell)
            else:
                runner = AnnRunner(world, self.population.units_per_cell)
            ideal_grid, actual_grid = runner.run(self.ann, iterations=self.population.printer_runtime)
            result.append((ideal_grid.grid, actual_grid.grid))
        return result
