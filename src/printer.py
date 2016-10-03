from vector import Vector

class Printer(object):
    """A simple model of a 2d 3d-printer. Can draw in a GridWorld"""

    def __init__ (self, x, y, r, grid, sub_cell_resolution):
        """Constructs a printer which draws in a GridWorld and moves in increments of fractions of cell widths

        x: the x coordinate for the printer start position
        y: the y coordinate for the printer start position
        r: the radius of the printer (does not influence how the printer prints, only the way it is represented if drawn visually)
        grid: the gridworld that the printer can act upon
        sub_cell_resolution: the factor by which cell width is divided by to determine the distance moved by the printer in a single time unit
        """

        self.position = Vector(float(x), float(y))
        self.r = r
        move_unit_pixels = grid.gridsize() / sub_cell_resolution
        self.v = Vector(move_unit_pixels, move_unit_pixels)
        self.grid = grid
        self.penDown = False

    def set_printer_direction(self, leftright, updown):
        """Set the direction the printer will move in on the following time steps.

        leftright: -1 = left motion, 0 = no leftright motion, 1 = right motion
        updown: -1 = down motion, 0 = no updown motion, 1 = up motion"""
        self.v = Vector(leftright, updown)

    def set_position_on_grid(self, xcell, ycell):
        """ Move the printer to the specified cell position on the grid"""
        self.position = Vector((xcell * self.grid.gridsize()) + self.grid.gridsize()/2, (ycell * self.grid.gridsize())+ self.grid.gridsize()/2)

    def setPenUp(self):
        self.penDown = False
        
    def setPenDown(self):
        self.penDown = True

    def simulate(self):
        """Simulate a single time unit for the printer (which will be moving in a particular direction and may or may not have the pen down"""
        if self.move_is_valid():
            self.position = self.position.plus(self.v)
            if self.penDown:
                position = (self.position.x, self.position.y)
                self.grid.PenDraw(position)

    def move_is_valid(self):
        """ Checks if moving with the given dt will cause collision with the boundaries of the grid """
        new_loc = self.position.plus(self.v)
        new_loc = (new_loc.x, new_loc.y)
        return self.grid.inbounds(new_loc)
