##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## This character has an FMS that allows it to go back and forth
## between two states: waiting and following a given path. The path is
## specified as a sequence of points and the character uses seek
## behavior to get from one point to the next.
##

import pygame
from moving_ball_2d import MovingBall
from vector import Vector

class VirtualPrinter(MovingBall):

    def __init__ (self, x, y, r, m, color, grid):

        MovingBall.__init__(self, x, y, r, color, 0, 0)
        self.grid = grid
        self.penDown = False
        
    def move (self, dt):
        self.stop_v ()
        self.position = self.position.plus(self.v.times(float(dt)/1000))
              
    def setPenUp(self):
        self.penDown = False
        
    def setPenDown(self):
        self.penDown = True

    def simulate(self,dt):
        if self.move_is_valid(dt):
            self.move(dt)
            if self.penDown:
                position = (self.position.x, self.position.y)
                self.grid.PenDraw(position)

    def move_is_valid(self, dt):
        """ Checks if moving with the given dt will cause collision with
            the boundaries of the grid """
        new_loc = self.position.plus(self.v.times(float(dt)/1000))
        new_loc = (new_loc.x, new_loc.y)
        return self.grid.inbounds(new_loc)
