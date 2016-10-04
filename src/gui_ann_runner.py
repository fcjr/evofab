from gui_printer import GuiPrinter
from gui_camera import GuiCamera
from grid import Grid
from vector import Vector
from gui_gridworld import GuiGridWorld
from ann_runner import AnnRunner
from ann import Network
import pygame

import csv

camera_size = 3

class GuiAnnRunner(AnnRunner):
    """Graphical ANN runner which sets up all of the relevant things needed to perform a graphical print with the GRAPHICAL simulated 3d printer"""

    def __init__(self, ideal_grid_path, cell_size, units_per_cell):
        """Sets up all the pieces needed to perform a print with the simulated 3d printer (controlled by the neural network). Takes in a path to an a ``goal'' or ``ideal'' grid, and constructs the GridWorld based on the dimensions of that goal grid. Understands both a ``camera'', which observes the actual world (around the print head) and an ``ideal camera'' which observes the same location but based on the ``goal grid''.
        
        This effectively duplicates work done in AnnRunner, but there is no better way to do it because we need to use the subclassed (GUI) versions of the simulation classes
        """

        ideal_grid = Grid(path=ideal_grid_path, scale=cell_size)
        self.ideal_grid = ideal_grid
        self.gridworld = GuiGridWorld(ideal_grid.width, ideal_grid.height, cell_size)
        self.gridworld.set_ideal_grid(ideal_grid)
        self.printer = GuiPrinter(10, 10, 9, self.gridworld, units_per_cell)
        self.camera = GuiCamera(self.gridworld.grid, self.printer, camera_size)
        self.ideal_camera = GuiCamera(self.gridworld.ideal_grid, self.printer, camera_size) #TODO: this might break -- might need a gridworld not a grid

        #gui stuff
        width = self.gridworld.width() * self.gridworld.gridsize()
        height = self.gridworld.height() * self.gridworld.gridsize()

        self.window = pygame.display.set_mode((width, height))
        pygame.init()

    def update(self):
        self.gridworld.draw(self.window)
        self.printer.draw(self.window)
        self.camera.draw(self.window)
        pygame.display.update()
