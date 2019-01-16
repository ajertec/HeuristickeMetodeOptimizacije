import time

from loadInstance import loadInstance
from solution import addToSolutions, outputSolution
from node import evaluateNode, evaluateNode1, evaluateNode2, addNodeToList


# WIP
# checks if the node state is allowed based on the rules
def allowed(node, vehicles, lanes, vehicleLaneMatrix):
    return False


# WIP
# explores the given node, updates the solutions if it is a solution and nodesToVisit with next steps
def exploreNode(node, vehicles, lanes, vehicleLaneMatrix, solutions, nodesToVisit):
    if not allowed(node, vehicles, lanes, vehicleLaneMatrix):
        return


# checks if there is still time left for the algorithm to run
def stillSomeTimeLeft(unlimited, startTime, timeAllowed):
    if unlimited:
        return True

    return ((time.time() - startTime) < timeAllowed)


# WIP
def main():
    vehicles, lanes, vehicleLaneMatrix = loadInstance("instanca1.txt")

    # make a node here
    firstNode = {

    }

    nodesToVisit = []
    solutions = []

    nodesToVisit.append(firstNode)

    startTime = time.time()
    time.clock()
    while nodesToVisit and stillSomeTimeLeft(False, startTime, 60):
        workingNode = nodesToVisit.pop(0)
        exploreNode(workingNode, vehicles, lanes,
                    vehicleLaneMatrix, solutions, nodesToVisit)

    outputSolution(solutions)


if __name__ == "__main__":
    main()
