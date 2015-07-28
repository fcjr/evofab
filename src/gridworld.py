import math

from vector import Vector
from grid import Grid

class GridWorld(object):

        filled = 1
        both_empty = 0
        need_fill = 1
        both_full = 2
        wrong_fill = 3

        def __init__(self,wid,hi,scale):
            self.grid = Grid(wid, hi,scale)

        def set_ideal_grid(self, grid):
            self.ideal_grid = grid

        def inbounds(self,p):
            return self.grid.inbounds(p)

        def width(self):
            return self.grid.width

        def height(self):
            return self.grid.height

        def gridsize(self):
            return self.grid.gridsize

        def PenDraw(self,p):
                myx,myy = self.grid.find_closest_gridloc(p)
                self.grid.set_loc_val(myx, myy, self.filled)

        #shouldn't need these for now -- might be useful later?
        def distance(self,startp,endp):
                (endx,endy) = endp
                (startx,starty) = startp
                return math.sqrt(pow(endx - startx,2) + pow(endy - starty,2))
                                  
        def manhattan(self,startp,endp):
                (endx,endy) = endp
                (startx,starty) = startp
                '''given two points, return manhattan distance of two points'''
                return (abs(endx - startx) + abs(endy - starty))
        
        def estimate_distance(self,start,end):
                 #return self.manhattan(start,end)
                 return self.distance(start,end)
