import pygame
from printer import Printer

color = pygame.color.Color("darkorange")

class GuiPrinter(Printer):
    """A GUI Printer. Understands how to draw itself in the Pygame window"""

    def __init__ (self, x, y, r, grid, move_units_per_cell):
        super(GuiPrinter, self).__init__(x, y, r, grid, move_units_per_cell)
        self.color = color
        
    def draw (self, window):
        pygame.draw.circle(window, self.color, (int(self.position.x),int(self.position.y)), self.r)
