from grid import Grid
from vector import Vector
from virtualprinter import VirtualPrinter
import pygame

class VisualCamera:
    """Visual wrapper on the camera class"""

    def __init__(self, visual_grid, printer, n):
        self.color = pygame.color.Color("black")
        self.camera = Camera(visual_grid.grid, printer, n)

    def draw(self, window):
        topleft = self.camera.get_top_left_camera_coords()
        for row in xrange(self.camera.n + 1):
                #xcoord = (col * self.camera.grid.gridsize) + self.camera.get_top_left_camera_coords().x
                pygame.draw.line(window, pygame.color.Color("black"), (topleft.x, topleft.y + self.camera.gridsize() * row), (topleft.x + self.camera.gridsize() * self.camera.n, topleft.y + self.camera.gridsize() * row))
        for col in xrange(self.camera.n + 1):
                pygame.draw.line(window, pygame.color.Color("black"), (topleft.x + self.camera.gridsize() * col, topleft.y), (topleft.x + self.camera.gridsize() * col, topleft.y + self.camera.gridsize() * self.camera.n))

class Camera:
    """ Simulates a camera attached to the print head of the printer.
    It is defined in a grid, and does processing on each grid space to
    determine the percentage filled with material in that camera region.

    NOTE: don't be stupid and position the printer so that some of the
    camera regions are not in valid world cells. That's dumb and will
    break processing a lot. Make sure everythings inside the world grid"""

    def __init__(self, grid, printer, n):
        """constructs a Camera based on the given world grid,
        printer, and n (it is an n x n grid camera)"""

        self.grid = grid
        self.printer = printer
        self.n = n
        self.cell_width = grid.gridsize

    def gridsize(self):
        return self.grid.gridsize

    def num_cells_in_view(self, gridcell):
        """returns the number of cells in view of the given gridcell"""

        printer_position = self.printer.position
        top_left_camera_coords = printer_position.same_minus((self.cell_width * self.n) / 2.0)

        gridcell_pixel = gridcell.same_times(self.cell_width)
        topleft_cell_corner = top_left_camera_coords.plus(gridcell_pixel)
        topright_cell_corner = top_left_camera_coords.plus(Vector(gridcell_pixel.x + self.cell_width, gridcell_pixel.y))
        bottomleft_cell_corner = top_left_camera_coords.plus(Vector(gridcell_pixel.x, gridcell_pixel.y + self.cell_width))
        bottomright_cell_corner = top_left_camera_coords.plus(Vector(gridcell_pixel.x + self.cell_width, gridcell_pixel.y + self.cell_width))
        if topleft_cell_corner.x % self.cell_width == 0:
            if topleft_cell_corner.y % self.cell_width == 0:
                #then we are aligned with a cell
                return 1
            else:
                #then we are aligned on the x but not the y
                return 2
        else:
            if topleft_cell_corner.y % self.cell_width == 0:
                #then we are aligned on the y but not the x
                return 2
            else:
                return 4

    def get_top_left_camera_coords(self):
        printer_position = self.printer.position
        top_left_camera_coords = printer_position.same_minus((self.cell_width * self.n) / 2.0)
        return top_left_camera_coords

    def all_cell_values(self):
        output = [[self.percent_in_view(Vector(x, y)) for x in range(self.n)] for y in range(self.n)]
        return output

    def percent_in_view(self, gridcell):
        printer_position = self.printer.position
        top_left_camera_coords = printer_position.same_minus((self.cell_width * self.n) / 2.0)

        gridcell_pixel = gridcell.same_times(self.cell_width)
        topleft_cell_corner = top_left_camera_coords.plus(gridcell_pixel)
        topright_cell_corner = top_left_camera_coords.plus(Vector(gridcell_pixel.x + self.cell_width, gridcell_pixel.y))
        bottomleft_cell_corner = top_left_camera_coords.plus(Vector(gridcell_pixel.x, gridcell_pixel.y + self.cell_width))
        bottomright_cell_corner = top_left_camera_coords.plus(Vector(gridcell_pixel.x + self.cell_width, gridcell_pixel.y + self.cell_width))

        if topleft_cell_corner.x % self.cell_width == 0:
            if topleft_cell_corner.y % self.cell_width == 0:
                #then we are aligned with a cell
                cell_coords = topleft_cell_corner.same_times(1.0/self.cell_width)
                return self.grid.val_at(int(cell_coords.x), int(cell_coords.y))
            else:
                #then we are aligned on the x but not the y
                factor_top = (topright_cell_corner.y % self.cell_width) / float(self.cell_width)
                factor_bottom = self.cell_width - factor_top / float(self.cell_width)
                top_val = self.grid.val_at(*self.grid.find_closest_gridloc(topleft_cell_corner.get_tuple()))
                bottom_val = self.grid.val_at(*self.grid.find_closest_gridloc(bottomleft_cell_corner.get_tuple()))
                weighted_top_val = factor_top * top_val
                weighted_bottom_val = factor_bottom * bottom_val
                percentage_filled = weighted_top_val + weighted_bottom_val
                return percentage_filled
        else:
            if topleft_cell_corner.y % self.cell_width == 0:
                #then we are aligned on the y but not the x
                factor_left = (topright_cell_corner.x % self.cell_width) / float(self.cell_width)
                factor_right = self.cell_width - factor_left / float(self.cell_width)
                left_val = self.grid.val_at(*self.grid.find_closest_gridloc(topleft_cell_corner.get_tuple()))
                right_val = self.grid.val_at(*self.grid.find_closest_gridloc(topright_cell_corner.get_tuple()))
                weighted_left_val = factor_left * left_val
                weighted_right_val = factor_right * right_val
                percentage_filled = weighted_left_val + weighted_right_val
                return percentage_filled
            else:
                topleft_factor = self.get_4_cell_topleft_factor(topleft_cell_corner)
                topright_factor = self.get_4_cell_topright_factor(topright_cell_corner)
                bottomleft_factor = self.get_4_cell_bottomleft_factor(bottomleft_cell_corner)
                bottomright_factor = self.get_4_cell_bottomright_factor(bottomright_cell_corner)

                topleft_val = self.grid.val_at(*self.grid.find_closest_gridloc(topleft_cell_corner.get_tuple()))
                topright_val = self.grid.val_at(*self.grid.find_closest_gridloc(topright_cell_corner.get_tuple()))
                bottomleft_val = self.grid.val_at(*self.grid.find_closest_gridloc(bottomleft_cell_corner.get_tuple()))
                bottomright_val = self.grid.val_at(*self.grid.find_closest_gridloc(bottomright_cell_corner.get_tuple()))

                total_val = (
                        (topleft_val * topleft_factor)
                        + (topright_val * topright_factor)
                        + (bottomleft_val * bottomleft_factor)
                        + (bottomright_val * bottomright_factor)
                        )
                return total_val

    def get_4_cell_topleft_factor(self, topleft_cell_corner):
        distance_into_cell_x = topleft_cell_corner.x % self.cell_width
        xfactor = self.cell_width - distance_into_cell_x
        distance_into_cell_y = topleft_cell_corner.y % self.cell_width
        yfactor = self.cell_width - distance_into_cell_y
        topleft_factor = (xfactor * yfactor) / (self.cell_width * self.cell_width)
        return topleft_factor

    def get_4_cell_topright_factor(self, topright_cell_corner):
        xfactor = topright_cell_corner.x % self.cell_width
        distance_into_cell_y = topright_cell_corner.y % self.cell_width
        yfactor = self.cell_width - distance_into_cell_y
        topright_factor = (xfactor * yfactor) / (self.cell_width * self.cell_width)
        return topright_factor

    def get_4_cell_bottomleft_factor(self, bottomleft_cell_corner):
        distance_into_cell_x = bottomleft_cell_corner.x % self.cell_width
        xfactor = self.cell_width - distance_into_cell_x
        yfactor = bottomleft_cell_corner.y % self.cell_width
        bottomleft_factor = (xfactor * yfactor) / (self.cell_width * self.cell_width)
        return bottomleft_factor

    def get_4_cell_bottomright_factor(self, bottomright_cell_corner):
        xfactor = bottomright_cell_corner.x % self.cell_width
        yfactor = bottomright_cell_corner.y % self.cell_width
        bottomright_factor = (xfactor * yfactor) / (self.cell_width * self.cell_width)
        return bottomright_factor
