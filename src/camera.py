from grid import Grid
from vector import Vector
from virtualprinter import VirtualPrinter

class Camera:
    """ Simulates a camera attached to the print head of the printer.
    It is defined in a grid, and does processing on each grid space to
    determine the percentage filled with material in that camera region.

    NOTE: don't be stupid and position the printer so that some of the
    camera regions are not in valid world cells. That's dumb and will
    break processing a lot. Make sure everythings inside the world grid"""

    def __init__(self, world_grid, printer, n):
        """constructs a Camera based on the given world grid,
        printer, and n (it is an n x n grid camera)"""

        self.world_grid = world_grid
        self.printer = printer
        self.n = n
        self.cell_width = world_grid.gridsize

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
