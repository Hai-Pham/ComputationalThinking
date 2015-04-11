# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

# choose the best legend location
pylab.rcParams['legend.loc'] = 'best'
#set line width
pylab.rcParams['lines.linewidth'] = 6
#set font size for titles
pylab.rcParams['axes.titlesize'] = 10
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 10
#set size of numbers on x-axis
pylab.rcParams['xtick.major.size'] = 5
#set size of numbers on y-axis
pylab.rcParams['ytick.major.size'] = 5


def simulationDelayedTreatmentPlot(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """

    timesteps = [0, 75, 150, 300]
    additionalStep = 150
    numViruses = 100
    maxPop = 1000


    for timestep in timesteps:

        totVirus = [[] for x in range(timestep + additionalStep)]
        totRVirus = [[] for x in range(timestep + additionalStep)]
        finalPopulation = []

        for i in range(numTrials):
            # a list of 100 alike virus
            viruses = [ResistantVirus(0.1, 0.05, {'guttagonol': False}, 0.005)] * numViruses
            # print len(viruses)
            patient = TreatedPatient(viruses, maxPop)

            for i in range(timestep + additionalStep):
                # record total virus as update's return
                if i == timestep:
                    patient.addPrescription('guttagonol')
                totVirus[i].append(patient.update())
                # record total resistant virus
                totRVirus[i].append(patient.getResistPop({'guttagonol'}))


        # Process the results with average
        averageTotVirus = [sum(result)/float(len(result)) for result in totVirus]
        averageTotRVirus = [sum(r_result)/float(len(r_result)) for r_result in totRVirus]
        time = [i for i in range(timestep + additionalStep)]


        # plot
        if timestep == 0:
            loc = 1
        elif timestep == 75:
            loc = 2
        elif timestep == 150:
            loc = 3
        else:
            loc = 4

        pylab.subplot(2, 2, loc)
        pylab.plot(time, averageTotVirus, 'ro', label = "Avg Total Virus")
        pylab.plot(time, averageTotRVirus, 'bo', label = "Avg Resistant Virus")
        pylab.title("ResistantVirus simulation: " + str(timestep))
        pylab.xlabel("Time Steps")
        pylab.ylabel("Average Virus Population")
        pylab.legend()
    pylab.show()



#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    timesteps = [0, 75, 150, 300]
    additionalStep = 150
    numViruses = 100
    maxPop = 1000


    for timestep in timesteps:

        finalPopulation = []

        for i in range(numTrials):
            # a list of 100 alike virus
            viruses = [ResistantVirus(0.1, 0.05, {'guttagonol': True}, 0.005)] * numViruses
            patient = TreatedPatient(viruses, maxPop)

            for i in range(timestep + additionalStep):
                # record total virus as update's return
                if i == timestep:
                    patient.addPrescription('guttagonol')

                patient.update()

            # for historgram
            # each trial record the last population only
            finalPopulation.append(patient.getTotalPop())

        # plot
        if timestep == 0:
            loc = 1
        elif timestep == 75:
            loc = 2
        elif timestep == 150:
            loc = 3
        else:
            loc = 4

        pylab.subplot(2, 2, loc)
        pylab.hist(finalPopulation, bins=100)

        pylab.title("Delay Treatment Affects " + str(timestep))
        pylab.xlabel("AVG total virus")
        pylab.ylabel("Trials")
        pylab.legend()
    pylab.show()


# simulationDelayedTreatmentPlot(10)
# simulationDelayedTreatment(100)

#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """

    midSteps = [0, 75, 150, 300]
    initStep = 150
    additionalStep = 150
    numViruses = 100
    maxPop = 1000

    for midStep in midSteps:

        finalPopulation = []

        for i in range(numTrials):
            # a list of 100 alike virus
            viruses = [ResistantVirus(0.1, 0.05, {'guttagonol': False, 'grimpex': False}, 0.005)] * numViruses
            patient = TreatedPatient(viruses, maxPop)

            for i in range(initStep + midStep + additionalStep):
                # record total virus as update's return
                if i == initStep:
                    patient.addPrescription('guttagonol')
                if i == initStep + midStep:
                    patient.addPrescription('grimpex')

                patient.update()

            # for historgram
            # each trial record the last population only
            finalPopulation.append(patient.getTotalPop())

        # plot
        if midStep == 0:
            loc = 1
        elif midStep == 75:
            loc = 2
        elif midStep == 150:
            loc = 3
        else:
            loc = 4

        pylab.subplot(2, 2, loc)
        pylab.hist(finalPopulation, bins=100)

        pylab.title("Delay Treatment Affects " + str(midStep))
        pylab.xlabel("AVG total virus")
        pylab.ylabel("Trials")
        pylab.legend()
    pylab.show()


# Test for problem 2
simulationTwoDrugsDelayedTreatment(100)