class Grid:

    empty = 0
    filled = 1

    def __init__(self,wid,hi,scale):
            self.width = wid
            self.height = hi
            self.gridsize = scale
            self.grid = [[self.empty for x in xrange(self.width)] for x in xrange(self.height)]

    def val_at(self, row, col):
        return self.grid[row][col]

    def set_loc_val(self, row, col, val):
        self.grid[col][row] = val

    def inbounds(self,p):
        (x,y) = p
        return (x >= 0) and (x < self.width*self.gridsize) and (y >= 0) and (y < self.height*self.gridsize)

    def find_closest_gridloc(self,p):
            '''given a point in (high resolution) game space, return the closest grid point'''
            x,y = p
            xval = int(x/self.gridsize)
            yval = int(y/self.gridsize)
            #print "endpoint is :",x,y, "(",xval,",",yval,")"
            return (xval,yval)
