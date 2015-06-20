__author__ = 'Gorilla'

import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

def rabbitGrowth():
    """
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up,
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP

    # TO DO
    for x in range(CURRENTRABBITPOP):
        if random.random() <= 1.0 - CURRENTRABBITPOP / float(MAXRABBITPOP):
            if CURRENTRABBITPOP < MAXRABBITPOP:
                CURRENTRABBITPOP += 1

def foxGrowth():
    """
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP

    # prob that a fox eats a rabbit
    # SUCCESS case
    for x in range(CURRENTFOXPOP):

        if random.random() <= CURRENTRABBITPOP / float(MAXRABBITPOP):
            if CURRENTRABBITPOP > 10:
                CURRENTRABBITPOP -= 1

                # giving birth to fox
                if random.random() <= 1/float(3):
                    CURRENTFOXPOP += 1
        else:
            # FAILURE than incurs 1/10 chance of dying
            # if random.random() <= 1/float(10):

            # try to change to 9/10 chance of dying
            if random.random() <= 9/float(10):
                if CURRENTFOXPOP > 10:
                    CURRENTFOXPOP -= 1


def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """

    # TO DO
    rabbits = []
    foxes = []

    for i in range(numSteps):
        rabbitGrowth()
        foxGrowth()
        rabbits.append(CURRENTRABBITPOP)
        foxes.append(CURRENTFOXPOP)


    return (rabbits, foxes)


def plot(numSteps):
    foxes, rabbits = runSimulation(numSteps)

    pylab.plot([i for i in range(numSteps)], rabbits, 'ro', label = "rabbits")
    pylab.plot([i for i in range(numSteps)], foxes, 'b', label = "foxes")
    pylab.title("relevance between rabbits and foxes")
    pylab.legend()

    coeff = pylab.polyfit(range(len(rabbits)), rabbits, 2)
    pylab.plot(pylab.polyval(coeff, range(len(rabbits))))
    coeff2 = pylab.polyfit(range(len(foxes)), foxes, 2)
    pylab.plot(pylab.polyval(coeff2, range(len(foxes))))
    pylab.show()


rabbitGrowth()
print CURRENTRABBITPOP
rabbitGrowth()
print CURRENTRABBITPOP


# runSimulation(2000)
plot(200)