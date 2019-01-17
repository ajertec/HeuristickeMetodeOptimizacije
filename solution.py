from node import evaluateNode

# WIP
# adds the node to solutions, possibly sorting them


def addToSolutions(node, solutions):
    evaluateNode(node)
    solutions.append(node)


# WIP
# finds best solution and calls writeSolution
def outputSolution(solutions):
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

    writeSolution(currentBestSolution)


# prints out the solution in the required format
def writeSolution(node, vehicles, filename):

    with open(filename, w) as outfile:

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

