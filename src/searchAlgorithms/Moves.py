import math
import random

from utils.Classes import Truck
from utils.Utility import evaluateRoute


###################################
#       MOVE_0_0
###################################

# Nadi prvi swap unutar kamiona koji rezultira smanjenjem udaljenosti/vremena
def move_0_0(truck: Truck):
    customers = truck.customers
    currentTimeOnTheRoute = truck.timeOnTheRoute

    for i in range(len(customers)):
        for j in range(i+1, len(customers)):
            customers[i], customers[j] = customers[j], customers[i]

            evalTime, capacity = evaluateRoute(customers)
            if evalTime < currentTimeOnTheRoute:
                truck.timeOnTheRoute = evalTime
                return True
            customers[i], customers[j] = customers[j], customers[i]

    return False

###################################
#       MOVE_1_1
###################################

# pronadi prvi swap izmedu kamiona koji smanjuje udaljenost/vrijeme ruta
def move_1_1(truck1: Truck, truck2: Truck):
    customers1 = truck1.customers
    customers2 = truck2.customers

    currentRoutesTime = truck1.timeOnTheRoute + truck2.timeOnTheRoute

    for ind1 in range(0, len(truck1.customers)):
        cust1 = customers1[ind1]

        for ind2 in range(0, len(truck2.customers)):
            cust2 = customers2[ind2]
            # Check if capacity constraint will be satisfied if swap was made
            if (truck1.leftCapacity + cust1.demand - cust2.demand) > 0 and (
                    truck2.leftCapacity + cust2.demand - cust1.demand) > 0:
                # swap two customers
                customers1[ind1], customers2[ind2] = cust2, cust1

                truck1RouteTime, truck1LeftCapacity = evaluateRoute(customers1)
                truck2RouteTime, truck2LeftCapacity = evaluateRoute(customers2)

                if truck1RouteTime + truck2RouteTime < currentRoutesTime:
                    truck1.timeOnTheRoute = truck1RouteTime
                    truck2.timeOnTheRoute = truck2RouteTime
                    truck1.leftCapacity = truck1LeftCapacity
                    truck2.leftCapacity = truck2LeftCapacity
                    return True

                # if swap did not result in better solution, swap back as it was
                customers1[ind1], customers2[ind2] = cust1, cust2

    return False


###################################
#       MOVE_0_1
###################################

# umeci musterije iz truck2 u truck1 i vrati prvo rjesenje koje zadovoljava ogranicenja
# ovdje truck2 uvijek ima manje klijenata od truck1!!!  -> tj pokusavamo iz rute sa manje klijenata gurnuti klijente u rutu sa vise klijenata
# zbog toga ce customerDenistyObjValue sigurno porasti i dobiti cemo bolje rjesnje
def move_0_1(truck1: Truck, truck2: Truck):
    for ind2 in range(0, len(truck2.customers)):
        cust2 = truck2.customers[ind2]

        for ind1 in range(0, len(truck1.customers)+1):
            # evaluiraj kao da si stavio cust2 na index ind1 u truck1
            routeTime, leftCapacity = truck1.setAtIndexAndEvaluate(index=ind1, newCustomer=cust2)

            if routeTime != math.inf:
                truck1.customers.insert(ind1, cust2)
                truck1.leftCapacity = leftCapacity
                truck1.timeOnTheRoute = routeTime

                del truck2.customers[ind2]
                truck2.leftCapacity += cust2.demand
                # da ne gubimo vrijeme rutu od truck2 cemo naknadno evaluirati, a mozda ce se i sama evaluirati kroz naredne iteracije local searcha
                truck2.routeLazyEvaluate = True
                truck1.routeLazyEvaluate = False
                return True

            startInd1 = 0

    return False


# trazi se prvi move_0_1 koji nece krsiti ogranicenja
# ovdje primijeti da truck2 moze imati vise klijenata na svojoj ruti od truck1
# s toga mozda guramo musterije iz kamiona sa vise musterija u onaj sa mnje i tako nam pada customerDenistyObjValue
# ali to je ok, jer ovo korisitmu u sim.ann. gdje prihvacamo i gora rjesenja
#
# ovdje simuliramo random move, ne krecemo iteraciju u petljama od pocetka, nego od neke radnom pozicije u petlji
def randomPick_move_0_1(truck1: Truck, truck2:Truck):
    # kreni potragu na nekoj radnom pozciji u for loop-u
    randomIndex1 = random.randint(0, len(truck1.customers))
    randomIndex2 = random.randint(0, len(truck2.customers) - 1)

    startInd1 = randomIndex1
    for ind2 in range(randomIndex2, len(truck2.customers)):
        cust2 = truck2.customers[ind2]

        for ind1 in range(startInd1, len(truck1.customers) + 1):
            routeTime, leftCapacity = truck1.setAtIndexAndEvaluate(index=ind1, newCustomer=cust2)

            if routeTime != math.inf:
                truck1.customers.insert(ind1, cust2)
                truck1.leftCapacity = leftCapacity
                truck1.timeOnTheRoute = routeTime

                del truck2.customers[ind2]
                truck2.leftCapacity += cust2.demand
                truck2.routeLazyEvaluate = True
                truck1.routeLazyEvaluate = False
                return True
        # nakon prve iteracije unutarnju petlju kreni od 0...tako zapravo prolazimo kroz sve kombinacije ind2,ind1 od pocetnih indexa randomIndex1, randomIndex2
        startInd1 = 0

    # ako nisi nasao feaseable move startajuci od ind2=randomIndex2, ind1=randomIndex1, probaj krenuti od ind2=0,ind1=0 i stani kad dodes do randomIndex1, randomIndex2
    for ind2 in range(0, randomIndex2 + 1):
        cust2 = truck2.customers[ind2]

        for ind1 in range(0, len(truck1.customers) + 1):
            if ind2 == randomIndex2 and ind1 == randomIndex1:
                return False

            routeTime, leftCapacity = truck1.setAtIndexAndEvaluate(index=ind1, newCustomer=cust2)
            if routeTime != math.inf:
                truck1.customers.insert(ind1, cust2)
                truck1.leftCapacity = leftCapacity
                truck1.timeOnTheRoute = routeTime

                del truck2.customers[ind2]
                truck2.leftCapacity += cust2.demand
                truck2.routeLazyEvaluate = True
                truck1.routeLazyEvaluate = False
                return True