


def evaluateNode1(node, vehicles, lanes):

    """Evaluation function : f1p1 + f2p2 + f3p3."""

    lanesAmount = len(lanes)

    totalVehiclesLength = 0
    totalLanesCapacity = 0

    for vehicleIdx in vehicles.keys():
        totalVehiclesLength += vehicles[vehicleIdx]["length"] 

    seriesChangedCounter = 0
    firstSerie = 0 # assuming there is no vehicle with series = 0
    
    usedLanesAmount = 0

    usedCapacity = 0
    totalUsedCapacity = 0

    for laneIdx in range(lanesAmount):
        
        if node["lanes"][laneIdx] != []:
            
            usedLanesAmount += 1

            if firstSerie == 0:
                firstVehicleId = node["lanes"][laneIdx][0]
                firstSerie = vehicles[firstVehicleId - 1]["series"]
            else:
                firstVehicleId = node["lanes"][laneIdx][0]
                temporarySerie = vehicles[firstVehicleId - 1]["series"]
                
                if temporarySerie != firstSerie:
                    seriesChangedCounter += 1
                    firstSerie = temporarySerie

            for vehicleId in node["lanes"][laneIdx]:
            
                usedCapacity += vehicles[vehicleId - 1]["length"]

            laneLength = len(node["lanes"][laneIdx])

            if laneLength >= 2:
                usedCapacity += (laneLength - 1) * 0.5

            totalUsedCapacity += lanes[laneIdx]["length"]


        totalLanesCapacity += lanes[laneIdx]["length"]

    F1 = (seriesChangedCounter)/(usedLanesAmount - 1)
    F2 = usedLanesAmount/lanesAmount 
    F3 = (totalUsedCapacity - usedCapacity)/(totalLanesCapacity-totalVehiclesLength)

    return F1 + F2 + F3


def rewardOrPenalty(v1, v2):
    vr = abs(v1-v2)
    if vr >= 10 and vr <= 20:
        return 15
    if vr > 20:
        return 10
    if vr < 10:
        return -4*(10-vr)

def evaluateNode2(node, vehicles, lanes):

    """Evaluation function : g1r1 + g2r2 + g3r3."""

    lanesAmount = len(lanes)
    vehiclesAmount = len(vehicles)

    #g1
    layoutVehiclePairsCounter = 0
    
    #g2
    g2 = -1 # jer sam brojil prvu traku..
    firstVehicleTmpId = -9999
    lastVehicleTmpId = -9999 
    
    #g3
    rewardPenaltyTotal = 0
    vehiclePairsCounter = 0

    usedLanesAmount = 0

    for laneIdx in range(lanesAmount):
        
        if node["lanes"][laneIdx] != []:

            usedLanesAmount += 1
            
            previousLayout = -9999 

            firstVehicleId = node["lanes"][laneIdx][0]


            lastVehicleId = node["lanes"][laneIdx][-1]
        
            if firstVehicleTmpId == -9999:
                firstVehicleTmpId = firstVehicleId
                lastVehicleTmpId = lastVehicleId 

            if vehicles[firstVehicleId -1]["layout"] == vehicles[lastVehicleTmpId -1]["layout"]:
                g2 += 1
                firstVehicleTmpId = firstVehicleId
                lastVehicleTmpId = lastVehicleId   
            else:
                firstVehicleTmpId = firstVehicleId
                lastVehicleTmpId = lastVehicleId   


            laneLength = len(node["lanes"][laneIdx])
            if laneLength > 2:

                temporaryDepartureTime = -9999
                # nagrada/penal po traci
                rewardPenalty = 0
                  
            for vehicleId in node["lanes"][laneIdx]:

                # G1 ********
                # odredi raspored prvog vozila u traci i spremi za usporedbu
                if previousLayout == -9999:
                    previousLayout = vehicles[vehicleId - 1]["layout"]
                else:
                    # raspored sljedeceg vozila u istoj traci
                    temporaryLayout = vehicles[vehicleId - 1]["layout"]

                    if previousLayout == temporaryLayout:
                        layoutVehiclePairsCounter += 1
                    else:
                        previousLayout = temporaryLayout
                        
                # G3 *********
                if laneLength > 2:
                    if temporaryDepartureTime == -9999:
                        temporaryDepartureTime = vehicles[vehicleId -1 ]["departureTime"]
                    else:     
                        currentDepartureTime = vehicles[vehicleId -1 ]["departureTime"]
                        rewardPenalty += rewardOrPenalty(currentDepartureTime, temporaryDepartureTime)
                        vehiclePairsCounter += 1
                        temporaryDepartureTime = currentDepartureTime
            # G3
            if laneLength == 2:
                vehicleId1 = int(node["lanes"][laneIdx][0])
                vehicleId2 = int(node["lanes"][laneIdx][-1])
            
                departureTimeFirst = vehicles[vehicleId1 - 1]["departureTime"]
                departureTimeLast = vehicles[vehicleId2 - 1]["departureTime"]

                rewardPenalty2 = rewardOrPenalty(departureTimeLast, departureTimeFirst)
                rewardPenaltyTotal += rewardPenalty2
                vehiclePairsCounter += 1
                
            if laneLength > 2:                
                rewardPenaltyTotal += rewardPenalty # g3

    G1 = layoutVehiclePairsCounter/(vehiclesAmount-usedLanesAmount)
    G2 = g2/(usedLanesAmount - 1)
    G3 = rewardPenaltyTotal/(15*vehiclePairsCounter)

    return G1 + G2 + G3


# WIP
# evaluates the node and modifies it with evaluated number for easier sorting
def evaluateNode(node):
    node["eval"] = 1


# WIP
# adds the node to the list and sorts the list
def addNodeToList(node, nodesToVisit):
    nodesToVisit.append(node)
