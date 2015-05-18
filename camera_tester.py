from gridworld import GridWorld
from virtualprinter import VirtualPrinter
from camera import Camera
import pygame

#camera tester
the_grid = GridWorld(40, 40, 10)
the_grid.grid.set_loc_val(2, 1, 1)
printer = VirtualPrinter(20, 20, 1, 0, pygame.color.Color("darkorange"), the_grid)
camera = Camera(printer, the_grid.grid, 10)
print camera.get_cells_in_view((1, 1))
print camera.get_ratio_filled_in_view((1, 1))
