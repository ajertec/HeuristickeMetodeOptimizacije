from loadInstance import loadInstance
from evaluators import evaluator1, evaluator2


def main():
    sortedVehicles, lanes, vehicleLaneMatrix = loadInstance("instanca1.txt")
    print(vehicleLaneMatrix)


if __name__ == "__main__":
    main()
