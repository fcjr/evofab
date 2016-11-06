from gui_printer import *
from gui_gridworld import GuiGridWorld
from grid import Grid
import pygame
from vector import Vector
from noise import *
import imp

def calculate_fitness(ideal_grid, actual_grid):
    """Calculate the fitness of this member of the population by first using it to control the 3d printer, and then evaluating the fitness of the output. Fitness is determined by how well the output from the printer matches the ``ideal/goal'' grids (paths specified in the populations.goal list)"""

    fitness = 0
    for ideal_row, actual_row in zip(ideal_grid, actual_grid):
        for ideal, actual in zip(ideal_row, actual_row):
            if ideal == 1 and actual == 1:
                fitness += 100
            elif ideal == 0 and actual == 1:
                fitness -= 30
    return fitness


def goXdistance(x):
        x = x * 15
        for i in range(x):
            printer.simulate()
            if gui:
                #redraw the grid and printer and update the display
                grid.draw(window)
                printer.draw(window)
                pygame.display.update()



def runSquare(noiseMaker):

    #make a 20x20 grid where each cell is 30 pixels
    g = Grid(scale=15, path="worlds/square.test")

    grid = noiseMaker.GenGridWorld(g.width, g.height, g.gridsize,0,0)

    #create the ideal grid
    grid.set_ideal_grid(g)

    #make a printer that is at location 0,0, is shown as a 15 pixel circle, it needs the grid, and it moves in 10*grid resolution
    printer = noiseMaker.GenPrinter(0,0, 15/2, grid, 10,.008,5,.01)
    #move printer to 4,4
    printer.set_position_on_grid(13,12)

    #pygame init shit
    if gui:
        window = pygame.display.set_mode((grid.width() * grid.gridsize(), grid.height() * grid.gridsize()))
        pygame.init()

    printer.setPenDown()

    printer.v = Vector(1,0)
    goXdistance(6)

    printer.v = Vector(0,1)
    goXdistance(4)

    printer.v = Vector(-1,0)
    goXdistance(6)

    printer.v = Vector(0,-1)
    goXdistance(4)

    if gui:
        pygame.quit()

    return calculate_fitness(g.grid,grid.grid.grid)

def runTriangle(noiseMaker,gui):
    #make a 20x20 grid where each cell is 30 pixels
    g = Grid(scale=15, path="worlds/triangle.test")

    grid = noiseMaker.GenGridWorld(g.width, g.height, g.gridsize,0,0)

    #create the ideal grid
    grid.set_ideal_grid(g)

    #make a printer that is at location 0,0, is shown as a 15 pixel circle, it needs the grid, and it moves in 10*grid resolution
    printer = noiseMaker.GenPrinter(0,0, 15/2, grid, 10,.008,5,.01)
    #move printer to 4,4
    printer.set_position_on_grid(13,12)

    #pygame init shit
    if gui:
        window = pygame.display.set_mode((grid.width() * grid.gridsize(), grid.height() * grid.gridsize()))
        pygame.init()

    printer.setPenDown()

    printer.v = Vector(1,1)
    goXdistance(8)

    printer.v = Vector(-1,0)
    goXdistance(8)

    printer.v = Vector(0,-1)
    goXdistance(8)

    if gui:
        pygame.quit()

    return calculate_fitness(g.grid,grid.grid.grid)

def main():

    gui = True
    generationSize = 10

    noiseMaker = NoisyFactory(gui)

    fitnesses = []

    for x in range(generationSize):
        fitnesses[x] = runSquare(noiseMaker,gui)

if __name__ == "__main__":
    main()
