import numpy as np
from solve import *


def convertTimeToSecond(dateTime: str) -> int:
    timeList = [int(i) for i in dateTime.split(":")]
    return (timeList[0] * 60 + timeList[1]) * 60 + timeList[2]


def convertSecondsToHours(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_format = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return time_format


def createInfoVehicle(vehicleInfo: str) -> dict:
    infoList = vehicleInfo.split()
    infoDict = {
        "startIdHub": int(infoList[0]) - 1,
        "startTime": convertTimeToSecond(infoList[1]),
        "endTime": convertTimeToSecond(infoList[2]),
        "capacity": float(infoList[3]),
        "volume": float(infoList[4]),
        "velocity": float(infoList[5]),
    }
    return infoDict


def createInfoRequest(requestInfo: str) -> dict:
    infoList = requestInfo.split()
    infoDict = {
        "pickupIdHub": int(infoList[0]) - 1,
        "deliveryIdHub": int(infoList[1]) - 1,
        "weight": float(infoList[2]),
        "volume": float(infoList[3]),
        "pickupLoadingTime": int(infoList[4]),
        "deliveryLoadingTime": int(infoList[5]),
        "pickupTime": [convertTimeToSecond(infoList[6]), convertTimeToSecond(infoList[7])],
        "deliveryTime": [convertTimeToSecond(infoList[8]), convertTimeToSecond(infoList[9])],
    }
    return infoDict


def readInputFile(data: RouteNode):
    currentIndex = 0
    numberOfHub = int(data[currentIndex])
    currentIndex += 1

    orderList = []
    orderList.append([])
    vehicleList = []
    distanceMatrix = []

    for hubNumber in range(currentIndex, currentIndex + numberOfHub):
        arr = data[hubNumber]
        distanceMatrix.append(list(map(int, arr.split())))
    # distanceMatrix = np.array(distanceMatrix)
    currentIndex += numberOfHub

    numberOfVehicle = int(data[currentIndex])
    currentIndex += 1

    for orderIdx in range(currentIndex, currentIndex + numberOfVehicle):
        vehicleList.append(createInfoVehicle(data[orderIdx]))
    currentIndex += numberOfVehicle

    numberOfOrder = int(data[currentIndex])
    currentIndex += 1

    for orderIdx in range(currentIndex, currentIndex + numberOfOrder):
        orderList.append(createInfoRequest(data[orderIdx]))

    return DataModel(distanceMatrix, vehicleList, orderList)


def writeVehicleNotUse(vehicle: dict):
    time = convertSecondsToHours(vehicle["startTime"])
    print(1)
    print(f"{vehicle['startIdHub'] + 1} 0 {time} {time}")


def writeRoute(route: Route):
    print(len(route.routeNodeList))
    for node in route.routeNodeList:
        print(f"{node.idHub + 1} {len(node.requestProcessStatus)} {convertSecondsToHours(node.timeCome)} {convertSecondsToHours(node.timeGo)}")
        for idx in range(len(node.requestProcessStatus)):
            # for request in node.requestProcessStatus:
            # for timeProcess in timeRequestProcessing[request][0]:
            print(
                f"{abs(node.requestProcessStatus[idx])} {convertSecondsToHours(node.timeRequestProcessing[idx][0])}")


def writeOutFile(solution: Solution, dataModel: DataModel):
    vehicleList = dataModel.vehicleList
    locationOfVehicle = solution.locationOfVehicle
    routeList = solution.routeList
    for idx, locationRoute in enumerate(locationOfVehicle):
        if locationRoute == -1:
            writeVehicleNotUse(vehicleList[idx])
        else:
            writeRoute(routeList[locationRoute])