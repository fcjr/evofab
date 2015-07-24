from printer import Printer
from clean_camera import Camera
from vector import Vector
from grid import Grid
from clean_gridworld import GridWorld
from ann import Network

import csv

camera_headers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
output_headers = ['x velocity', 'y velocity']

downsample_constant = 100

camera_size = 3

class AnnRunner:

    def __init__(self, ideal_grid):
        self.gridworld = GridWorld(ideal_grid.width, ideal_grid.height, ideal_grid.gridsize)
        self.gridworld.set_ideal_grid(ideal_grid)
        self.printer = Printer(10, 10, 9, 1, self.gridworld)
        self.camera = Camera(self.gridworld.grid, self.printer, camera_size)
        self.ideal_camera = Camera(self.gridworld.ideal_grid, self.printer, camera_size)

        #gui stuff
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
        return self.gridworld.grid

    def get_velocity(self, instruction):
        if instruction == "10":
            return -100
        elif instruction == "01":
            return 100
        else:
            return 0
