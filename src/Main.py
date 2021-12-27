from searchAlgorithms.GreedyConstruction import greedy
from searchAlgorithms.LocalSearch import localSearch
from searchAlgorithms.SimulatedAnnealing import simAnn, verySlowDecrease
from utils.Utility import readInstance


def findBetaFor(T0, Tf, N):
    return (T0- Tf)/(N*T0*Tf)

def testDifferentParameters(intancePath):
    inst = readInstance(intancePath)
    greedySol = greedy(problem=inst)
    localSearchSol = localSearch(initSol=greedySol)

    N = 5000    # otprilike broj iteracija koji zelimo za sim ann
    T0 = 100
    for Tf in [1,5,10]:
        print("Tf=", Tf)
        beta = findBetaFor(T0, Tf, N)   # izracunaj param beta sa obzirom na T0,Tf i zeljeni broj iteracija
        sol = simAnn(localSearchSol, T0, Tf, verySlowDecrease(beta))
        sol.printSolution(all=False)

        print("\n\n")

def normalExecution(intancePath):
    inst = readInstance(intancePath)
    greedySol = greedy(problem=inst)

    print("Greedy solution:")
    greedySol.printSolution()

    localSearchSol = localSearch(initSol=greedySol)
    simAnnSol = simAnn(localSearchSol, T0 = 100, Tf = 1, coolingSchedule=verySlowDecrease(beta=0.001))

    print("Simulated annealing solution:")
    simAnnSol.printSolution()

if __name__ == '__main__':
    normalExecution("resources/instance2")
    #testDifferentParameters("resources/instance1")
