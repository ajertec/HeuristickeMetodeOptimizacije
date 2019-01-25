import time
import copy

from loadInstance import loadInstance
from solution import addToSolutions, outputSolution
from node import evaluateNode, evaluateNode1, evaluateNode2, addNodeToList


# WIP
# checks if the node state is allowed based on the rules
def allowed(node, vehicles, lanes, vehicleLaneMatrix):
    workingVehicle = vehicles[node["workingVehicleIndex"]][1]

    if vehicleLaneMatrix[workingVehicle["id"] - 1][node["targetLane"]] == 0:
        return False

    for vehicleIndex in node["lanes"][node["targetLane"]]:
        if workingVehicle["series"] != vehicles[vehicleIndex][1]["series"]:

            return False
        else:
            break

    lengthSum = 0.5 * (len(node["lanes"][node["targetLane"]]) - 1)
    for vehicleIndex in node["lanes"][node["targetLane"]]:
        lengthSum = lengthSum + vehicles[vehicleIndex][1]["length"]

    if lengthSum > lanes[node["targetLane"]]["length"]:
        return False

    for laneIndex in range(len(lanes)):
        if len(lanes[laneIndex]["blocked"]) == 0:
            continue

        blockingVehicles = node["lanes"][laneIndex]
        if len(blockingVehicles) == 0:
            continue

        lastInBlockingIndex = blockingVehicles[len(blockingVehicles) - 1]

        for blockedNumber in lanes[laneIndex]["blocked"]:
            blockedIndex = blockedNumber - 1

            blockedVehicles = node["lanes"][blockedIndex]

            if len(blockedVehicles) == 0:
                continue

            firstInBlockedIndex = blockedVehicles[0]

            if vehicles[lastInBlockingIndex][1]["departureTime"] > vehicles[firstInBlockedIndex][1]["departureTime"]:
                return False

    return True


# WIP
# explores the given node, updates the solutions if it is a solution and nodesToVisit with next steps
def exploreNode(node, vehicles, lanes, vehicleLaneMatrix, solutions, nodesToVisit):

    workingVehicleIndex = node["workingVehicleIndex"]
    print(workingVehicleIndex)
    if workingVehicleIndex == (len(vehicles) - 1):
        addToSolutions(node, solutions)
        return

    workingVehicleIndex = workingVehicleIndex + 1
    for laneIndex in range(len(lanes)):
        newNode = {
            "targetLane": laneIndex,
            "workingVehicleIndex": workingVehicleIndex,
            "lanes": copy.deepcopy(node["lanes"])
        }
        newNode["lanes"][laneIndex].append(workingVehicleIndex)

        if allowed(newNode, vehicles, lanes, vehicleLaneMatrix):
            evaluateNode(newNode, vehicles, lanes)
            addNodeToList(newNode, nodesToVisit)


# checks if there is still time left for the algorithm to run
def stillSomeTimeLeft(unlimited, startTime, timeAllowed):
    if unlimited:
        return True

    if ((time.time() - startTime) < timeAllowed):
        return True
    else:
        print("no time left")
        return False


# WIP
def main():
    vehicles, lanes, vehicleLaneMatrix = loadInstance("instanca1.txt")

    print(len(vehicles))
    print(lanes)
    firstNode = {
        "targetLane": -1,  # also empty, added in exploreNode
        "lanes": [],  # holds all vehicle IDs in particular lane, every node should have it's own instance of this variable, vehicle infos are acquired through vehicles variable
        "workingVehicleIndex": -1
    }

    for i in range(len(lanes)):
        firstNode["lanes"].append([])

    nodesToVisit = []
    solutions = []

    nodesToVisit.append(firstNode)

    startTime = time.time()
    time.clock()
    while nodesToVisit and stillSomeTimeLeft(False, startTime, 1 * 60):
        workingNode = nodesToVisit.pop(0)
        exploreNode(workingNode, vehicles, lanes,
                    vehicleLaneMatrix, solutions, nodesToVisit)

    outputSolution(solutions, vehicles, lanes, "res-1m-i1.txt")


if __name__ == "__main__":
    main()
