import pygame
from gridworld import GridWorld

class GuiGridWorld(GridWorld):
    """A GUI GridWorld. Implements drawing of a GridWorld using PyGame"""

    colors = [pygame.color.Color("white"),pygame.color.Color("yellow"), pygame.color.Color("blue"), pygame.color.Color("red")]

    def draw(self,window):
        """Draw the GridWorld in the PyGame window"""
        for row in xrange(0,self.height()):
            for col in xrange(0,self.width()):
                xcoord = col * self.gridsize()
                ycoord = row * self.gridsize()
                val_at_loc = self.grid.val_at(col, row)
                val_at_ideal = self.ideal_grid.val_at(col, row)
                if val_at_loc == 0 and val_at_ideal == 0:
                    color = pygame.color.Color("white")
                elif val_at_loc == 0 and val_at_ideal == 1:
                    color = pygame.color.Color("yellow")
                elif val_at_loc == 1 and val_at_ideal == 1:
                    color = pygame.color.Color("blue")
                else:
                    color = pygame.color.Color("red")

                #actually draw the rectangle
                dimen_of_rect = self.gridsize()
                pygame.draw.rect(window, color, pygame.Rect(xcoord,ycoord,dimen_of_rect, dimen_of_rect))
        for row in xrange(0, self.height()):
            pygame.draw.line(window, pygame.color.Color("black"), (0, self.grid.gridsize * row), (self.grid.gridsize * self.width(), self.grid.gridsize * row))
        for col in xrange(0, self.width()):
            pygame.draw.line(window, pygame.color.Color("black"), (self.grid.gridsize * col, 0), (self.grid.gridsize * col, self.grid.gridsize * self.height()))
