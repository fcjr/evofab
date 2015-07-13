import pygame
import csv
from gridworld import GridWorld
from grid import Grid
from virtualprinter import VirtualPrinter
from camera import VisualCamera, Camera
from vector import Vector
import sys

camera_headers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
output_headers = ['x velocity y velocity']

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
        self.ideal_camera = Camera(self.gridworld.ideal_grid, self.printer, 3)
        
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
        self.printer.position = Vector(250, 180)
        while self.aquire_data:
            actual = self.camera.camera.all_cell_values()
            ideal = self.ideal_camera.all_cell_values()
            inputs.append([i - a for a,i in zip(actual, ideal)])
            outputs.append([self.printer.v.x, self.printer.v.y])
            self.act_and_refresh()
        inputs = [thing for thing in inputs[::10]]
        outputs = [[self.encode(x) + self.encode(y)] for x,y in outputs[::100]]
        self.aquire_data = True
        with open(outputfile, 'w') as output:
            writer = csv.writer(output)
            writer.writerow(camera_headers + output_headers)
            for inval, outval in zip(inputs, outputs):
                writer.writerow(inval + outval)

    def encode(self, velocity):
        if velocity >= 100:
            return "01"
        elif velocity <= -100:
            return "10"
        else:
            return "00"

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
            self.printer.v = Vector(-100, 0)
        if keys[pygame.K_RIGHT]:
            self.printer.v = Vector(100, 0)
        if keys[pygame.K_UP]:
            self.printer.v = Vector(0, -100)
        if keys[pygame.K_DOWN]:
            self.printer.v = Vector(0, 100)
        if keys[pygame.K_SPACE]:
            self.printer.v = Vector(0, 0)
        if keys[pygame.K_q]:
            self.aquire_data = False

    def redraw(self):
        self.gridworld.draw(self.window)
        self.printer.draw(self.window)
        self.camera.draw(self.window)

grid = sys.argv[1]
outputfile = sys.argv[2]
gen = Generator(ideal_grid = Grid(scale=60, path=grid))
gen.generate(outputfile)
