from virtualprinter import VirtualPrinter
from camera import VisualCamera, Camera
from vector import Vector
from grid import Grid
from gridworld import GridWorld
from ann import Network
import pygame

import csv

camera_headers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
output_headers = ['x velocity', 'y velocity']

graycode = {
       0  : "00000",
       1  : "00001",
       2  : "00010",
       3  : "00011",
       4  : "00100",
       5  : "00101",
       6  : "00110",
       7  : "00111",
       8  : "01000",
       9  : "01001",
       10 : "01010",
       11 : "01011",
       12 : "01100",
       13 : "01101",
       14 : "01110",
       15 : "01111",
       16 : "10000",
       17 : "10001",
       18 : "10010",
       19 : "10011",
       20 : "10100",
       21 : "10101",
       22 : "10110",
       23 : "10111",
       24 : "11000",
       25 : "11001",
       26 : "11010",
       27 : "11011",
       28 : "11100",
       29 : "11101",
       30 : "11110",
       31 : "11111",
    }

class training_set_loader:

    def __init__(self, path):
        self.path = path

    def read(self):
        """ returns (camera_vals, x,y velocities) """

        with open(self.path, 'r') as to_read:
            reader = csv.reader(to_read)
            _ = reader.next()
            camera_vals = []
            velocities = []
            for row in reader:
                camera_vals.append(row[:len(camera_headers)])
                velocities.append(row[len(camera_headers):][0])
                velocities = [[int(x) for x in string] for string in velocities]
        return (
                [[float(x) for x in row] for row in camera_vals],
                velocities
                )

class ann_trainer:

    def __init__(self, ideal_grid):
        self.gridworld = GridWorld(ideal_grid.width, ideal_grid.height, ideal_grid.gridsize)
        self.gridworld.set_ideal_grid(ideal_grid)
        self.printer = VirtualPrinter(10, 10, 9, 1, pygame.color.Color("darkorange"), self.gridworld)
        self.camera = VisualCamera(self.gridworld, self.printer, 3)
        self.ideal_camera = Camera(self.gridworld.ideal_grid, self.printer, 3)

        #gui stuff
        pygame.init()
        width = self.gridworld.width() * self.gridworld.gridsize()
        height = self.gridworld.height() * self.gridworld.gridsize()
        self.window = pygame.display.set_mode((width, height))

    def train(self, n, paths_to_training_sets):
        n.inputs = []
        n.targets = []
        for path in paths_to_training_sets:
            loader = training_set_loader(path)
            inputs, targets = loader.read()
            n.inputs += inputs
            n.targets += targets
            #print 'loaded', path
        n.test()
        n.train(20)

    def run(self, n):
        self.printer.position = Vector(270, 150)
        while True:
            self.printer.setPenDown()
            actual = self.camera.camera.all_cell_values()
            ideal = self.ideal_camera.all_cell_values()
            pattern = [i - a for i,a in zip(actual, ideal)]
            result = n.propagate(pattern)
            #print 'pattern', pattern
            result = [int(round(x)) for x in result]
            result = ''.join(map(str, result))
            #print 'velocities', (self.decode(result[:5]), self.decode(result[5:]))
            self.printer.v = Vector(self.decode(result[:5]), self.decode(result[5:]))
            self.printer.simulate(1)
            self.redraw()
            pygame.display.update()

    def redraw(self):
        self.gridworld.draw(self.window)
        self.printer.draw(self.window)
        self.camera.draw(self.window)

    def decode(self, grayval):
        rev_code = dict([(val, key) for key, val in graycode.items()])
        return (rev_code[grayval] - 16) * 100

n = Network(9, 7, 10)
ideal_grid = Grid(scale=60, path='corner.test')
trainer = ann_trainer(ideal_grid)
trainer.train(n, ['training_sets/corner/' + x for x in ['output1.out', 'output2.out', 'output3.out', 'output4.out', 'output5.out']]) #this is bad fix this
trainer.run(n)
