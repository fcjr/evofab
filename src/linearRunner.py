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

def Debugger:
    def __init__(self):
        self.debug = False
    def debugOn(self):
        self.debug = True
    def debugOff(self):
        self.debug = False
    def print(self,toPrint):
        if self.debug:
            print toPrint
    def fprintf(self,*arg):
        if self.debug:
            fprintf(*args)



# sub-command functions
def physical(args):
    from physicalModels import PhysicalPrinter,PhysicalCamera
    print args.verbose
    printer = PhysicalPrinter(args.printerport,2)
    camera = PhysicalCamera(args.cameraport)
    try:
        pass#TODO
    except KeyboardInterrupt:
        pass
    printer.close()
    camera.close()


def simulation(args):
    from noise.py import NoisyFactory
    #TODO implement simulation

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
    parser_physical.add_argument("")
    #set physical function
    parser_physical.set_defaults(func=physical)

    # create the parser for the "simulation" command
    parser_simulation = subparsers.add_parser('simulate')
    parser_physical.add_argument("-g", "--gui", help="Run with pygame gui",
                    action="store_true")
    #parser_simulation.add_argument('z')
    parser_simulation.set_defaults(func=simulation)

    # parse the args and call whatever function was selected
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
