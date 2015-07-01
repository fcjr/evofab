import pygame
import csv
from gridworld import GridWorld
from grid import Grid
from virtualprinter import VirtualPrinter
from camera import VisualCamera, Camera
from vector import Vector

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
        self.printer.position = Vector(150, 150)
        while self.aquire_data:
            actual = self.camera.camera.all_cell_values()
            ideal = self.ideal_camera.all_cell_values()
            inputs.append([i - a for a,i in zip(actual, ideal)]) #subtract actual and ideal TODO: check to make sure this line is doing what i think it is
            outputs.append([self.printer.v.x, self.printer.v.y])
            self.act_and_refresh()
        outputs = [[graycode[int(pair[0]/100) + 16] + graycode[int(pair[1]/100) + 16]] for pair in outputs] #TODO fix this
        self.aquire_data = True
        with open(outputfile, 'w') as output:
            writer = csv.writer(output)
            writer.writerow(camera_headers + output_headers)
            for inval, outval in zip(inputs, outputs):
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
gen.generate("output3.out")
