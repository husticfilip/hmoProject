from searchAlgorithms.GreedyConstruction import greedy
from searchAlgorithms.LocalSearch import localSearch
from searchAlgorithms.SimulatedAnnealing import simAnn, verySlowDecrease
from utils.Utility import readInstance


def findBetaFor(T0, Tf, N):
    return (T0 - Tf) / (N * T0 * Tf)


def testDifferentParameters(intancePath):
    inst = readInstance(intancePath)
    greedySol = greedy(problem=inst)
    localSearchSol = localSearch(initSol=greedySol)

    N = 5000  # otprilike broj iteracija koji zelimo za sim ann
    T0 = 100
    for Tf in [1, 5, 10]:
        print("Tf=", Tf)
        beta = findBetaFor(T0, Tf, N)  # izracunaj param beta sa obzirom na T0,Tf i zeljeni broj iteracija
        sol = simAnn(localSearchSol, T0, Tf, verySlowDecrease(beta))
        sol.printSolution(all=False)

        print("\n\n")


def normalExecution(instancePath):
    inst = readInstance(instancePath)
    greedySol = greedy(problem=inst)

    print("Greedy solution:")
    greedySol.printSolution()

    localSearchSol = localSearch(initSol=greedySol)
    simAnnSol = simAnn(localSearchSol, T0=100, Tf=1, coolingSchedule=verySlowDecrease(beta=0.001))

    print("Simulated annealing solution:")
    simAnnSol.printSolution()


def writeSolutionsExecution(inst, i, minutes):
    greedySol = greedy(problem=inst)
    localSearchSol = localSearch(initSol=greedySol)
    simAnnSol = simAnn(localSearchSol, minutes=minutes)

    simAnnSol.writeSolutionToFile(minutes, i)
    simAnnSol.printSummary(minutes, i)


def findBestParameters(i):
    inst = readInstance("../resources/instance" + str(i))

    greedySol = greedy(problem=inst)
    localSearchSol = localSearch(initSol=greedySol)

    N = 500  # otprilike broj iteracija koji zelimo za sim ann
    bestSolution = simAnn(localSearchSol, 100, 1, verySlowDecrease(0.1))
    bestParams = [100, 1, 0.1]
    for t0 in range(100, 1000, 100):
        for tf in [1, 5]:
            beta = findBetaFor(t0, tf, N)
            simAnnSol = simAnn(localSearchSol, t0, tf, verySlowDecrease(beta))
            if simAnnSol.usedTrucks < bestSolution.usedTrucks or (
                    simAnnSol.usedTrucks == bestSolution.usedTrucks and simAnnSol.totalRouteDistance < bestSolution.totalRouteDistance):
                bestSolution = simAnnSol
                bestParams = [t0, tf, beta]

    simAnnSol.writeSolutionToFile(0, i)
    simAnnSol.printSummary(0, i)
    print(bestParams)
    print("\n\n\n")


if __name__ == '__main__':

    # for i in range(1, 7, 1):
    #     findBestParameters(i)

    for i in range(1, 7, 1):
        inst = readInstance("../resources/instance" + str(i))
        for j in [1, 5, 0]:
            writeSolutionsExecution(inst, i, j)

    # normalExecution("resources/instance1")
    # testDifferentParameters("resources/instance1")
