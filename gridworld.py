
import pygame
import math

from vector import Vector

class GridWorld:


        gravity = Vector(0,10) #useless here, but required for compatability
        grass = 0
        water = 1
        wall = 1
        #use terrain type to index colors
        colors = [pygame.color.Color("white"),pygame.color.Color("blue"),pygame.color.Color("black")]
        #float("inf") returns infinity! (well not really)

        costs = [1,4,float("inf")]


        def __init__(self,wid,hi,scale):

                self.width = wid
                self.height = hi
                self.gridsize = scale
                #value at a grid location is the "terrain cost"
                self.grid = [[self.grass for x in xrange(self.width)] for x in xrange(self.height)]

                

        def handle_events(self,keymap):
                mpos = pygame.mouse.get_pos()
                x,y = self.find_closest_gridloc(mpos)
                if keymap.has_key(pygame.K_w) and keymap[pygame.K_w]:
                        self.grid[y][x] = self.wall                                 
                if keymap.has_key(pygame.K_m) and keymap[pygame.K_m]:
                        self.grid[y][x] = self.water
                if keymap.has_key(pygame.K_g) and keymap[pygame.K_g]:
                        self.grid[y][x] = self.grass
                   
            

                

        def draw(self,window):
                window.fill(pygame.color.Color("green"))
                for row in range(0,self.height):
                        for col in range(0,self.width):
                                xcoord = col*self.gridsize
                                ycoord = row*self.gridsize
                                terrain = self.grid[row][col]
                                groundcolor = self.colors[terrain]
                                pygame.draw.rect(window,groundcolor,pygame.Rect(xcoord,ycoord,self.gridsize,self.gridsize))


        def inbounds(self,p):
          (x,y) = p
          return (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height)
                  

        def isLegitimate(self,p):
                (x,y) = p
                '''if out of bounds or wall, return false'''
                if self.inbounds(p):
                        return self.grid[int(y)][int(x)] != self.wall
                else:
                        return False
                        

        def valueAtPoint(self,p):
                '''return the terrain cost of a point in the grid'''
                (x,y) = p
                if self.inbounds(p):
                        index = self.grid[int(y)][int(x)]
                        return self.costs[index]
                else:
                        return None

        def neighbors(self,p):
                '''given a point p, return a vector of all the neighboring points'''
                (x,y) = p
                outvec = []
                north = (x,y - 1)
                south = (x,y + 1)
                east = (x + 1, y)
                west = (x - 1,y)
                coords = [north,south,east,west]
                #only put something in the outvec if it is a legitimate point
                #i.e. don't return walls or out-of-bounds
                outvec = [loc for loc in coords if self.isLegitimate(loc)]
                return outvec



        def distance(self,startp,endp):
                (endx,endy) = endp
                (startx,starty) = startp

                return math.sqrt(pow(endx - startx,2) + pow(endy - starty,2))
                                  
        def manhattan(self,startp,endp):
                (endx,endy) = endp
                (startx,starty) = startp
                '''given two points, return manhattan distance of two points'''
                return (abs(endx - startx) + abs(endy - starty))
        
        def estimate_distance(self,start,end):
#                return self.manhattan(start,end)
                 return self.distance(start,end)

        def find_closest_gridloc(self,p):
                '''given a point in (high resolution) game space, return the closest grid point'''
                x,y = p
                xval = int(x/self.gridsize)
                yval = int(y/self.gridsize)
                #print "endpoint is :",x,y, "(",xval,",",yval,")"
                return (xval,yval)

        def PenDraw(self,p):
                myx,myy = self.find_closest_gridloc(p)
                self.grid[myy][myx] = self.wall
                print "penDraw", p, myx, myy

        def xOr(self, x, y):
                if x==y:
                        return 0
                else:
                        return 1


        def convertGray(self, n):
                arrBin = [0 for i in range(4)]
                i = 3 
                while i>=0:
                       if pow(2, i) < n:
                               arrBin[i] = 1
                               n = n-pow(2, i)

                       i = i-1

                        
                grayArr = [0 for x in range(4)]

                grayArr[3] = arrBin[3]
                grayArr[2] = self.xOr(arrBin[3], arrBin[2])
                grayArr[1] = self.xOr(arrBin[2], arrBin[1])
                grayArr[0] = self.xOr(arrBin[1], arrBin[0])
                                
                return grayArr                                
                        
                


        def createInArr(self, vprinter):

                gridwidth = 10
                gridheight = 10
                gridsize = gridwidth*gridheight
                inArr=[0 for i in range (gridsize+9)]
                
                for i in range(gridwidth):
                    for j in range(gridheight):
                        inArr[i*gridwidth + j] = self.grid[i][j]

                xLoc = round(vprinter.p.x, 0)
                yLoc = round(vprinter.p.y, 0)
                xArr = self.convertGray(xLoc)
                yArr = self.convertGray(yLoc)
                

                for i in range(0, 3):
                        inArr[gridsize+i] = xArr[i]

                for i in range(4, 7):
                        inArr[gridsize+i] = yArr[i-4]

                if vprinter.penDown:
                        inArr[108] = 1
                else:
                        inArr[108]=0

                return inArr

        
        def detFitness(self):
                score = 0
        
                gridwidth = 10
                gridheight = 10
                gridsize = gridwidth*gridheight
                target = [0 for i in range (gridsize)]
                  
                for i in range(gridwidth):
                        for j in range(gridheight):
                            if i==j:
                                target[i*gridwidth+j]=1

        
                actual = [0 for i in range (gridsize)]
                for i in range(gridwidth):
                        for j in range(gridheight):
                            actual[i*gridwidth+j] = self.grid[i][j]

                for i in range(gridsize):
                    if target[i]==actual[i]:
                        score += 1

                return score


        def getGreatest(self, arr, loopCount):
                greatestVal = 0
                greatestIndex = 0
                for i in range(0, loopCount):
                        if arr[i]>greatestVal:
                            greatestVal = arr[i]
                            greatestIndex = i

                return greatestVal, greatestIndex
