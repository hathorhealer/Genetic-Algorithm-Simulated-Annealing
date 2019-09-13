import numpy as np

def GACont(parameterRanges,GANumber):
    """
    The "parameterRanges" input should be a list containing a numerical upper bound
    for the range for each parameter, and the lower bound should be prepared as
    0. In the 1-d curve example, this should be the x-range.
    """
    candidates = []
    for j in range(GANumber):
            candidate = []
            for i in range(len(parameterRanges)):
                  candidate.append(parameterRanges[i]*np.random.random_sample())
            candidates.append(list(candidate))
    return candidates

###############################################################

def mutateCont(parent,parameterRanges,mutationProbability,mutationScale):

    """
    This is for continuous problems.
    """
    child = list(parent)
    if np.random.random_sample()<mutationProbability:
        theta = np.random.random_sample()*np.pi*2
        magnitude = abs(np.random.normal(scale=mutationScale))
        child[0] = child[0] + magnitude*np.cos(theta)
        child[1] = child[1] + magnitude*np.sin(theta)
    for i in range(len(child)):
        if child[i] < 0:
            child[i] = 0
        if child[i] > parameterRanges[i]:
            child[i] = parameterRanges[i]
    return list(child)

###############################################################

def crossover(parent1,parent2,discrete):
    if not discrete:
        listParent1 = list(str(parent1[0])[2:]+str(parent1[1])[2:])
        listParent2 = list(str(parent2[0])[2:]+str(parent2[1])[2:])
        splicePoint1 = np.random.randint(len(listParent1))
        listChild1 = []
        listChild2 = []
        parent1Splice1 = listParent1[:splicePoint1]
        parent1Splice2 = listParent1[splicePoint1:]
        parent2Splice1 = listParent2[:splicePoint1]
        parent2Splice2 = listParent2[splicePoint1:]
        listChild1 += parent1Splice1 + parent2Splice2
        listChild2 += parent2Splice1 + parent1Splice2
        conversionChild1 = ["".join(listChild1[:len(listChild1)/2]),"".join(listChild1[len(listChild1)/2:])]
        conversionChild2 = ["".join(listChild2[:len(listChild2)/2]),"".join(listChild2[len(listChild2)/2:])]
        child1 = [float("0."+conversionChild1[0]),float("0."+conversionChild1[1])]
        child2 = [float("0."+conversionChild2[0]),float("0."+conversionChild2[1])]
        return list(child1),list(child2)
    if discrete:


        return list(child)


###############################################################

def breedCont(candidatesSorted,fitnessSortedNormalised,mutationProbability,mutationScale,parameterRanges,crossoverFlag,discrete):
    newGeneration = [list(candidatesSorted[-1])] #elitism

    while len(newGeneration) < len(candidatesSorted):
          flag = 1
          while flag:
                parent1Index = np.random.randint(len(candidatesSorted))
                randomCheck = np.random.random_sample()
                chance = randomCheck-fitnessSortedNormalised[parent1Index][0]
                if chance <= 0.0:
                      parent1 = list(candidatesSorted[parent1Index])
                      flag = 0

          flag = 1
          while flag:
                parent2Index = np.random.randint(len(candidatesSorted))
                randomCheck = np.random.random_sample()
                chance = randomCheck-fitnessSortedNormalised[parent2Index][0]
                if chance <= 0.0:
                      parent2 = list(candidatesSorted[parent2Index])
                      flag = 0
          if crossoverFlag:
              crossoverChildren = list(crossover(parent1,parent2,discrete))
              child1 = list(crossoverChildren[0])
              child2 = list(crossoverChildren[1])
          else:
            child1 = list(parent1)
          child1 = list(mutateCont(child1,parameterRanges,mutationProbability,mutationScale))
          newGeneration.append(list(child1))
          if crossoverFlag:
              child2 = list(mutateCont(child2,parameterRanges,mutationProbability,mutationScale))
              newGeneration.append(list(child2))
    return list(newGeneration)

###############################################################

def sortFitness(fitnesses):

      """
      fitnesses should be a list containing tuples corresponding to each string
      in the GA. In turn the tuple should contain a fitness value and an index
      number corresponding to the index number of the string in the
      candidates list.
      """
      sortedFitnesses = sorted(fitnesses, key=lambda slot:slot[0])
      return list(sortedFitnesses)

###############################################################

def sortGA(candidates,fitnessSorted):
      """
      candidates should be a list containing lists for each string
      with the parameters that correspond to the problem.
      fitnessSorted should be a list containing tuples corresponding to
      candidates, sorted by fitness. The tuple should be a fitness value
      and an "out of order" index number.
      """
      sorted = []
      for i in range (len(fitnessSorted)):
            slotList = fitnessSorted[i]
            slot = slotList[1]
            sorted.append(candidates[slot])
      return sorted

################################################################

def GAProgress(fitnessSorted):
      top = fitnessSorted[len(fitnessSorted)-1]
      q3 = fitnessSorted[int(len(fitnessSorted)*(0.75))]
      q2 = fitnessSorted[int(len(fitnessSorted)*(0.5))]
      q1 = fitnessSorted[int(len(fitnessSorted)*(0.25))]
      bottom = fitnessSorted[0]
      return ([bottom, q1, q2, q3, top])