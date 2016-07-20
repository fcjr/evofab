from ann_genetic_algorithms import AnnGenotype, AnnPopulation
from genetic_algorithms import Population
from evocontroller.evoPyLib.evoPyLib import *
from evocontroller.evoCamera.evoCamera import EvoCamera
import time
import sys
import threading

kbdInput = ""

class PhysPopulation(AnnPopulation):

    """Population class for the physical EvoFab system. Is used to
    wrap up a significant amount of information important for the
    execution of the GA within members
    """

    def __init__(self, random_seed, printer_runtime, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, serial_port, sensor_serial_port, conveyor_port, camera, outputfolder, crop=True, is_visual=True, dump_to_files=False):
        super(PhysPopulation, self).__init__(random_seed, printer_runtime, size, mutation_rate, mutation_range, crossover_rate, replacement_number, num_input, num_hidden, num_output, outputfolder, is_visual=is_visual, dump_to_files=dump_to_files)
        self.genotype_factory = PhysGenotypeFactory(self)
        #TODO: should probably test that sensor and controller serial ports are valid
        self.controller = EvoController(serial_port)
        self.sense = EvoArray(sensor_serial_port)
        self.camera = EvoCamera(camera, crop)
        self.conveyor = EvoConveyor(conveyor_port)
        listener = threading.Thread(target=kbdListener)
        listener.start()

class PhysGenotypeFactory(object):
    def __init__(self, population):
        self.pop = population
    
    def new(self):
        return PhysGenotype(self.pop)

def kbdListener():
    global kbdInput
    kbdInput = raw_input()

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
        print("evaluating...")
        self.population.controller.testHome()
        fitness = self.population.camera.eval()
        time.sleep(2)
        self.fitness = fitness * 100
        print "fitness:", self.fitness
        self.population.camera.showImage()
        self.population.conveyor.run()

    def get_velocity(self, instruction):
        """Basic translation from expected outputs from the neural network
        and the strings needed for printer control. Returns a string
        """

        if instruction == "10":
            return "+030"
        elif instruction == "01":
            return "-030"
        else:
            return "+000"

    def express(self):
        """Expresses the Neural Network by running the neural net on the
        printer for an amount of time specified by the population's
        printer_runtime. After expression, instructs the printer to move
        the print bed to the "eval" location for evaluation.
        No return value expected
        """

        global kbdInput
        c = self.population.controller
        c.home()
        start_time = time.time()
        c.extrude()
        time.sleep(4)
        while time.time() - start_time < self.population.printer_runtime:
            #if kbdInput == "q":
            #    c.pause()
            #    c.disable()
            #    c.close()
            #    sys.exit(0)
            #run the printer based on neural net responses
            photo_array_values = self.population.sense.getNext()
            print photo_array_values
            time.sleep(0.4)
            result = self.ann.propagate(photo_array_values)
            result = [int(round(x)) for x in result]
            result = ''.join(map(str, result))
            #result are floats returned by the neural network
            command = self.get_velocity(result[:2]) + self.get_velocity(result[2:])
            result = c.changeVelocity(command)
        print time.time() - start_time, "seconds elapsed"
        c.pause()
        return
