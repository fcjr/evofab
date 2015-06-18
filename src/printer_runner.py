import pygame
from gridworld import GridWorld
from virtualprinter import VirtualPrinter
from camera import VisualCamera
from vector import Vector

class Runner:
    """Runner for printer test"""

    movement_constant = 3

    def __init__(self):
        """ Set pygame stuff up for running the simulation."""

        pygame.init()
        grid = GridWorld(20, 20, 30)
        width = grid.width() * grid.gridsize()
        height = grid.height() * grid.gridsize()
        self.grid = grid
        self.window = pygame.display.set_mode((width, height))
        self.printer = VirtualPrinter(10, 10, 9, 1, pygame.color.Color("darkorange"), grid)
        self.camera = VisualCamera(self.grid, self.printer, 3)
        self.grid.draw(self.window)

    def run(self):
        self.printer.setPenDown()
        self.printer.v = Vector(0, 0)
        while (True):
            self.act_on_key_input()
            self.printer.simulate(1)
            self.redraw()
            pygame.display.update()

    def act_on_key_input(self):
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.printer.v.x += self.movement_constant * -1
        if keys[pygame.K_RIGHT]:
            self.printer.v.x += self.movement_constant
        if keys[pygame.K_UP]:
            self.printer.v.y += self.movement_constant * -1
        if keys[pygame.K_DOWN]:
            self.printer.v.y += self.movement_constant

    def redraw(self):
        self.grid.draw(self.window)
        self.printer.draw(self.window)
        self.camera.draw(self.window)

runner = Runner()
runner.run()
