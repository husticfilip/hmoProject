import math
import random
from searchAlgorithms.Moves import randomPick_move_0_1
from searchAlgorithms.LocalSearch import localSearch
from utils.Classes import SolutionInstance
import copy

def verySlowDecrease(beta=0.001):
    def fun(T):
        return T/(1+beta*T)
    return fun

def generateRandomNeighbour(solution:SolutionInstance):
    newSol = copy.deepcopy(solution)

    while True:
        truck1 = random.choice(newSol.trucks)
        truck2 = random.choice(newSol.trucks)
        objBefore = len(truck1.customers) ** 2 + len(truck2.customers) ** 2

        if truck1 != truck2:
            moveMade = randomPick_move_0_1(truck1, truck2)

            if moveMade:
                objAfter = len(truck1.customers) ** 2 + len(truck2.customers) ** 2
                newSol.customerDenistyObjValue += (objAfter-objBefore)

                # mozda smo maknuli jednu rutu
                if len(truck2.customers) == 0:
                    newSol.trucks.remove(truck2)
                    newSol.usedTrucks -= 1

                return newSol

def simAnn(initalSolution: SolutionInstance, T0, Tf, coolingSchedule, numberOfWorseMovesBeforeLocalSearch=20):
    initalSolution.setCustomerDensityObjValue()

    currentSolution = copy.deepcopy(initalSolution)
    bestSolution = copy.deepcopy(initalSolution)
    numOfItWithoutImprovement = 0

    T = T0
    while T > Tf:
        newSolution = generateRandomNeighbour(currentSolution)

        deltaF = currentSolution.customerDenistyObjValue - newSolution.customerDenistyObjValue
        if deltaF <= 0:
            currentSolution = newSolution

            if currentSolution.customerDenistyObjValue > bestSolution.customerDenistyObjValue:
                currentSolution = localSearch(currentSolution)
                bestSolution = copy.deepcopy(currentSolution)
                numOfItWithoutImprovement = 0
                T = T0

        elif math.exp(-deltaF / T) > random.random():
            currentSolution = newSolution
            numOfItWithoutImprovement += 1

        if numOfItWithoutImprovement == numberOfWorseMovesBeforeLocalSearch:
            currentSolution = localSearch(currentSolution)
            if currentSolution.customerDenistyObjValue > bestSolution.customerDenistyObjValue:
                bestSolution = copy.deepcopy(currentSolution)
                T = T0
            numOfItWithoutImprovement = 0

        T = coolingSchedule(T)

    bestSolution.evaluateRouteForAllLazyEvaluateTrucks()
    return bestSolution