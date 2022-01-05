import math
from typing import List


class Customer:

    def __init__(self, id, xCoord, yCoord, demand, readyTime, dueTime, serviceTime):
        self.id = id
        self.serviceTime = serviceTime
        self.dueTime = dueTime
        self.readyTime = readyTime
        self.demand = demand
        self.yCoord = yCoord
        self.xCoord = xCoord

    def __lt__(self, other):
        return self.id > other.id


class ProblemInstance:

    def __init__(self, numVehicles, VehiCapacity, depot, customers):
        ProblemInstance.customers = customers
        ProblemInstance.depot = depot
        ProblemInstance.vehicleCapacity = VehiCapacity
        ProblemInstance.numVehicles = numVehicles
        ProblemInstance.numOfCustomers = len(customers) - 1

        from utils.Utility import initDistanceMatrix
        ProblemInstance.distances = initDistanceMatrix(customers)


class Truck:

    def __init__(self, truckCapacity):
        self.truckCapacity = truckCapacity
        self.leftCapacity = truckCapacity
        self.customers: List[Customer] = []
        self.timeOnTheRoute = 0

        self.routeLazyEvaluate = False

    def setCustomers(self, customers):
        self.customers = customers

    def setObjValue(self, objValue):
        self.timeOnTheRoute = objValue

    def evaluateRouteAndSetObJvalue(self):
        from utils.Utility import evaluateRoute
        self.timeOnTheRoute, self.leftCapacity = evaluateRoute(self.customers)

    def copyCustomersList(self) -> List[Customer]:
        return self.customers[:]

    # Metoda evaluira rutu kao da je newCustomer umetnut u listu klijenata na index index
    # ovo radimo jer puno rjesenja nece biti dobro zbog ogranicenja kapaciteta i obilaska
    # pa je ovo puno jeftinije nego da radimo:
    #       truck.customers.insert(index, newCustomer)
    #       timeOnTheRoute, leftCapacity = evaluateRoute(truck.customers)
    #       if timeOnTheRoute == math.inf    # ruta krsi ogranicenja
    #           truck.customers.remove(index)
    #
    def setAtIndexAndEvaluate(self, index, newCustomer: Customer):
        capacity = self.leftCapacity - newCustomer.demand
        if capacity < 0:
            return math.inf, None

        # Path before adding new customer
        currCust = ProblemInstance.depot
        time = 0
        for i in range(index):
            nextCust = self.customers[i]
            dist = math.ceil(ProblemInstance.distances[currCust.id][nextCust.id])

            if time + dist < nextCust.readyTime:
                time = nextCust.readyTime
            else:
                time += dist
            time += nextCust.serviceTime

            currCust = nextCust

        # add customer at index
        dist = math.ceil(ProblemInstance.distances[currCust.id][newCustomer.id])
        if time + dist > newCustomer.dueTime:
            return math.inf, None

        if time + dist < newCustomer.readyTime:
            time = newCustomer.readyTime
        else:
            time += dist
        time += newCustomer.serviceTime

        currCust = newCustomer

        # Path after adding new customer
        for i in range(index, len(self.customers)):
            nextCust = self.customers[i]
            dist = math.ceil(ProblemInstance.distances[currCust.id][nextCust.id])

            if time + dist > nextCust.dueTime:
                return math.inf, None

            if time + dist < nextCust.readyTime:
                time = nextCust.readyTime
            else:
                time += dist
            time += nextCust.serviceTime

            currCust = nextCust

        # Check if there is time to get back to depot
        time += math.ceil(ProblemInstance.distances[currCust.id][ProblemInstance.depot.id])
        if time <= ProblemInstance.depot.dueTime:
            return time, capacity
        else:
            return math.inf, None


class SolutionInstance:

    def __init__(self, truckCapacity, problem):
        self.usedTrucks = 0
        self.trucksCapacity = truckCapacity
        self.trucks: List[Truck] = []
        self.problem = problem
        self.totalRouteDistance = 0
        self.customerDenistyObjValue = 0

        self.iterations = 0

    def initNewTruck(self):
        self.usedTrucks += 1
        self.trucks.append(Truck(self.trucksCapacity))
        return self.trucks[-1]

    def setCustomerDensityObjValue(self):
        self.customerDenistyObjValue = 0
        for truck in self.trucks:
            self.customerDenistyObjValue += len(truck.customers) ** 2

    def evaluateRouteForAllLazyEvaluateTrucks(self):
        for truck in self.trucks:
            if truck.routeLazyEvaluate:
                truck.evaluateRouteAndSetObJvalue()
                truck.routeLazyEvaluate = False

    def printSolution(self, all=True):
        print("--------------------------------------------------")

        totalTime = 0
        totalCustomers = 0
        for i, truck in enumerate(self.trucks):
            if all:
                print("Truck ", i, ".", "   Num of customers=", len(truck.customers), "    Route time=",
                      truck.timeOnTheRoute, "    Capacity=", truck.leftCapacity)

            totalTime += truck.timeOnTheRoute
            totalCustomers += len(truck.customers)
        print("Number of trucks=", self.usedTrucks)
        print("Total solution route time=", totalTime)
        print("Customers on the routes=", totalCustomers)
        print("--------------------------------------------------")



    def writeSolutionToFile(self, time, instance):
        filename = "../results/res-" + getTimeStr(time) + "-i" + str(instance) + ".txt"
        f = open(filename, "w")

        f.write(self.usedTrucks.__str__())

        time = 0
        totalDistancePassed = 0.0
        currentCustomer = ProblemInstance.depot
        for i, truck in enumerate(self.trucks):
            f.write("\n"+str(i+1) + ": 0(0)->")

            for nextCustomer in truck.customers:
                dist = math.ceil(ProblemInstance.distances[currentCustomer.id][nextCustomer.id])
                if time + dist < nextCustomer.readyTime:
                    time = nextCustomer.readyTime
                else:
                    time += dist
                f.write(str(nextCustomer.id) + "(" + str(time) + ")->")

                totalDistancePassed += ProblemInstance.distances[currentCustomer.id][nextCustomer.id]
                time += nextCustomer.serviceTime
                currentCustomer = nextCustomer

            # get beack to the depot
            time += math.ceil(ProblemInstance.distances[currentCustomer.id][ProblemInstance.depot.id])
            totalDistancePassed += ProblemInstance.distances[currentCustomer.id][ProblemInstance.depot.id]

            f.write("0(" + str(time) + ")")

            # start new route
            time = 0
            currentCustomer = ProblemInstance.depot

        self.totalRouteDistance = totalDistancePassed
        f.write("\n"+str(totalDistancePassed))
        f.close()

    # instance, time, no of trucks, total distance, iterations
    def printSummary(self, time, instance):
        print(instance, ",", getTimeStr(time), ",", self.usedTrucks, ",", self.totalRouteDistance, ",", self.iterations, sep='')


def getTimeStr(time):
    return "un" if time == 0 else str(time) + "m"