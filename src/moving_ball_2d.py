##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## This file defines a ball class that can move in two dimensions and
## can bounce off other balls. It also bounces off the edges of the
## screen.

import pygame
import math

from vector import Vector

class MovingBall :

    r = 25

    #velocity vector

    speedlimit = Vector(100.0, 100.0) 

    color = pygame.color.Color('darkgreen')

    def __init__ (self, x, y, r, color, xv, yv):
        self.position = Vector(float(x), float(y))
        self.r = r
        self.color = color
        self.v = Vector(float(xv),float(yv))

    def stop_v (self):
        """ Reset the velocity to 0 if it gets very close. """

        if self.v.length() < 3:
            self.v = Vector (0,0)
        
    def draw (self, window):
        pygame.draw.circle(window, self.color, (int(self.position.x),int(self.position.y)), self.r)
