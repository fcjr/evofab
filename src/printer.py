from vector import Vector

class Printer(object):

    def __init__ (self, x, y, r, m, grid, move_units_per_cell):
        self.position = Vector(float(x), float(y))
        self.r = r
        move_unit_pixels = grid.gridsize() / move_units_per_cell
        self.v = Vector(move_unit_pixels, move_unit_pixels)
        self.grid = grid
        self.penDown = False

    def set_position_on_grid(self, xcell, ycell):
        self.position = Vector((xcell * self.grid.gridsize()) + self.grid.gridsize()/2, (ycell * self.grid.gridsize())+ self.grid.gridsize()/2)

    def move (self):
        self.position = self.position.plus(self.v)
              
    def setPenUp(self):
        self.penDown = False
        
    def setPenDown(self):
        self.penDown = True

    def simulate(self):
        if self.move_is_valid():
            self.move()
            if self.penDown:
                position = (self.position.x, self.position.y)
                self.grid.PenDraw(position)

    def move_is_valid(self):
        """ Checks if moving with the given dt will cause collision with
            the boundaries of the grid """
        new_loc = self.position.plus(self.v)
        new_loc = (new_loc.x, new_loc.y)
        return self.grid.inbounds(new_loc)
