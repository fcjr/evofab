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
    """A population of relatively simple neural networks. Currently impelmented to be semi-specific to the task of optimimizing neural netowrks to control a 3d-printer to draw particular (specified) shapes"""

    def __init__(self, random_seed, printer_runtime, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, outputfolder, reward_for_correct=None, punishment_for_incorrect=None, goal=None, is_visual=True, dump_to_files=False, cell_size=0, units_per_cell=0, recur = 0, time = 1):
        """Constructs a population on which to perform evolution to optimize to the defined fitness function

        random_seed: the random seed for the stochastic components of the system. Needs to be specified so that we have repeatable experiments
        printer_runtime: the amount of time steps for which the printer will draw on the world before being cut off
        size: the size of the population
        mutation_rate: the likelyhood of a component of a genotype being randomly changed during mutation (evaluated for each individual component of the encoding
        mutation_range: the range of values for mutation
        crossover_rate: the probability that a new member of the population will be created using crossover (breeding) instead of randomly mutated from a fitness-proportionally-selected parent
        replacement_number: the number of members of the population to cull after fitness ranking. must be even because crossover yields two children
        num_input: the number of input nodes for the neural network
        num_hidden: the number of hidden nodes for the neural network
        num_output: the number of output nodes for the neural network
        outputfolder: relative path to the folder where results shouldbe output to
        reward_for_correct: reward for putting material where there is supposed to be material
        punishment_for_incorrect: punishment for not putting material where there should be material
        goal: a list of relative paths to ``ideal/goal'' grid specifications (text files containing a rectangle of 0s and 1s (where a 1 means ``there should be material here'') and a single ``S'' denoting the start location for the printer
        is_visual: False if there should be GUI (pygame) output during evaluation, and False otherwise
        dump_to_files: Whether or not to dump statistics about fitness over time and a Pickled version of the highest-fitness individual so far to the appropriate directory
        cell_size: the number of pixels in a single grid cell
        units_per_cell: the factor by which cell width is divided by to determine the distance moved by the printer in a single time unit
        recur: 0 if there should be no recurrance in the neural network
               1 for recurance from outputs to inputs
               2 for recurance from inputs to inputs
               3 for recurance from both
        time: how many time steps to recur for
        """

        super(AnnPopulation, self).__init__(random_seed, size, mutation_rate, mutation_range, crossover_rate, replacement_number, outputfolder)
        self.goal = goal
        self.printer_runtime = printer_runtime
        self.units_per_cell = units_per_cell
        self.cell_size = cell_size
        self.reward_for_correct = reward_for_correct
        self.punishment_for_incorrect = punishment_for_incorrect
        self.is_visual = is_visual
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.dump_to_files = dump_to_files
        self.genotype_factory = AnnGenotypeFactory(self, recur, time)
        self.init_csv_writer()

    def init_csv_writer(self):
        """set up the CSV writer to be used to write statistic to a file"""
        if self.dump_to_files:
            print("outputfolder: ", self.outputfolder)
            print("statsfile_filename ", statsfile_filename)
            with open(self.outputfolder + statsfile_filename, 'w') as statsfile:
                writer = csv.writer(statsfile)
                writer.writerow(statsfileheader)

    def write_stats(self, gen):
        """write relevant statistics to a file"""
        if self.dump_to_files:
            with open(self.outputfolder + statsfile_filename, 'a') as statsfile:
                self.sort_by_fitness()
                min_fitness = self.members[0].fitness
                max_fitness = self.members[-1].fitness
                median_fitness = self.members[len(self.members)/2].fitness
                writer = csv.writer(statsfile)
                writer.writerow([gen, min_fitness, max_fitness, median_fitness])

    def output(self, gen):
        """Save the higest fitness member of the population to a file"""
        if self.dump_to_files:
            self.sort_by_fitness()
            member = self.members[-1]
            ann_io.save(member.ann, self.outputfolder + curbest_filename)

class AnnGenotypeFactory(object):
    def __init__(self, population, recur, time):
        """An GenotypeFactory for ANNs"""

        self.pop = population
        self.recur = recur
        self.time = time

    def new(self):
        return AnnGenotype(self.pop, self.recur, self.time)

class AnnGenotype(Genotype):

    def __init__(self, population, recur, time):
        """Construct an ANN Genotype with the given population (and therefore the given properties of that population)
        
        recur: 0 if there should be no recurrance in the neural network
               1 for recurance from outputs to inputs
               2 for recurance from inputs to inputs
               3 for recurance from both
        time: how many time steps to recur for"""

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
        """Mutate this member. Each unit of the members encoding will have a *mutation_rate* chance of being mutated. Each unit is evaluated independently"""

        rate = self.population.mutation_rate * 100
        lower, upper = self.population.mutation_range
        for i in range(len(self.values)):
            rand_num = random.uniform(-100, 100)
            if rand_num < rate:
                self.values[i] += random.uniform(lower, upper)

    def calculate_fitness(self, q=None):
        """Calculate the fitness of this member of the population by first using it to control the 3d printer, and then evaluating the fitness of the output. Fitness is determined by how well the output from the printer matches the ``ideal/goal'' grids (paths specified in the populations.goal list)"""

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
        """Control the simulated 2d 3d-printer with this member of the population and evaluate the fitness of the output"""
        result = []
        self.ann.allConnections = self.values
        for world in self.population.goal:
            if self.population.is_visual:
                from gui_ann_runner import GuiAnnRunner
                runner = GuiAnnRunner(world, self.population.cell_size, self.population.units_per_cell)
            else:
                runner = AnnRunner(world, self.population.cell_size, self.population.units_per_cell)
            ideal_grid, actual_grid = runner.run(self.ann, iterations=self.population.printer_runtime)
            result.append((ideal_grid.grid, actual_grid.grid))
        return result
