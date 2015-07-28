from gui_printer import GuiPrinter
from gui_camera import GuiCamera
from vector import Vector
from gui_gridworld import GuiGridWorld
from ann_runner import AnnRunner
from ann import Network
import pygame

import csv

camera_size = 3

class GuiAnnRunner(AnnRunner):

    def __init__(self, ideal_grid):
        self.gridworld = GuiGridWorld(ideal_grid.width, ideal_grid.height, ideal_grid.gridsize)
        self.gridworld.set_ideal_grid(ideal_grid)
        self.printer = GuiPrinter(10, 10, 9, 1, self.gridworld)
        self.camera = GuiCamera(self.gridworld.grid, self.printer, camera_size)
        self.ideal_camera = GuiCamera(self.gridworld.ideal_grid, self.printer, camera_size) #TODO: this might break -- might need a gridworld not a grid
        width = self.gridworld.width() * self.gridworld.gridsize()
        height = self.gridworld.height() * self.gridworld.gridsize()

        #gui stuff
        self.window = pygame.display.set_mode((width, height))
        pygame.init()

    def update(self):
        self.gridworld.draw(self.window)
        self.printer.draw(self.window)
        self.camera.draw(self.window)
        pygame.display.update()
