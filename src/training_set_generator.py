import pygame
import csv
from gridworld import GridWorld
from grid import Grid
from virtualprinter import VirtualPrinter
from camera import VisualCamera
from vector import Vector

graycode = {
       0  : [0, 0, 0, 0, 0],
       1  : [0, 0, 0, 0, 1],
       2  : [0, 0, 0, 1, 0],
       3  : [0, 0, 0, 1, 1],
       4  : [0, 0, 1, 0, 0],
       5  : [0, 0, 1, 0, 1],
       6  : [0, 0, 1, 1, 0],
       7  : [0, 0, 1, 1, 1],
       8  : [0, 1, 0, 0, 0],
       9  : [0, 1, 0, 0, 1],
       10 : [0, 1, 0, 1, 0],
       11 : [0, 1, 0, 1, 1],
       12 : [0, 1, 1, 0, 0],
       13 : [0, 1, 1, 0, 1],
       14 : [0, 1, 1, 1, 0],
       15 : [0, 1, 1, 1, 1],
       16 : [1, 0, 0, 0, 0],
       17 : [1, 0, 0, 0, 1],
       18 : [1, 0, 0, 1, 0],
       19 : [1, 0, 0, 1, 1],
       20 : [1, 0, 1, 0, 0],
       21 : [1, 0, 1, 0, 1],
       22 : [1, 0, 1, 1, 0],
       23 : [1, 0, 1, 1, 1],
       24 : [1, 1, 0, 0, 0],
       25 : [1, 1, 0, 0, 1],
       26 : [1, 1, 0, 1, 0],
       27 : [1, 1, 0, 1, 1],
       28 : [1, 1, 1, 0, 0],
       29 : [1, 1, 1, 0, 1],
       30 : [1, 1, 1, 1, 0],
       31 : [1, 1, 1, 1, 1],
    }

camera_headers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
output_headers = ['x velocity', 'y velocity']

class Generator:
    movement_constant = 3

    aquire_data = True

    def __init__(self, ideal_grid=None, ideal_grid_path=None):
        """ Set pygame stuff up for running the simulation."""

        assert ideal_grid or ideal_grid_path, "must provide at least one ideal grid"

        self.gridworld = GridWorld(ideal_grid.width, ideal_grid.height, ideal_grid.gridsize)
        self.gridworld.set_ideal_grid(ideal_grid)
        self.printer = VirtualPrinter(10, 10, 9, 1, pygame.color.Color("darkorange"), self.gridworld)
        self.camera = VisualCamera(self.gridworld, self.printer, 3)
        
        #gui stuff
        pygame.init()
        width = self.gridworld.width() * self.gridworld.gridsize()
        height = self.gridworld.height() * self.gridworld.gridsize()
        self.window = pygame.display.set_mode((width, height))

    def generate(self, outputfile):
        inputs = []
        outputs = []
        self.printer.setPenDown()
        self.printer.v = Vector(0, 0)
        while self.aquire_data:
            inputs.append(self.camera.camera.all_cell_values())
            outputs.append([self.printer.v.x, self.printer.v.y])
            self.act_and_refresh()
        self.aquire_data = True
        with open(outputfile, 'w') as output:
            writer = csv.writer(output)
            writer.writerow(camera_headers + output_headers)
            for inval, outval in zip(inputs, outputs):
                inval = [item for sublist in inval for item in sublist] #this shouldn't work but seems to?
                writer.writerow(inval + outval)

    def act_and_refresh(self):
            self.act_on_key_input()
            self.printer.simulate(1)
            self.redraw()
            pygame.display.update()

    def act_on_key_input(self):
        for event in pygame.event.get(pygame.KEYUP):
            if event.key == pygame.K_p:
                self.print_all_camera_values()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.printer.v.x += self.movement_constant * -1
        if keys[pygame.K_RIGHT]:
            self.printer.v.x += self.movement_constant
        if keys[pygame.K_UP]:
            self.printer.v.y += self.movement_constant * -1
        if keys[pygame.K_DOWN]:
            self.printer.v.y += self.movement_constant
        if keys[pygame.K_SPACE]:
            self.printer.v = Vector(0, 0)
        if keys[pygame.K_q]:
            self.aquire_data = False

    def redraw(self):
        self.gridworld.draw(self.window)
        self.printer.draw(self.window)
        self.camera.draw(self.window)


gen = Generator(ideal_grid = Grid(scale=60, path='square.test'))
gen.generate("output.out")
