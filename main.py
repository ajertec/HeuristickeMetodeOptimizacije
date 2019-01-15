from loadInstance import loadInstance


def main():
    sortedVehicles, lanes, vehicleLaneMatrix = loadInstance("instanca1.txt")
    print(vehicleLaneMatrix)

if __name__ == "__main__":
    main()
