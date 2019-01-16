import time

from loadInstance import loadInstance
from evaluators import evaluator1, evaluator2
from solution import addToSolutions, outputSolution


def allowed(node, vehicles, lanes, vehicleLaneMatrix):
    return False


def exploreNode(node, vehicles, lanes, vehicleLaneMatrix, solutions, nodesToVisit):
    if not allowed(node, vehicles, lanes, vehicleLaneMatrix):
        return


def someTimeLeft(unlimited, startTime, timeAllowed):
    if unlimited:
        return True

    return ((time.time() - startTime) < timeAllowed)


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
    while nodesToVisit and someTimeLeft(False, startTime, 60):
        workingNode = nodesToVisit.pop(0)
        exploreNode(workingNode, vehicles, lanes,
                    vehicleLaneMatrix, solutions, nodesToVisit)

    outputSolution(solutions)


if __name__ == "__main__":
    main()
