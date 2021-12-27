import bisect
import math
from typing import List

from utils.Classes import ProblemInstance, Customer, SolutionInstance
from utils.Utility import evaluateRoute


def findClosestNeighbour(currentTime, currCust: Customer, unUsedCust:List[Customer], truckCapacity ,distances):
    candidateList = []
    for cust in unUsedCust:
        if cust.demand <= truckCapacity:
            dist = distances[currCust.id][cust.id]
            if currentTime + dist <= cust.dueTime:
                if currentTime + dist < cust.readyTime:
                    bisect.insort_left(candidateList, (cust.readyTime-currentTime, cust))
                else:
                    bisect.insort_left(candidateList, (dist, cust))
    if not candidateList:
        return None, None

    return candidateList[0]

def greedy(problem: ProblemInstance):
    # copy all customers and delete depot from the list
    unUsedCustomers = problem.customers[:]
    del unUsedCustomers[0]

    solution = SolutionInstance(truckCapacity=problem.vehicleCapacity, problem=problem)

    # Start route from depot
    currentCustomer = problem.depot
    currentTime = 0
    currentCapacity = problem.vehicleCapacity
    customers = []
    while True:
        distToCustomer, nextCustomer = findClosestNeighbour(currentTime, currentCustomer, unUsedCustomers, currentCapacity,
                                              problem.distances)
        if nextCustomer is not None:
            customers.append(nextCustomer)
            unUsedCustomers.remove(nextCustomer)

            currentTime = currentTime + distToCustomer + nextCustomer.serviceTime
            currentCapacity -= nextCustomer.demand
            currentCustomer = nextCustomer

        else:
            # Maybe there is no time to get back to depot so remove last customers until there is time
            while True:
                routeTime, leftCapacity = evaluateRoute(customers)
                if routeTime != math.inf:
                    break
                # if there is no time to get back to depot, remove last added customer
                unUsedCustomers.append(customers[-1])
                del customers[-1]

            # add route to solution
            truck = solution.initNewTruck()
            truck.setCustomers(customers)
            truck.timeOnTheRoute = routeTime
            truck.leftCapacity = leftCapacity

            # Start new route
            currentTime = 0
            currentCapacity = problem.vehicleCapacity
            currentCustomer = problem.depot
            customers = []

            # if we used all customers that is it
            if not unUsedCustomers:
                break

    return solution


