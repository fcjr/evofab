##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## A very simple vector class.

import math

class Vector:

    x = 0
    y = 0

    def __init__ (self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__ (self):
        return "["+str(self.x)+", "+str(self.y)+"]"

    def plus (self, v2):
        return Vector(self.x + v2.x, self.y + v2.y)

    def minus (self, v2):
        return Vector(self.x - v2.x, self.y - v2.y)

    def times (self, scalar):
        return Vector(self.x*scalar, self.y*scalar)

    def length (self):
        """ Length of the vector in pixels.
        """
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        """ Make the vector be one unit in length. [Old: I am using 10
        pixels as my unit.]
        """
        #l = float(self.length())/10
        l = float(self.length())
        if l != 0:
            return Vector (self.x/l, self.y/l)
        else:
            return Vector(0,0)

    def dot (self, v2):
        """
        The dot product.
        """
        return self.x * v2.x + self.y * v2.y

    def cross(self,other):
        return (self.x*other.y) - (self.y*other.x)

    def equals(self,other):
        return (self.x == other.x) and (self.y == other.y)

    def orthog(self):
        n = self.normalize()
        return Vector(n.y,-n.x)

        
