import pygame
import math

from vector import Vector
from grid import Grid

class GridWorld:

        empty = 0
        filled = 1
        #use terrain type to index colors
        colors = [pygame.color.Color("white"),pygame.color.Color("blue")]
        #float("inf") returns infinity! (well not really)

        costs = [1,4,float("inf")]

        def __init__(self,wid,hi,scale):
            self.grid = Grid(wid, hi,scale)

        def draw(self,window):
                for row in xrange(0,self.grid.height):
                        for col in xrange(0,self.width()):
                                xcoord = col * self.gridsize()
                                ycoord = row * self.gridsize()
                                val_at_loc = self.grid.val_at(col, row)
                                color = self.colors[val_at_loc]

                                #actually draw the rectangle
                                dimen_of_rect = self.gridsize()
                                pygame.draw.rect(window, color, pygame.Rect(xcoord,ycoord,dimen_of_rect, dimen_of_rect))

        def inbounds(self,p):
          (x,y) = p
          return (x >= 0) and (x < self.width() * self.gridsize()) and (y >= 0) and (y < self.height() * self.gridsize())

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
