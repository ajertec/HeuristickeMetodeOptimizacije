from node import evaluateNode, evaluateNode1, evaluateNode2


def addToSolutions(node, solutions):
    solutions.append(node)


def filterSolutions(solutions, vehicles, lanes):
    newSolutions = []

    for solution in solutions:
        allowed = True

        for laneIndex in range(len(lanes)):
            if not allowed:
                break

            if len(lanes[laneIndex]["blocked"]) == 0:
                continue

            blockingVehicles = solution["lanes"][laneIndex]
            if len(blockingVehicles) == 0:
                continue

            lastInBlockingIndex = blockingVehicles[len(blockingVehicles) - 1]

            for blockedNumber in lanes[laneIndex]["blocked"]:
                blockedIndex = blockedNumber - 1

                blockedVehicles = solution["lanes"][blockedIndex]

                if len(blockedVehicles) == 0:
                    continue

                firstInBlockedIndex = blockedVehicles[0]

                if vehicles[lastInBlockingIndex][1]["departureTime"] > vehicles[firstInBlockedIndex][1]["departureTime"]:
                    allowed = False
                    break

        if allowed:
            solution["eval1"] = evaluateNode1(solution, vehicles, lanes)
            solution["eval2"] = evaluateNode2(solution, vehicles, lanes)
            newSolutions.append(solution)

    return newSolutions


def outputSolution(solutions, vehicles, lanes, filename):
    print("prior solutions ", len(solutions))
    solutions = filterSolutions(solutions, vehicles, lanes)
    if len(solutions) == 0:
        print("no solution found")
        return

    currentBestSolution = solutions[0]
    currentMaxValue = currentBestSolution["eval2"]/currentBestSolution["eval1"]

    for sol in solutions:
        workingValue = sol["eval2"]/sol["eval1"]
        if currentMaxValue < workingValue:
            currentMaxValue = workingValue
            currentBestSolution = sol

    print(len(solutions))
    writeSolution(currentBestSolution, vehicles, filename)


def writeSolution(node, vehicles, filename):
    print(node)
    with open(filename, "w") as outfile:

        lanesLength = len(node["lanes"])
        j = 0
        for lane in node["lanes"]:
            for vehicleIndex in lane:

                vehicleId = vehicles[vehicleIndex][1]["id"]

                outfile.write(str(vehicleId))
                outfile.write(" ")
            j += 1
            if j != lanesLength:
                outfile.write("\n")
