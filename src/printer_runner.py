import pygame
from gridworld import GridWorld
from grid import Grid
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
        ideal_grid = Grid(20, 20, 30)
        ideal_grid.grid = [[1 if x <= 10 else 0 for x in range(20)] for _ in range(20)]
        grid.set_ideal_grid(ideal_grid)
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

    def run_auto(self):
        printer = self.printer
        printer.setPenDown()
        printer.position = Vector(45, 45)
        printer.v = Vector(500, 0)
        while printer.position.x < ((self.grid.width() - 2) * self.grid.gridsize() - 15):
            self.printer.simulate(1)
            self.redraw()
            pygame.display.update()
        printer.v = Vector(0, 500)
        while printer.position.y < ((self.grid.height() -2) * self.grid.gridsize() - 15):
            self.printer.simulate(1)
            self.redraw()
            pygame.display.update()
        printer.v = Vector(-500, 0)
        while printer.position.x > ((2 * self.grid.gridsize()) + 15):
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

    def print_all_camera_values(self):
        val_matrix = self.camera.camera.all_cell_values()
        for row in val_matrix:
            output = ''
            for val in row:
                output += str(val) + ' '
            print output
        print '*' * 10

    def redraw(self):
        self.grid.draw(self.window)
        self.printer.draw(self.window)
        self.camera.draw(self.window)

runner = Runner()
runner.run()
