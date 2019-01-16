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


# WIP
# prints out the solution in the required format
def writeSolution(node):
    print(node)
