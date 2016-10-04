
class Grid:
    """Operates as an nxm binary grid"""

    empty = 0
    filled = 1

    def __init__(self,wid=None,hi=None,scale=None, path=None):
        """A grid can either be constructed with dimensions and a scale or a scale and a path.
        For the real canvas, we likely do not want anything to initially be drawn on the grid. In that case, use the first construction option.
        However, if we are contructing a ``goal'' grid to add to a GridWorld, we likely want to load it from a file. In that case, we load it from a file by specifying scale and path.
        Specs for grid files are given in ``load_grid_from_file''"""

        self.starting_point = None
        if not scale:
            #you have to provide a scale and if you don't this should break things
            assert(1 == 2) #TODO: do this with an exception
        if path:
            self.grid = self.load_grid_from_file(path)
            grid = self.grid
            self.height = len(grid)
            self.width = len(grid[0])
            self.gridsize = scale
        else:
            self.width = wid
            self.height = hi
            self.gridsize = scale
            self.grid = [[self.empty for x in xrange(self.width)] for x in xrange(self.height)]

    def load_grid_from_file(self, path):
        """Constructs a grid by loading it from a grid file. A grid file is a text file containing a rectangle of 0s, 1s, and a single ``S''. ``S'' denotes a starting point and can be used to provide information for where a printer should begin drawing for a test run"""

        grid = []
        with open(path, 'r') as to_read:
            y = 0
            for line in to_read:
                grid.append([])
                x = 0
                for char in line.strip():
                    if char == 'S':
                        self.starting_point = (x, y)
                        grid[-1].append(0)
                    else:
                        grid[-1].append(int(char))
                    x += 1
                y += 1
        return grid

    def val_at(self, x, y):
        """Returns the value at the specified location in the grid"""
        return self.grid[y][x]

    def val_at_vector(self, vector):
        """Returns the value at the specified location in the grid as given by a vector"""
        return self.grid[vector.x][vector.y]

    def set_loc_val(self, x, y, val):
        """Sets the value at the specified grid location"""
        self.grid[y][x] = val

    def inbounds(self,p):
        """Takes a pair giving a pixel location. If that pixel location is in the bounds of the grid (does not enter the perimeter cells of the grid), returns True. Otherwise, returns False"""
        (x,y) = p
        return (x > 1.5 * self.gridsize) and (x < (self.width - 1.5) * self.gridsize) and (y > 1.5 * self.gridsize) and (y < (self.height - 1.5) * self.gridsize)

    def find_closest_gridloc(self,p):
        """Determines the closest grid location (in grid space) to the given pixel coordinates"""
        x,y = p
        xval = int(x/self.gridsize)
        yval = int(y/self.gridsize)
        #print "endpoint is :",x,y, "(",xval,",",yval,")"
        return xval,yval
