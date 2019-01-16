from loadInstance import loadInstance
from evaluators import evaluator1, evaluator2


def allowed(node, vehicles, lanes, vehicleLaneMatrix):


def exploreNode(node, vehicles, lanes, vehicleLaneMatrix, solutions):
    if not allowed(node, vehicles, lanes, vehicleLaneMatrix):
        return

    print("allowed")


def main():
    sortedVehicles, lanes, vehicleLaneMatrix = loadInstance("instanca1.txt")


if __name__ == "__main__":
    main()
