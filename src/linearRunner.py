from evocontroller.evoPyLib.evoPyLib import *
from evocontroller.evoCamera.evoCamera import EvoCamera
import datetime
import csv
import sys,os,errno,getopt
import numpy as np
import argparse

#debugging setup
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class Debugger:
    def __init__(self):
        self.debug = False
    def debugOn(self):
        self.debug = True
    def debugOff(self):
        self.debug = False
    def debug(self,toPrint):
        if self.debug:
            print toPrint

#helper functions
def calculate_simulation_fitness(ideal_grid, actual_grid):
    """Calculate the fitness of this member of the population by first using it to control the 3d printer, and then evaluating the fitness of the output. Fitness is determined by how well the output from the printer matches the ``ideal/goal'' grids (paths specified in the populations.goal list)"""

    fitness = 0
    for ideal_row, actual_row in zip(ideal_grid, actual_grid):
        for ideal, actual in zip(ideal_row, actual_row):
            if ideal == 1 and actual == 1:
                fitness += 100
            elif ideal == 0 and actual == 1:
                fitness -= 30
    return fitness

def goXdistance(x,printer,gui,window,grid):
        x = x * 15
        for i in range(x):
            printer.simulate()
            if gui:
                #redraw the grid and printer and update the display
                grid.draw(window)
                printer.draw(window)
                pygame.display.update()


def square(printer,gui,window,grid):
        print "START"
        printer.setPenDown()

        print "LEFT"
        printer.set_printer_direction(1,0)
        goXdistance(6,printer,gui,window,grid)

        print "DOWN"
        printer.set_printer_direction(0,1)
        goXdistance(4,printer,gui,window,grid)

        print "RIGHT"
        printer.set_printer_direction(-1,0)
        goXdistance(6,printer,gui,window,grid)

        print "UP"
        printer.set_printer_direction(0,-1)
        goXdistance(4,printer,gui,window,grid)

        print "DONE"
        printer.setPenUp()

# sub-command functions
def physical(args):
    from physicalModels import PhysicalPrinter,PhysicalCamera
    print args.verbose
    printer = PhysicalPrinter(args.printerport,.1)
    camera = PhysicalCamera(args.cameraport)
    try:
        square(printer,False,None,None)
    except KeyboardInterrupt:
        pass
    printer.close()
    camera.close()


def simulation(args):
    if args.gui:
        global pygame
        import pygame
    from noise import NoisyFactory
    from grid import Grid
    noiseMaker = NoisyFactory(args.gui)
    #make a 20x20 ggrid where each cell is 30 pixels
    g = Grid(scale=15, path="worlds/square.test")

    grid = noiseMaker.GenGridWorld(g.width, g.height, g.gridsize,0,0)

    #create the ideal grid
    grid.set_ideal_grid(g)

    #make a printer that is at location 0,0, is shown as a 15 pixel circle, it needs the grid, and it moves in 10*grid resolution
    printer = noiseMaker.GenPrinter(0,0, 15/2, grid, 10,.008,5,.01)
    #move printer to 4,4
    printer.set_position_on_grid(13,12)

    #pygame init shit
    if args.gui:
        window = pygame.display.set_mode((grid.width() * grid.gridsize(), grid.height() * grid.gridsize()))
        pygame.init()

    #run test
    if args.gui:
        square(printer,args.gui,window,grid)
    else:
        square(printer,args.gui,None,None)

    if args.gui:
        pygame.quit()

    print calculate_simulation_fitness(g.grid,grid.grid.grid)



def main():
    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the "physical" command
    parser_physical = subparsers.add_parser('physical')
    parser_physical.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
    parser_physical.add_argument("-p", "--printerport", help="Port for the Printer Controller",required = True)
    parser_physical.add_argument("-c", "--cameraport", help="Port for the Camera Array",required = True)
    parser_physical.add_argument("-t", "--task",choices=["square","triangle"],help="choose the task to evaluate",default = "square")
    parser_physical.add_argument("-r", "--runs", help="number of runs",type=int,default=1)
    parser_physical.add_argument("-o", "--outfile", help="File to save ouput fitnesses in",required = True)
    #set physical function
    parser_physical.set_defaults(func=physical)

    # create the parser for the "simulation" command
    parser_simulation = subparsers.add_parser('simulate')
    parser_simulation.add_argument("-g", "--gui", help="Run with pygame gui",
                    action="store_true")
    #parser_simulation.add_argument('z')
    parser_simulation.set_defaults(func=simulation)

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
