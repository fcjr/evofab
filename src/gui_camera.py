from grid import Grid
from vector import Vector
from camera import Camera
from gui_printer import GuiPrinter
import pygame

class GuiCamera(Camera):
    """Visual wrapper on the camera class"""

    def __init__(self, grid, printer, n):
        super(GuiCamera, self).__init__(grid, printer, n)
        self.color = pygame.color.Color("black")

    def draw(self, window):
        topleft = self.get_top_left_camera_coords()
        for row in xrange(self.n + 1):
                #xcoord = (col * self.grid.gridsize) + self.get_top_left_camera_coords().x
                pygame.draw.line(window, pygame.color.Color("black"), (topleft.x, topleft.y + self.gridsize() * row), (topleft.x + self.gridsize() * self.n, topleft.y + self.gridsize() * row))
        for col in xrange(self.n + 1):
                pygame.draw.line(window, pygame.color.Color("black"), (topleft.x + self.gridsize() * col, topleft.y), (topleft.x + self.gridsize() * col, topleft.y + self.gridsize() * self.n))
