from virtualprinter import VirtualPrinter
from camera import VisualCamera, Camera
from vector import Vector
from grid import Grid
from gridworld import GridWorld
from ann import Network
from ann_trainer import AnnTrainer
import pygame

import csv

camera_headers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
output_headers = ['x velocity', 'y velocity']

downsample_constant = 100

class AnnRunner:

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

    def run(self, n):
        self.printer.position = Vector(270, 150)
        while True:
            self.printer.setPenDown()
            actual = self.camera.camera.all_cell_values()
            ideal = self.ideal_camera.all_cell_values()
            pattern = [i - a for i,a in zip(actual, ideal)]
            result = n.propagate(pattern)
            result = [int(round(x)) for x in result]
            result = ''.join(map(str, result))
            self.printer.v = Vector(self.get_velocity(result[:2]), self.get_velocity(result[2:]))
            self.printer.simulate(1)
            self.redraw()
            pygame.display.update()

    def get_velocity(self, instruction):
        if instruction == "10":
            return -100
        elif instruction == "01":
            return 100
        else:
            return 0

    def redraw(self):
        self.gridworld.draw(self.window)
        self.printer.draw(self.window)
        self.camera.draw(self.window)
