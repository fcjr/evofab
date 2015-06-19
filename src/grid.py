def load_grid_from_file(path):
    grid = []
    with open(path, 'r') as to_read:
        for line in to_read:
            grid.append([])
            for char in line.strip():
                grid[-1].append(int(char))
    return grid

class Grid:
    """Operates as a grid with values"""

    empty = 0
    filled = 1

    def __init__(self,wid=None,hi=None,scale=None, path=None):
        """can either be constructed with a width, height, and scale (init to empty)
        or with a scale and a path"""
        if not scale:
            #you have to provide a scale and if you don't this should break things
            assert(1 == 2) #TODO: do this with an exception
        if path:
            self.grid = load_grid_from_file(path)
            grid = self.grid
            self.height = len(grid)
            self.width = len(grid[0])
            self.gridsize = scale
        else:
            self.width = wid
            self.height = hi
            self.gridsize = scale
            self.grid = [[self.empty for x in xrange(self.width)] for x in xrange(self.height)]

    def val_at(self, x, y):
        return self.grid[x][y]

    def val_at_vector(self, vector):
        return self.grid[vector.x][vector.y]

    def set_loc_val(self, x, y, val):
        self.grid[x][y] = val

    def inbounds(self,p):
        (x,y) = p
        return (x >= 0) and (x < self.width*self.gridsize) and (y >= 0) and (y < self.height*self.gridsize)

    #TODO: this shouldn't be here. should be in the visual grid. same with `scale` variable
    def find_closest_gridloc(self,p):
            '''given a point in (high resolution) game space, return the closest grid point'''
            x,y = p
            xval = int(x/self.gridsize)
            yval = int(y/self.gridsize)
            #print "endpoint is :",x,y, "(",xval,",",yval,")"
            return xval,yval
