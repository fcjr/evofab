##
## Author: Kristina Striegnitz
##
## Version: Fall 2011 
##
## This character has an FMS that allows it to go back and forth
## between two states: waiting and following a given path. The path is
## specified as a sequence of points and the character uses seek
## behavior to get from one point to the next.
##

import pygame
from moving_ball_2d import MovingBall
from vector import Vector

class VirtualPrinter(MovingBall):

    def __init__ (self, x, y, r, m, color, grid):

        MovingBall.__init__(self, x, y, r, m, color, 0, 0)
        self.grid = grid
        self.penDown = False
        
    def move (self, dt):
        #print 'inside move begin', dt, self.v, self.p
        #total_acceleration = self.a.plus(world.gravity)
        #self.v = self.v.plus (total_acceleration.times(float(dt)/1000))
        self.clamp_v ()
        self.stop_v ()
        self.p = self.p.plus(self.v.times(float(dt)/1000))
        #print 'inside move end: dt, v, p ', dt, self.v, self.p
              
    def handle_events(self,keymap):
            if keymap.has_key(pygame.K_a) and keymap[pygame.K_a]:
                self.goLeft()
            if keymap.has_key(pygame.K_d) and keymap[pygame.K_d]:
                self.goRight()
            if keymap.has_key(pygame.K_w) and keymap[pygame.K_w]:
                self.goUp()
            if keymap.has_key(pygame.K_x) and keymap[pygame.K_x]:
                self.goDown()
            if keymap.has_key(pygame.K_p) and keymap[pygame.K_p]:
                print 'pen down'
                self.penDown = True
            if keymap.has_key(pygame.K_u) and keymap[pygame.K_u]:
                print 'pen up'
                self.penDown = False
            
            
    

    #JR - isntead of using 10 as a "magic number" which you reuse
    # multiple times, instead in __init__ declare a speed
    # as a variable self.PRINTSPEED and use that in the code below.
    # that way if you want to change the speed you only have to change one value
    
    def goLeft(self, printSpeed):
        self.v.x = -1*printSpeed
        

    def goRight(self, printSpeed):
        self.v.x = printSpeed
        
        
    def goUp(self, printSpeed):
        self.v.y = printSpeed

    def goDown(self, printSpeed):
        self.v.y = -1*printSpeed
        
    def setPenUp(self):
        self.penDown = False
        
    def setPenDown(self):
        self.penDown = True

    def simulate(self,dt):
        #print 'inside simulate', dt
        self.move(dt)
        if self.penDown:
            p = (self.p.x,self.p.y)
            self.grid.PenDraw(p)


    def setPrinter(self, outVal):
            maxspeed = 1000
            halfspeed = maxspeed/2
            fourthspeed = maxspeed/4
            
            
           
            
       
            xArr = outVal[0:3]
            yArr = outVal[3:6]
            penArr = outVal[6:9]
            
            #setting the x speed
            velocityScale = [-1,0,1]

            xvelocity = sum(float(xval*velo) for xval,velo in zip(xArr,velocityScale))/sum(xArr)
            if xvelocity<0:
                self.goLeft(maxspeed)
            else:
                self.goLeft(maxspeed)

            yvelocity = sum(float(yval*velo) for yval,velo in zip(yArr,velocityScale))/sum(yArr)
            if yvelocity<0:
                self.goDown(maxspeed)
            else:
                self.goUp(maxspeed)
            
                '''
            #\if xArr[0]==1:
                #if xArr[1] == 1:
                    if xArr[2]==1:
                        self.goRight(maxspeed)
                    else:
                        self.goRight(halfspeed)
                elif xArr[2]== 0:
                    self.goRight(0)
                else:
                    self.goRight(fourthspeed)
            elif xArr[1] == 1:
                if xArr[2]==1:
                    self.goLeft(maxspeed)
                else:
                    self.goLeft(halfspeed)
            elif xArr[2]== 0:
                self.goLeft(0)
            else:
                self.goLeft(fourthspeed)
            

            #setting the y speed
                
            if yArr[0]==1:
                if yArr[1] == 1:
                    if yArr[2]==1:
                        self.goUp(maxspeed)
                    else:
                        self.goUp(halfspeed)
                elif yArr[2]== 0:
                    self.goUp(0)
                else:
                    self.goUp(fourthspeed)
            elif yArr[1] == 1:
                if yArr[2]==1:
                    self.goDown(maxspeed)
                else:
                    self.goDown(halfspeed)
            elif yArr[2]== 0:
                self.goDown(0)
            else:
                self.goDown(fourthspeed)

            '''

            #set the pen

            '''
            penSum= 0
            for i in range (0, 3):
                penSum += penArr[i]

            if penSum == 0:
                self.setPenDown()

            else:
                self.setPenUp()
            '''

            penSum = sum(float(penVal*velo) for penVal,velo in zip(penArr,velocityScale))/sum(penArr)
            if penSum<0:
                self.setPenDown()
            else:
                self.setPenUp()


    


    def checkBoundary(self):
        self.collide_edge(self.grid)
