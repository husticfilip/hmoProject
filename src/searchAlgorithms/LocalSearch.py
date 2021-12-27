from utils.Classes import SolutionInstance
from searchAlgorithms.Moves import move_0_0,move_1_1,move_0_1
import copy


# Metoda pokusava smanjiti broj ruta, u njoj pozivamo move_0_1
# u move_0_1 truckI uvijek ima vise klijenata od truckJ, tako da pokusavamo klijente
# iz truckJ prebaciti u truckI
def reduceNumberOfRoutes(solution: SolutionInstance):
    trucks = solution.trucks[:]
    changed = False # da li smo napravili move u iteraciji

    for i in range(len(trucks)):
            for j in range(i+1, len(trucks)):
                diffInCustomers = len(trucks[i].customers) - len(trucks[j].customers)
                if diffInCustomers != 0:
                    # TruckI is allways one with more customers
                    truckI = trucks[i] if diffInCustomers>0 else trucks[j]
                    truckJ = trucks[j] if diffInCustomers>0 else trucks[i]

                    move = move_0_1(truckI, truckJ)
                    if move:
                        changed = True
                        if len(truckJ.customers) == 0: # ako smo maknuli jednu rutu
                            solution.trucks.remove(truckJ)
                            solution.usedTrucks -= 1

    return changed


# Metoda pokusava smanjiti prijedenu udaljenost u rjesenju
# move_0_0 radi swap unutar istog kamiona
# move_1_1 radi swap izmedu dva kamiona
def reduceDistancesInRoutes(solution: SolutionInstance):
    trucks = solution.trucks
    changeMade = False

    for i in range(len(trucks)):
        # Try swap moves inside one truck
        move = move_0_0(trucks[i])
        if move:
            changeMade = True

        # Try swap moves between trucks
        for j in range(i+1, len(trucks)):
            move = move_1_1(trucks[i], trucks[j])
            if move:
                changeMade = True

    return changeMade


def localSearch(initSol: SolutionInstance):
    solution = copy.deepcopy(initSol)

    change = True # vrti petlju dok ni prode iteracija bez promjena i u reduceNumberOfRoutes() i u reduceDistancesInRoutes()
    while change:
        change = False
        while reduceNumberOfRoutes(solution):
            pass
        solution.evaluateRouteForAllLazyEvaluateTrucks()
        while reduceDistancesInRoutes(solution):
            change = True

    # za sim ann ce nam trebati postavljen obj value
    solution.setCustomerDensityObjValue()
    return solution