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
from printer import Printer

color = pygame.color.Color("darkorange")

class GuiPrinter(Printer):

    def __init__ (self, x, y, r, m, grid, move_units_per_cell):
        super(GuiPrinter, self).__init__(x, y, r, m, grid, move_units_per_cell)
        self.color = color
        
    def draw (self, window):
        pygame.draw.circle(window, self.color, (int(self.position.x),int(self.position.y)), self.r)
