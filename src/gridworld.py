import pygame
import math

from vector import Vector
from grid import Grid

class GridWorld:

        filled = 1
        both_empty = 0
        need_fill = 1
        both_full = 2
        wrong_fill = 3

        #use terrain type to index colors
        colors = [pygame.color.Color("white"),pygame.color.Color("yellow"), pygame.color.Color("blue"), pygame.color.Color("red")]
        #float("inf") returns infinity! (well not really)

        costs = [1,4,float("inf")]

        def __init__(self,wid,hi,scale):
            self.grid = Grid(wid, hi,scale)

        def set_ideal_grid(self, grid):
            self.ideal_grid = grid

        def draw(self,window):
                for row in xrange(0,self.grid.height):
                        for col in xrange(0,self.width()):
                                xcoord = col * self.gridsize()
                                ycoord = row * self.gridsize()
                                val_at_loc = self.grid.val_at(col, row)
                                val_at_ideal = self.ideal_grid.val_at(col, row)
                                if val_at_loc == 0 and val_at_ideal == 0:
                                    color = self.colors[self.both_empty]
                                elif val_at_loc == 0 and val_at_ideal == 1:
                                    color = self.colors[self.need_fill]
                                elif val_at_loc == 1 and val_at_ideal == 1:
                                    color = self.colors[self.both_full]
                                else:
                                    color = self.colors[self.wrong_fill]

                                #actually draw the rectangle
                                dimen_of_rect = self.gridsize()
                                pygame.draw.rect(window, color, pygame.Rect(xcoord,ycoord,dimen_of_rect, dimen_of_rect))
                for row in xrange(0, self.width()):
                    pygame.draw.line(window, pygame.color.Color("black"), (0, self.grid.gridsize * row), (self.grid.gridsize * self.width(), self.grid.gridsize * row))
                for col in xrange(0, self.width()):
                    pygame.draw.line(window, pygame.color.Color("black"), (self.grid.gridsize * col, 0), (self.grid.gridsize * col, self.grid.gridsize * self.width()))

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
