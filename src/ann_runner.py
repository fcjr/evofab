from printer import Printer
from camera import Camera
from vector import Vector
from gridworld import GridWorld
from ann import Network

class AnnRunner(object):

    camera_size = 3

    def __init__(self, ideal_grid):
        self.gridworld = GridWorld(ideal_grid.width, ideal_grid.height, ideal_grid.gridsize)
        self.gridworld.set_ideal_grid(ideal_grid)
        self.printer = Printer(10, 10, 9, 1, self.gridworld)
        self.camera = Camera(self.gridworld.grid, self.printer, self.camera_size)
        self.ideal_camera = Camera(self.gridworld.ideal_grid, self.printer, self.camera_size)
        width = self.gridworld.width() * self.gridworld.gridsize()
        height = self.gridworld.height() * self.gridworld.gridsize()

    def run(self, n, x=270, y=150, iterations=10000):
        self.printer.position = Vector(x, y)
        for i in xrange(iterations):
            self.printer.setPenDown()
            actual = self.camera.all_cell_values()
            ideal = self.ideal_camera.all_cell_values()
            pattern = [i - a for i,a in zip(actual, ideal)]
            result = n.propagate(pattern)
            result = [int(round(x)) for x in result]
            result = ''.join(map(str, result))
            self.printer.v = Vector(self.get_velocity(result[:2]), self.get_velocity(result[2:]))
            self.printer.simulate(1)
            self.update()
        return self.gridworld.grid

    def update(self):
        return

    def get_velocity(self, instruction):
        if instruction == "10":
            return -900
        elif instruction == "01":
            return 900
        else:
            return 0
