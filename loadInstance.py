import numpy as np
import pandas as pd


def loadInstance(fileName): 

    with open(fileName, "r") as infile:
        lines = infile.readlines()

    linesArrayed = []
    for line in lines[:]:
        linesArrayed.append(line.split())

    vehicleAmount = int(linesArrayed[0][0])
    laneAmount = int(linesArrayed[1][0])

    vehicleLengths = np.array(linesArrayed[3], dtype = int)

    vehicleSeries = np.array(linesArrayed[5], dtype = int)

    vehicleLaneMatrix = np.array(linesArrayed[7 : 7 + vehicleAmount], dtype = int)

    assert vehicleLaneMatrix.shape[0] == vehicleAmount
    assert vehicleLaneMatrix.shape[1] == laneAmount

    laneLengths =  np.array(linesArrayed[7 + vehicleAmount + 1], dtype = int)

    departureTimes = np.array(linesArrayed[7 + vehicleAmount + 3], dtype = int)

    vehicleLayouts = np.array(linesArrayed[7 + vehicleAmount + 5], dtype = int)

    blockedLaneDefinitions = linesArrayed[7 + vehicleAmount + 5 + 2:]

    vehicles = {}

    for vehicleNumber in range(0, vehicleAmount):
        vehicles[vehicleNumber] = {
            "id": vehicleNumber + 1,
            "length": vehicleLengths[vehicleNumber], 
            "series": vehicleSeries[vehicleNumber], 
            "departureTime": departureTimes[vehicleNumber], 
            "layout":vehicleLayouts[vehicleNumber]
            }
    
    sortedVehicles = sorted(vehicles.items(), key=lambda kv: kv[1]["departureTime"])

    lanes= {}

    for laneNumber in range(0, laneAmount):
        lanes[laneNumber] = {
            "id": laneNumber + 1,
            "length": laneLengths[laneNumber],
            "blocked": []
        }

    for definition in blockedLaneDefinitions:
        lanes[int(definition[0]) - 1]["blocked"] = np.array(definition[1:], dtype = int)

    return sortedVehicles, lanes, vehicleLaneMatrix


