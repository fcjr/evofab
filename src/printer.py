from vector import Vector

class Printer:

    def __init__ (self, x, y, r, m, grid, xv=0, yv=0):
        self.position = Vector(float(x), float(y))
        self.r = r
        self.v = Vector(float(xv),float(yv))
        self.grid = grid
        self.penDown = False

    def stop_v (self):
        """ Reset the velocity to 0 if it gets very close. """
        if self.v.length() < 3:
            self.v = Vector (0,0)
        
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
