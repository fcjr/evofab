from printer import Printer
from camera import Camera
from grid import Grid
from vector import Vector
from gridworld import GridWorld
from ann import Network

class AnnRunner(object):
    """Wraps up the gross reality of running a ``print'' using the printer simulation (controlled by a neural network)"""

    camera_size = 3

    def __init__(self, ideal_grid_path, cell_size, units_per_cell=10):
        """Sets up all the pieces needed to perform a print with the simulated 3d printer (controlled by the neural network). Takes in a path to an a ``goal'' or ``ideal'' grid, and constructs the GridWorld based on the dimensions of that goal grid. Understands both a ``camera'', which observes the actual world (around the print head) and an ``ideal camera'' which observes the same location but based on the ``goal grid''
        """

        ideal_grid = Grid(path=ideal_grid_path, scale=cell_size)
        self.ideal_grid = ideal_grid
        self.gridworld = GridWorld(ideal_grid.width, ideal_grid.height, cell_size)
        self.gridworld.set_ideal_grid(ideal_grid)
        self.printer = Printer(10, 10, 9, self.gridworld, units_per_cell) #TODO: shouldn't be giving location values here when it's determined somewhere else. that smells a lot
        self.camera = Camera(self.gridworld.grid, self.printer, self.camera_size)
        self.ideal_camera = Camera(self.gridworld.ideal_grid, self.printer, self.camera_size)

    def run(self, n, iterations=10000):
        """Runs a simulated print run with the printer simulation (controlled by an ANN. Starts the printer in the location provided by the ideal grid spec
        """

        #set the printer location to the starting postition as defined by the ideal_grid spec
        self.printer.set_position_on_grid(*self.gridworld.get_starting_position())
        for i in xrange(iterations):
            self.printer.setPenDown()
            actual = self.camera.all_cell_values()
            ideal = self.ideal_camera.all_cell_values()
            pattern = [i - a for i,a in zip(actual, ideal)]
            result = n.propagate(pattern)
            result = [int(round(x)) for x in result]
            result = ''.join(map(str, result))
            self.printer.set_printer_direction(self.get_velocity(result[:2]), self.get_velocity(result[2:]))
            self.printer.simulate()
            self.update()
        return (self.ideal_grid, self.gridworld.grid)

    def update(self):
        return

    def get_velocity(self, instruction):
        """Translates between the output of the neural network and direction instructions for the printer. leftright and updown are translated separately"""
        if instruction == "10":
            return -1
        elif instruction == "01":
            return 1
        else:
            return 0
