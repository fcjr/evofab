from ann_genetic_algorithms import AnnGenotype, AnnPopulation
from genetic_algorithms import Population
from evocontroller.evoPyLib.evoPyLib import *
import time

class PhysPopulation(AnnPopulation):

    """Population class for the physical EvoFab system. Is used to
    wrap up a significant amount of information important for the
    execution of the GA within members
    """

    def __init__(self, random_seed, printer_runtime, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, serial_port, sensor_serial_port, outputfolder, is_visual=True, dump_to_files=False):
        super(PhysPopulation, self).__init__(random_seed, printer_runtime, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, outputfolder, is_visual=is_visual, dump_to_files=dump_to_files)
        self.genotype_factory = PhysGenotypeFactory(self)
        #TODO: should probably test that sensor and controller serial ports are valid
        self.controller = EvoController(serial_port)
        self.sense = EvoArray(sensor_serial_port)

class PhysGenotypeFactory(object):
    def __init__(self, population):
        self.pop = population
    
    def new(self):
        return PhysGenotype(self.pop)

class PhysGenotype(AnnGenotype):

    """Genotype for the physical EvoFab system. Is associated with
    a population, and can express and evaluate it's own fitness
    """

    def __init__(self, population):
        super(PhysGenotype, self).__init__(population)

    def calculate_fitness(self):
        """Caculates the fitness of this genotype. First expresses
        the neural network, then does some CV work to determine
        the fitness of the member. Returns that fitness as a float
        """
        phenotype = self.express()
        #TODO: do openCV eval to produce fitness value
        return

    def get_velocity(self, instruction):
        """Basic translation from expected outputs from the neural network
        and the strings needed for printer control. Returns a string
        """

        if instruction == "10":
            return "+025"
        elif instruction == "01":
            return "-025"
        else:
            return "+000"

    def express(self):
        """Expresses the Neural Network by running the neural net on the
        printer for an amount of time specified by the population's
        printer_runtime. After expression, instructs the printer to move
        the print bed to the "eval" location for evaluation.
        No return value expected
        """

        start_time = time.time()
        c = self.pop.controller
        c.home()
        c.extrude()
        while time.time() - start_time < self.pop.printer_runtime:
            #run the printer based on neural net responses
            photo_array_values = self.sense.getNext()
            result = self.ann.propogate(photo_array_values)
            result = [int(round(x)) for x in result]
            result = ''.join(map(str, result))
            #result are floats returned by the neural network
            c.changeVelocity(self.get_velocity(result[:2] + self.get_velocity(result[2:])))
        c.pause()
        c.testHome()
        return
