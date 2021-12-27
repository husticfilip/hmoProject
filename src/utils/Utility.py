from utils.Classes import Customer, ProblemInstance
import math
from typing import List


def euclidianDistance(cust1: Customer, cust2: Customer):
    return math.sqrt( (cust1.xCoord - cust2.xCoord)**2 + (cust1.yCoord - cust2.yCoord)**2)

def initDistanceMatrix(customers):
    return [[euclidianDistance(y, x) for y in customers] for x in customers]

def readInstance(instancePath):
    numOfVehicles = 0
    capacity = 0
    depot = None
    customers = []

    with open(instancePath, "r") as file:
        stage = 0
        for line in file:
            # Firstly read numberOfVeichelsAnd capacity

            splitted = line.split()
            if splitted and splitted[0].isdigit():
                if stage == 0:
                    numOfVehicles = int(splitted[0])
                    capacity = int(splitted[1])
                    stage = 1
                elif stage == 1:
                    depot = Customer(int(splitted[0]), int(splitted[1]), int(splitted[2]), int(splitted[3]), int(splitted[4]),
                                     int(splitted[5]), int(splitted[6]))
                    customers.append(depot)
                    stage = 2
                else:
                    customers.append(Customer(int(splitted[0]), int(splitted[1]), int(splitted[2]), int(splitted[3]), int(splitted[4]),
                                     int(splitted[5]), int(splitted[6])))

    return ProblemInstance(numOfVehicles, capacity, depot, customers)


# Provjeri da li je ruta dobra, da li se ne krse ogranicenja kapaciteta
# ,vremena dolaska kamiona do klijenata i vremena povratka u depot
def evaluateRoute(customers:List[Customer]):
    # if customers list is empty, empty truck
    if not customers:
       return 0, None

    currCust = ProblemInstance.depot
    time = 0
    capacity = ProblemInstance.vehicleCapacity
    for nextCust in customers:
        dist = ProblemInstance.distances[currCust.id][nextCust.id]
        if time + dist > nextCust.dueTime:
            return math.inf, None

        if time + dist < nextCust.readyTime:
            time = nextCust.readyTime
        else:
            time += dist
        time += nextCust.serviceTime

        currCust = nextCust

        capacity -= currCust.demand
        if capacity < 0:
            return math.inf, None

    # Check if there is time to get back to depot
    time += ProblemInstance.distances[currCust.id][ProblemInstance.depot.id]
    if time <= ProblemInstance.depot.dueTime:
        return time, capacity
    else:
        return math.inf, None