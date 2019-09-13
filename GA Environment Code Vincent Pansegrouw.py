# -*- coding: utf-8 -*-
"""
Created on Fri Mar 09 10:14:02 2018

@author: Vincent
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from GA import *


##########################################


def curve(x,y,spikes):
      height = (np.sin(np.pi*x)*np.sin(spikes*np.pi*x))**2*(np.sin(np.pi*y)*np.sin(spikes*np.pi*y))**2
      return float(height)

def fitnessCheck(candidate,spikes):
      return np.sqrt(curve(float(candidate[0]),float(candidate[1]),spikes))


##########################################


"""
Executable Code starts here
"""

GANumber = 100
parameterRanges = [1,1]
mutationScale = 0.1
mutationProbability = 0.1
generations = []
generationNumber = 100
crossoverFlag = 1
spikes = 1000
discrete = 0

print "Number of spikes: " + str(spikes**2) + ".\n"

candidates = list(GACont(parameterRanges,GANumber))


##########################################


"""
Generating plot of the curve to be optimised.
"""

xStart = 0.0
xStop = 1.0
xSteps = 0.001
yStart = 0.0
yStop = 1.0
ySteps = 0.001


X = np.arange(xStart,xStop,xSteps)
Y = np.arange(yStart,yStop,ySteps)
X, Y = np.meshgrid(X, Y)
Z = (np.sin(np.pi*X)*np.sin(spikes*np.pi*X))**2*(np.sin(np.pi*Y)*np.sin(spikes*np.pi*Y))**2
V = np.arange(0.0,1.0,0.05)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
p = ax.plot_surface(X, Y, Z, linewidth=0)
plt.title("Curve to be optimised which has "+ str(spikes**2)+" local optima.")
plt.show()


##########################################


for j in range(generationNumber):

      fitnesses = []
      for i in range(len(candidates)):
            fitnesses.append((fitnessCheck(candidates[i],spikes),i))
      fitnessSorted = list(sortFitness(fitnesses))
      candidatesSorted = list(sortGA(candidates,fitnessSorted))
      GAProgressList = list(GAProgress(fitnessSorted))
      generations.append(list(GAProgressList))
      if (j+1) in [1,2,5,10,25,50,100,200]:
        plt.contour(X,Y,Z,V)
        plt.title("Contour plot with GA candidates plotted on it. \n Generation "+ str(j+1))
        for XY in candidates:
            plt.scatter(XY[0],XY[1])
        plt.show()
      candidates = list(breedCont(candidatesSorted,fitnessSorted,mutationProbability,mutationScale,parameterRanges,crossoverFlag,discrete))


##########################################


bestList = []
q3List = []
q2List = []
q1List = []
worstList = []
x = np.arange(0.0,generationNumber)
for i in range(generationNumber):
      slot = generations[i]
      bestList.append(slot[4][0])
      q3List.append(slot[3][0])
      q2List.append(slot[2][0])
      q1List.append(slot[1][0])
      worstList.append(slot[0][0])
fig2 = plt.figure()
fig2.subplots_adjust(bottom=0.2)
ax2 = fig2.add_subplot(1,1,1)
bestLine = ax2.plot(bestList,'b-',label='best')

q3Line = ax2.plot(q3List,'g-',label='q3')

q2Line = ax2.plot(q2List,'r-',label='q2')

q1Line = ax2.plot(q1List,'y-',label='q1')

worstLine = ax2.plot(worstList,'m-',label='worst')


##########################################


plt.show()

print "Done! The best candidate's coordinates were: " + str(candidatesSorted[-1])
