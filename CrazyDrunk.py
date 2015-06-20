__author__ = 'Gorilla'

import pylab
import math

# Global Variables
LEFT_EDGE = BOTTOM_EDGE = -50
RIGHT_EDGE = TOP_EDGE = 50


#set line width
pylab.rcParams['lines.linewidth'] = 6
#set font size for titles
pylab.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
pylab.rcParams['xtick.major.size'] = 5
#set size of numbers on y-axis
pylab.rcParams['ytick.major.size'] = 5
#set size of markers
pylab.rcParams['lines.markersize'] = 10


class Location(object):

    def __init__(self, x, y):
        """x and y are floats"""
        self.x = x
        self.y = y

    def move(self, deltaX, deltaY):
        """deltaX and deltaY are floats"""
        return Location(self.x + deltaX, self.y + deltaY)

    # for Solid Wall
    def moveSW(self, deltaX, deltaY):
        if self.x + deltaX < LEFT_EDGE or self.x + deltaX > RIGHT_EDGE:
            deltaX = 0
        if self.y + deltaY < BOTTOM_EDGE or self.y + deltaY > TOP_EDGE:
            deltaY = 0

        return Location(self.x + deltaX, self.y + deltaY)

    # for Return Home
    def moveRH(self, deltaX, deltaY):
        if self.x + deltaX < LEFT_EDGE or self.x + deltaX > RIGHT_EDGE:
            deltaX = -1 * self.x
        if self.y + deltaY < BOTTOM_EDGE or self.y + deltaY > TOP_EDGE:
            deltaY = -1 * self.y

        return Location(self.x + deltaX, self.y + deltaY)

    # Small Planet
    def moveSP(self, deltaX, deltaY):
        if self.x + deltaX < LEFT_EDGE:
            deltaX += RIGHT_EDGE - LEFT_EDGE
        elif self.x + deltaX > RIGHT_EDGE:
            deltaX += LEFT_EDGE - RIGHT_EDGE

        if self.y + deltaY < BOTTOM_EDGE:
            deltaY += TOP_EDGE - BOTTOM_EDGE
        elif self.y + deltaY > TOP_EDGE:
            deltaY += BOTTOM_EDGE - TOP_EDGE

        return Location(self.x + deltaX, self.y + deltaY)


    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # return Euclidian distance
    def distFrom(self, other):
        ox = other.x
        oy = other.y
        xDist = self.x - ox
        yDist = self.y - oy
        return (xDist**2 + yDist**2)**0.5

    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'




# This Field is abstract
# it has only Drunk people element inside
# and the respective location
# using the dictionary data structure with format (drunk_person:location)

class Field(object):

    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc

    def moveDrunk(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]

        #use move method of Location to get new location
        self.drunks[drunk] = currentLocation.move(xDist, yDist)


    # move in solid wall
    def moveDrunk_SW(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]

        #use move method of Location to get new location
        self.drunks[drunk] = currentLocation.moveSW(xDist, yDist)


    def moveDrunk_RH(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]

        #use move method of Location to get new location
        self.drunks[drunk] = currentLocation.moveRH(xDist, yDist)

    def moveDrunk_SP(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]

        #use move method of Location to get new location
        self.drunks[drunk] = currentLocation.moveSP(xDist, yDist)







    # def moveDrunk_custom(self, drunk, method = None):
    #     if not drunk in self.drunks:
    #         raise ValueError('Drunk not in field')
    #     xDist, yDist = drunk.takeStep()
    #     currentLocation = self.drunks[drunk]
    #
    #     #use move method of Location to get new location
    #     self.drunks[drunk] = method(currentLocation, xDist, yDist)

    def getLoc(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]










import random


class Drunk(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'This drunk is named ' + self.name

class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0,1.0), (0.0,-1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)

# THIS class is used for FINAL EXAM
class CrazyDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(-1.0,-1.0),(-1.0,0.0),(-1.0,1.0),(0.0,1.0),
                       (0.0,-1.0),(1.0,-1.0),(1.0,0.0),(1.0,1.0)]

        return random.choice(stepChoices)



"""
# New version of Walk
# returns the actual x and y distance from the start point to the end point of a random walk.
# just record the last location
def walkVector(f, d, numSteps):
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return(f.getLoc(d).getX() - start.getX(),
           f.getLoc(d).getY() - start.getY())
# New version of simWalk using walkVector() instead of walk()
# return a tuple (x,y) instead of Euclidian distance
def simWalkVector(numSteps, numTrials, dClass):
    homer = dClass('Homer')
    origin = Location(0, 0)
    distancesX = []
    distancesY = []

    for t in range(numTrials):
        f = Field()
        f.addDrunk(homer, origin)

        (x,y) = walkVector(f, homer, numSteps)
        distancesX.append(x)
        distancesY.append(y)

    return distancesX, distancesY

#New version of drunkTestP using simWalkVector
def drunkTestPVector(numTrials = 50):

    stepsTaken = [i**2 for i in range(50)]

    # for dClass in (UsualDrunk, ColdDrunk, EDrunk, PhotoDrunk, DDrunk):
    for dClass in (UsualDrunk, CrazyDrunk):
        meanX = []
        meanY = []
        for numSteps in stepsTaken:
            distanceX, distanceY = simWalkVector(numSteps, numTrials, dClass)
            meanX.append(sum(distanceX)/len(distanceX))
            meanY.append(sum(distanceY)/len(distanceY))

        pylab.plot(meanX, meanY, "ro",  label = dClass.__name__)
        pylab.xlim(-100, 100)
        pylab.ylim(-100, 100)
        # pylab.gca().set_aspect('equal', adjustable='box')
        pylab.title('Distance from Origin')
        pylab.xlabel('x axis')
        pylab.ylabel('y axis')
        pylab.legend()

        pylab.show()
# TEST
# drunkTestPVector(3)

"""












def walk_Vector_Field(f, d, numSteps):
    start = f.getLoc(d)
    for s in range(numSteps):
        # f.moveDrunk_SW(d) # apply for Solid Wall, WrapedWorld, Small Planet, etc.
        # f.moveDrunk_RH(d)
        f.moveDrunk_SP(d)


    return(f.getLoc(d).getX() - start.getX(),
           f.getLoc(d).getY() - start.getY())


# def walk_Vector_Custom(f, d, numSteps, method = None):
#     start = f.getLoc(d)
#     for s in range(numSteps):
#         f.moveDrunk_custom(d, method) # apply for Solid Wall, WrapedWorld, Small Planet, etc.
#     return(f.getLoc(d).getX() - start.getX(),
#            f.getLoc(d).getY() - start.getY())



def simWalkVector_Field(numSteps, numTrials, dClass):
    homer = dClass('Homer')
    origin = Location(0, 0)
    distancesX = []
    distancesY = []

    for t in range(numTrials):
        f = Field()
        f.addDrunk(homer, origin)

        (x,y) = walk_Vector_Field(f, homer, numSteps)
        distancesX.append(x)
        distancesY.append(y)

    return distancesX, distancesY


# TEST
# simWalkVector_Field(10, 3, CrazyDrunk)


#New version of drunkTestP using simWalkVector
def drunkTestPVector_Field(numTrials):

    stepsTaken = [i for i in range(3000)]

    # for dClass in (UsualDrunk, ColdDrunk, EDrunk, PhotoDrunk, DDrunk):
    # for dClass in (UsualDrunk, CrazyDrunk):
    meanX = []
    meanY = []
    for numSteps in stepsTaken:
        distanceX, distanceY = simWalkVector_Field(numSteps, numTrials, CrazyDrunk)
        meanX.append(sum(distanceX)/len(distanceX))
        meanY.append(sum(distanceY)/len(distanceY))

    pylab.plot(meanX, meanY, "r.",  label = CrazyDrunk.__name__)
    pylab.xlim(-60, 60)
    pylab.ylim(-60, 60)
    # pylab.gca().set_aspect('equal', adjustable='box')
    pylab.title('Distance from Origin')
    pylab.xlabel('x axis')
    pylab.ylabel('y axis')
    pylab.legend()

    pylab.show()



drunkTestPVector_Field(3)