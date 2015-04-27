
import pygame
import math

from vector import Vector

class GridWorld:

        empty = 0
        filled = 1
        wall = 1
        #use terrain type to index colors
        colors = [pygame.color.Color("white"),pygame.color.Color("blue")]
        #float("inf") returns infinity! (well not really)

        costs = [1,4,float("inf")]

        def __init__(self,wid,hi,scale):
                self.width = wid
                self.height = hi
                self.gridsize = scale
                #value at a grid location is the "terrain cost"
                self.grid = [[self.empty for x in xrange(self.width)] for x in xrange(self.height)]

        def handle_events(self,keymap):
                mpos = pygame.mouse.get_pos()
                x,y = self.find_closest_gridloc(mpos)
                if keymap.has_key(pygame.K_w) and keymap[pygame.K_w]:
                        self.grid[y][x] = self.wall                                 
                if keymap.has_key(pygame.K_m) and keymap[pygame.K_m]:
                        self.grid[y][x] = self.filled
                if keymap.has_key(pygame.K_g) and keymap[pygame.K_g]:
                        self.grid[y][x] = self.grass

        def draw(self,window):
                for row in range(0,self.height):
                        for col in range(0,self.width):
                                xcoord = col*self.gridsize
                                ycoord = row*self.gridsize
                                val_at_loc = self.grid[row][col]
                                color = self.colors[val_at_loc]
                                pygame.draw.rect(window,color ,pygame.Rect(xcoord,ycoord,self.gridsize,self.gridsize))

        def inbounds(self,p):
          (x,y) = p
          return (x >= 0) and (x < self.width*self.gridsize) and (y >= 0) and (y < self.height*self.gridsize)
                        
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

        def find_closest_gridloc(self,p):
                '''given a point in (high resolution) game space, return the closest grid point'''
                x,y = p
                xval = int(x/self.gridsize)
                yval = int(y/self.gridsize)
                #print "endpoint is :",x,y, "(",xval,",",yval,")"
                return (xval,yval)

        def PenDraw(self,p):
                myx,myy = self.find_closest_gridloc(p)
                self.grid[myy][myx] = self.filled
