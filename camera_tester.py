from gridworld import GridWorld
from virtualprinter import VirtualPrinter
from camera import Camera
import pygame

#camera tester
the_grid = GridWorld(10, 10, 10)
printer = VirtualPrinter(15, 10, 1, 0, pygame.color.Color("darkorange"), the_grid)
camera = Camera(printer, the_grid.grid, 10)
print camera.get_cells_in_view((0, 0))
