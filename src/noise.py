from grid import Grid
from vector import Vector
from camera import Camera
import random
from printer import Printer
from gridworld import GridWorld


class NoisyFactory:
    def __init__(self,gui):
        self.gui = gui


    def GenGridWorld(self,wid,hi,scale,penNoise,penNoiseChance):
        if self.gui:
            from gui_gridworld import GuiGridWorld
            from gui_printer import GuiPrinter

        class _NoisyGridWorld(GuiGridWorld if self.gui else GridWorld):
            def __init__(self,wid,hi,scale,penNoise,penNoiseChance,gui):
                if gui:
                    GuiGridWorld.__init__(self,wid,hi,scale)
                else:
                    GridWorld.__init__(self,wid,hi,scale)
                self.penNoise = penNoise
                self.penNoiseChance = penNoiseChance

            def PenDraw(self,p):
                #based on noise chance do:
                if random.random() < self.penNoiseChance:
                    # unpack pen location
                    (x,y) = p
                    #choose random numbers for p +/- penNoise
                    newX = random.randrange(x-self.penNoise,x+self.penNoise)
                    newY = random.randrange(y-self.penNoise,y+self.penNoise)
                    p = (newX,newY)
                super(_NoisyGridWorld,self).PenDraw(p)


        return _NoisyGridWorld(wid,hi,scale,penNoise,penNoiseChance,self.gui)

    def GenPrinter(self, x, y, r, grid, sub_cell_resolution, dragChance,penNoise,penNoiseChance):
        if self.gui:
            from gui_gridworld import GuiGridWorld
            from gui_printer import GuiPrinter

        class _NoisyPrinter(GuiPrinter if self.gui else Printer):
            def __init__ (self, x, y, r, grid, sub_cell_resolution, dragChance,penNoise,penNoiseChance,gui):
                if gui:
                    GuiPrinter.__init__(self, x, y, r, grid, sub_cell_resolution)
                else:
                    Printer.__init__(self, x, y, r, grid, sub_cell_resolution)
                self.dragChance = dragChance
                self.lastPlace = (0,0)
                self.doDrag = True
                self.penNoise = penNoise
                self.penNoiseChance = penNoiseChance

            def get_cur_grid_coords(self):
                return self.grid.find_closest_gridloc((self.position.x, self.position.y))

            def shiftForeword(self):
                if self.v.x ==  -1: #LEFT
                    self.shiftLeft()
                if self.v.x == 1: #RIGHT
                    self.shiftRight()
                if self.v.y == 1: #UP
                    self.shiftUp()
                if self.v.y == -1: #DOWN
                    self.shiftDown()

            def shiftLeft(self):
                height = self.grid.grid.height
                for x in range(height):
                    self.grid.grid.grid[x] = self.shift(self.grid.grid.grid[x],-1)


            def shiftRight(self):
                height = self.grid.grid.height
                for x in range(height):
                    self.grid.grid.grid[x] = self.shift(self.grid.grid.grid[x],1)

            def shiftUp(self):
                self.grid.grid.grid = self.shift(self.grid.grid.grid,1)
                # height = self.grid.grid.height
                # for i in range(height):
                #     temp = self.grid.grid.grid[i];
                #     self.grid.grid.grid[i] = self.grid.grid.grid[i+1]
                #     self.grid.grid.grid[i+1] = temp

            def shiftDown(self):
                self.grid.grid.grid = self.shift(self.grid.grid.grid,-1)
                    # height = self.grid.grid.height
                    # for i in reversed(xrange(height)):
                    #     temp = self.grid.grid.grid[i];
                    #     self.grid.grid.grid[i] = self.grid.grid.grid[i-1]
                    #     self.grid.grid.grid[i-1] = temp

            def shift(self, seq, n=0):
                a = n % len(seq)
                return seq[-a:] + seq[:-a]

            def simulate(self):

                #based on noise chance do:
                if random.random() < self.penNoiseChance:
                    #choose random numbers for p +/- penNoise
                    newX = random.randrange(self.position.x-self.penNoise,self.position.x+self.penNoise)
                    newY = random.randrange(self.position.y-self.penNoise,self.position.y+self.penNoise)

                    self.position = Vector(newX,newY)



                if self.lastPlace != self.get_cur_grid_coords():
                    self.lastPlace = self.get_cur_grid_coords()
                    self.doDrag = True
                if random.random() < self.dragChance and self.doDrag:
                    self.shiftForeword()
                    self.doDrag = False
                super(_NoisyPrinter,self).simulate()

        return _NoisyPrinter(x, y, r, grid, sub_cell_resolution, dragChance,penNoise,penNoiseChance,self.gui)

    def GenCamera(self, grid, printer, n,noiseChance,noiseRange):
        class _NoisyCamera(Camera):
            def __init__(self, grid, printer, n,noiseChance,noiseRange,gui):
                Camera.__init__(self, grid, printer, n)
                self.noiseChance = noiseChance
                self.noiseRange = noiseRange

            def percent_inView(self,gridcell):
                realVal = super(_NoisyCamera,self).percent_inView(self,grid)
                if random.random() < self.nosieChance:
                    return random.randrange(realVal-self.noiseRange,realVal+self.noiseRange)
                else:
                    return realVal

        return _NoisyCamera(grid, printer, n,noiseChance,noiseRange,self.gui)
