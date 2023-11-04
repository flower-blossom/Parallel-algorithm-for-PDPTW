from typing import NoReturn
from dataStructure import RouteNode, Route, DataModel, Solution
from copy import deepcopy
from random import choice, seed
import time
seed(1)

def conflictVehicleCapacity(vehicleDict: dict, sequenceRequestProcessed: RouteNode, requestList: RouteNode) -> bool:
    vehicleCapacity = vehicleDict["capacity"]
    vehicleVolume = vehicleDict["volume"]
    currentCapacity = 0
    currentVolume = 0

    for statusRequest in sequenceRequestProcessed:
        requestDict = requestList[abs(statusRequest)]
        if statusRequest > 0:
            currentCapacity += requestDict["weight"]
            currentVolume += requestDict["volume"]
        else:
            currentCapacity -= requestDict["weight"]
            currentVolume -= requestDict["volume"]
        if currentVolume > vehicleVolume or currentCapacity > vehicleCapacity:
            return True
    return False


def isSmallerEqualNumber(firstNumber: int, secondNumber: int) -> int:
    return firstNumber <= secondNumber


def takeTimeStart(currentTime: int, time: int) -> int:
    """ Return time to start process request"""
    if currentTime > time:
        return currentTime, 0
    else:
        return time, time - currentTime
       


class firstVersionGreedy:
    
    def __init__(self, timeLimit=290) -> None:
        self.timeLimit = timeLimit

    def estimateTimeMoving(self, distance: int, velocity: int) -> int:
        return int(distance/velocity*3600)

    def pickVehicle(self,
                    candidateVehicle: RouteNode,
                    vehicleList: RouteNode,
                    locationOfVehicle: RouteNode,
                    numberOfRoute: int) -> dict:
        vehiclePicked = choice(candidateVehicle)
        candidateVehicle.remove(vehiclePicked)
        vehicleObject = vehicleList[vehiclePicked]
        locationOfVehicle[vehiclePicked] = numberOfRoute
        return vehicleObject

    def addFirstNodeRoute(self,
                          newRoute: Route,) -> NoReturn:
        vehicleDict = newRoute.vehicleDict
        startVehicleNode = RouteNode(idx=0,
                                     idHub=vehicleDict["startIdHub"],
                                     timeCome=vehicleDict["startTime"],
                                     timeGo=vehicleDict["startTime"],
                                     requestProcessStatus=[],
                                     timeRequestProcessing=list(),)
        newRoute.routeNodeList.append(startVehicleNode)

    def createFirstNode(self, route: Route) -> RouteNode:
        vehicleDict = route.vehicleDict
        return RouteNode(idx=0,
                         idHub=vehicleDict["startIdHub"],
                         timeCome=vehicleDict["startTime"],
                         timeGo=vehicleDict["startTime"],
                         requestProcessStatus=[],
                         timeRequestProcessing=list(),)

    def addEndNode(self, routeNodeList: RouteNode, vehicleInfoDict: dict, distanceMatrix: RouteNode) -> int:
        lastNode = routeNodeList[-1]
        startHub = vehicleInfoDict["startIdHub"]
        timeRequestProcessing = lastNode.timeRequestProcessing
        lastTime = 0
        if startHub != lastNode.idHub:
            # create nod to moving new hub
            distance = distanceMatrix[lastNode.idHub][startHub]
            movingTime = self.estimateTimeMoving(
                distance, vehicleInfoDict["velocity"])
            timeToComeBackHub = lastNode.timeGo + movingTime
            comeBackNode = RouteNode(lastNode.idx + 1, startHub, timeToComeBackHub, timeToComeBackHub, [],
                                     timeRequestProcessing=list())
            routeNodeList.append(comeBackNode)
            lastTime = timeToComeBackHub
        else:
            if len(timeRequestProcessing) != 0:
                lastTime = lastNode.timeRequestProcessing[-1][1]
            else:
                lastTime = lastNode.timeGo
        return (vehicleInfoDict["endTime"] - lastTime)

    def checkValidTimePartRoute(self, startIdx: int, nextOrderOfRequest: list, beforeNode: RouteNode,
                                vehicleDict: dict, requestList: RouteNode, distanceMatrix: RouteNode,
                                weightOfWaitTime=1, weightOfMovingTime=1, weightToDue=-1) -> (bool, RouteNode):
        """
        Check part of Route and return if is true
        """
        # locationOfProcessRequest = []
        usingTime = 0
        endTimeVehicle = vehicleDict["endTime"]
        estimatePartNodeList = [deepcopy(beforeNode)]
        beforeNode = estimatePartNodeList[-1]

        for indexRequest in range(startIdx, len(nextOrderOfRequest)):
            statusRequest = nextOrderOfRequest[indexRequest]
        # for statusRequest in nextOrderOfRequest:
            usingTime += weightOfMovingTime * self.processRequest(statusRequest, beforeNode, estimatePartNodeList,
                                                             vehicleDict, requestList, distanceMatrix)
            beforeNode = estimatePartNodeList[-1]
            if isSmallerEqualNumber(beforeNode.timeGo, endTimeVehicle) is False:
                return False, None, 0
            stopCondition, waitTime = self.performTheProcessRequest(
                beforeNode, requestList)
            if stopCondition is False:
                return False, None, 0
            usingTime += weightOfWaitTime * waitTime
        usingTime += weightToDue * \
            self.addEndNode(estimatePartNodeList, vehicleDict, distanceMatrix)
        return isSmallerEqualNumber(estimatePartNodeList[-1].timeGo, endTimeVehicle), estimatePartNodeList, usingTime

    def findPlaceToInsert(self,
                          idx, locationOfProcessRequest, statusRequest: int, currentNodeList: list,
                          route: Route,
                          requestList: RouteNode,
                          distanceMatrix: RouteNode) -> (int, int, RouteNode):

        # routeNodeList = route.routeNodeList
        vehicleDict = route.vehicleDict
        orderOfRequestProcessed = route.orderOfRequestProcessed
        # locationOfProcessRequest = route.locationOfProcessRequest
        minUsingTime = float("inf")
        idxToInsert = -1
        bestNodeList = 0
        changeIdx = abs(route.routeNodeList[0].idx - currentNodeList[0].idx)

        # index of delivery < index pickup
        for index in range(idx, len(orderOfRequestProcessed) + 1):
            if len(locationOfProcessRequest) == 0 or index == 0:
                beforeNode = self.createFirstNode(route)
                # beforeNode = addFirstNodeRoute(route)
            else:
                # changeIdx = abs(route.routeNodeList[0].idx - currentNodeList[0].idx)
                beforeRequest = locationOfProcessRequest[orderOfRequestProcessed[index - 1]]
                beforeNode = currentNodeList[beforeRequest - changeIdx]

            orderOfRequestProcessed.insert(index, statusRequest)

            if conflictVehicleCapacity(vehicleDict, orderOfRequestProcessed, requestList) is False:
                conditionRoute, tempNodeList, usingTime = self.checkValidTimePartRoute(index,
                                                                                       orderOfRequestProcessed,
                                                                                       beforeNode,
                                                                                       vehicleDict,
                                                                                       requestList,
                                                                                       distanceMatrix)
                if conditionRoute is True:
                    if usingTime < minUsingTime:
                        minUsingTime = usingTime
                        idxToInsert = index
                        bestNodeList = tempNodeList
            orderOfRequestProcessed.pop(index)
        return idxToInsert, minUsingTime, bestNodeList

    def updateLocationProcessRequest(self, locationOfProcessRequest: dict, nodelist: list,) -> NoReturn:
        for node in nodelist:
            for requestStatus in node.requestProcessStatus:
                locationOfProcessRequest[requestStatus] = node.idx

    def addNewRequest(self,
                      route: Route,
                      requestIndexCandidate: RouteNode,
                      requestInfoList: RouteNode,
                      distanceMatrix: RouteNode,
                      ) -> bool:
        """
        try to add new request 
        """

        orderOfRequestProcessed = route.orderOfRequestProcessed
        routeNodeList = route.routeNodeList
        locationOfProcessRequest = route.locationOfProcessRequest

        # Tổng thời gian di chuyển và chờ đợi = thời gian sử dụng
        minCost = float("inf")
        selectedRequest = -1
        idxInsertPickUp = 0
        idxInsertDelivery = 0

        for requestIdx in requestIndexCandidate:
            pickupStatus = requestIdx
            deliveryStatus = -requestIdx

            # try to insert pickup request
            idxPickUp, _, tempNodePickUp = self.findPlaceToInsert(0, locationOfProcessRequest, pickupStatus, routeNodeList,
                                                                  route, requestInfoList, distanceMatrix)
            if idxPickUp != -1:
                tempLocation = dict()
                self.updateLocationProcessRequest(tempLocation, tempNodePickUp)

                orderOfRequestProcessed.insert(idxPickUp, pickupStatus)

                # try to insert delivery request
                idxDelivery, cost, _ = self.findPlaceToInsert(idxPickUp + 1, tempLocation, deliveryStatus, tempNodePickUp,
                                                              route, requestInfoList,
                                                              distanceMatrix)
                orderOfRequestProcessed.pop(idxPickUp)
                # locationOfProcessRequest.pop(pickupStatus)
                if cost < minCost:
                    selectedRequest = requestIdx
                    idxInsertPickUp = idxPickUp
                    idxInsertDelivery = idxDelivery
                    minCost = cost

        if selectedRequest == -1:
            return False

        requestIndexCandidate.remove(selectedRequest)
        orderOfRequestProcessed.insert(idxInsertPickUp, selectedRequest)

        if len(locationOfProcessRequest) == 0:
            beforeNode = routeNodeList[-1]
        else:
            if idxInsertPickUp != 0:
                requestBefore = orderOfRequestProcessed[idxInsertPickUp - 1]
                beforeNode = routeNodeList[locationOfProcessRequest[requestBefore]]
            else:
                beforeNode = self.createFirstNode(route)

        orderOfRequestProcessed.insert(idxInsertDelivery, -selectedRequest)
        _, tempList, _ = self.checkValidTimePartRoute(0, orderOfRequestProcessed,
                                                      self.createFirstNode(
                                                          route), route.vehicleDict,
                                                      requestInfoList, distanceMatrix)
        route.routeNodeList = tempList
        self.updateLocationProcessRequest(
            locationOfProcessRequest, route.routeNodeList)

    def processRequest(self, statusRequest: int,
                       lastNode: Route,
                       routeNodeList: list,
                       vehicleInfoDict: dict,
                       requestList: list,
                       distanceMatrix: list,
                       ) -> int:
        """
        Create node to process request
        """
        usingTime = 0
        currentHub = lastNode.idHub
        requestObject = requestList[abs(statusRequest)]

        nextHub = 0
        if statusRequest > 0:
            nextHub = requestObject["pickupIdHub"]
        if statusRequest < 0:
            nextHub = requestObject["deliveryIdHub"]

        if nextHub == currentHub:
            # add request to last node
            lastNode.requestProcessStatus.append(statusRequest)
        else:
            # create and moving to new node
            distance = distanceMatrix[currentHub][nextHub]
            movingTime = self.estimateTimeMoving(
                distance, vehicleInfoDict["velocity"])
            timeGoToHub = lastNode.timeGo + movingTime
            usingTime += movingTime
            newNode = RouteNode(idx=lastNode.idx + 1,
                                idHub=nextHub,
                                timeCome=timeGoToHub,
                                timeGo=timeGoToHub,
                                requestProcessStatus=[statusRequest],
                                timeRequestProcessing=list(),)
            routeNodeList.append(newNode)
        return usingTime

    def performTheProcessRequest(self, node: RouteNode, requestList: RouteNode) -> (bool, int):
        """ 
        Try to update time to delivery or pickup request and time 
        to go out current hub 
        """

        requestProcessStatus = node.requestProcessStatus
        timeRequestProcessing = node.timeRequestProcessing
        timeRequestProcessing.clear()
        timeCome = node.timeCome
        lastTimeAction = node.timeCome
        startProcessTime = 0
        endProcessTime = 0
        loadingTime = 0
        waitTime = 0

        for requestStatusIdx in requestProcessStatus:
            requestInfoDict = requestList[abs(requestStatusIdx)]
            if len(timeRequestProcessing) == 0:
                # is first request process
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime, waitTime = takeTimeStart(
                        timeCome, requestInfoDict["pickupTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                        return False, 0
                    loadingTime = requestInfoDict["pickupLoadingTime"]
                else:
                    # delivery request
                    startProcessTime, waitTime = takeTimeStart(
                        timeCome, requestInfoDict["deliveryTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                        return False, 0
                    loadingTime = requestInfoDict["deliveryLoadingTime"]
            else:
                lastTimeRequest = timeRequestProcessing[-1][1]
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime, waitTime = takeTimeStart(
                        lastTimeRequest, requestInfoDict["pickupTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                        return False, 0
                    loadingTime = requestInfoDict["pickupLoadingTime"]
                else:
                    # delivery request
                    startProcessTime, waitTime = takeTimeStart(
                        lastTimeRequest, requestInfoDict["deliveryTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                        return False, 0
                    loadingTime = requestInfoDict["deliveryLoadingTime"]

            endProcessTime = startProcessTime + loadingTime

            timeRequestProcessing.append([startProcessTime, endProcessTime])
            lastTimeAction = endProcessTime
        node.timeGo = lastTimeAction
        return True, waitTime

    def getNewRoute(self,
                    vehicleDict: dict,
                    requestInfoList: RouteNode,
                    candidateRequests: RouteNode,
                    distanceMatrix: RouteNode,
                    timeStart: int) -> Route:
        newRoute = Route(list(), vehicleDict, list())
        self.addFirstNodeRoute(newRoute)

        while True:
            stopCondition = self.addNewRequest(newRoute, candidateRequests,
                                               requestInfoList, distanceMatrix)

            if stopCondition is False:
                break
            if time.time() - timeStart > 290:
                break
        return newRoute

    def main(self,
             solutionArr: RouteNode,
             dataModel: DataModel,
             candidateVehicle: RouteNode,
             candidateRequests: RouteNode,
             locationOfVehicle: RouteNode,
             timeStart: int) -> NoReturn:
        """ Create new Route through loop"""

        distanceMatrix = dataModel.distanceMatrix
        vehicleList = dataModel.vehicleList
        requestList = dataModel.requestList
        numberOfRoute = 0

        while True:
            vehicleDict = self.pickVehicle(
                candidateVehicle, vehicleList, locationOfVehicle, numberOfRoute)
            solutionArr.append(self.getNewRoute(vehicleDict,
                                                requestList,
                                                candidateRequests,
                                                distanceMatrix,
                                                timeStart))
            # solutionArr.append(newRoute)
            numberOfRoute += 1
            if len(candidateVehicle) == 0 or len(candidateRequests) == 0:
                break
            if time.time() - timeStart > 290:
                break

    def solve(self, dataModel: DataModel) -> Solution:
        timeStart = time.time()
        solutionArr = list()
        candidateRequests = [i for i in range(1, len(dataModel.requestList))]
        candidateVehicle = [i for i in range(len(dataModel.vehicleList))]
        locationOfVehicle = [-1 for _ in range(len(dataModel.vehicleList))]
        self.main(solutionArr, dataModel, candidateVehicle,
                  candidateRequests, locationOfVehicle, timeStart)
        initialSolution = Solution(solutionArr, locationOfVehicle)
        initialSolution.updateCostFuction(dataModel)
        return initialSolution





class secondVersionGreedy:
    
    def __init__(self, timeLimit=290) -> None:
        self.timeLimit = timeLimit

    def estimateTimeMoving(self, distance: int, velocity: int) -> int:
        return int(distance/velocity*3600)

    def pickVehicle(self,candidateVehicle: list,
                    vehicleList: list,
                    locationOfVehicle: list,
                    numberOfRoute: int) -> dict:
        vehiclePicked = choice(candidateVehicle)
        candidateVehicle.remove(vehiclePicked)
        vehicleObject = vehicleList[vehiclePicked]
        locationOfVehicle[vehiclePicked] = numberOfRoute
        return vehicleObject

    def addFirstNodeRoute(self, newRoute: Route,) -> NoReturn:
        vehicleDict = newRoute.vehicleDict
        startVehicleNode = RouteNode(0, idHub=vehicleDict["startIdHub"],
                                     timeCome=vehicleDict["startTime"],
                                     timeGo=vehicleDict["startTime"],
                                     requestProcessStatus=[],
                                     timeRequestProcessing=list(),)
        newRoute.routeNodeList.append(startVehicleNode)

    def addEndNode(self, routeNodeList: list, vehicleInfoDict: dict, distanceMatrix: list, weightToDue=-1) -> int:
        lastNode = routeNodeList[-1]
        startHub = vehicleInfoDict["startIdHub"]
        if startHub != lastNode.idHub:
            distance = distanceMatrix[lastNode.idHub][startHub]
            movingTime = self.estimateTimeMoving(
                distance, vehicleInfoDict["velocity"])
            timeToComeBackHub = lastNode.timeGo + movingTime
            comeBackNode = RouteNode(0, startHub, timeToComeBackHub, timeToComeBackHub, [],
                                     timeRequestProcessing=dict())
            routeNodeList.append(comeBackNode)
            return weightToDue * (vehicleInfoDict["endTime"] - timeToComeBackHub)
        else:
            return weightToDue*(vehicleInfoDict["endTime"] - lastNode.timeRequestProcessing[-1][1])

    def checkValidTimePartRoute(self, nextOrderOfRequest: list, lastNode: RouteNode,
                                vehicleDict: dict, requestList: list, distanceMatrix: list) -> (bool, list):
        usingTime = 0
        estimatePartNodeList = [deepcopy(lastNode)]
        endTimeVehicle = vehicleDict["endTime"]
        lastNode = estimatePartNodeList[-1]
        for statusRequest in nextOrderOfRequest:
            usingTime += self.processRequest(statusRequest, lastNode, estimatePartNodeList,
                                        vehicleDict, requestList, distanceMatrix)
            lastNode = estimatePartNodeList[-1]
            if isSmallerEqualNumber(lastNode.timeGo, endTimeVehicle) is False:
                return False, None, 0
            stopCondition, waitTime = self.performTheProcessRequest(
                lastNode, requestList)
            if stopCondition is False:
                return False, None, 0
            usingTime += waitTime
        usingTime += self.addEndNode(estimatePartNodeList,
                                vehicleDict, distanceMatrix)

        return isSmallerEqualNumber(estimatePartNodeList[-1].timeGo, endTimeVehicle), estimatePartNodeList, usingTime

    def findPlaceToInsert(self, statusRequest: int, orderOfRequestProcessed: list,
                          beforeNode: RouteNode, vehicleDict: dict,
                          requestList: list, distanceMatrix: list) -> (int, int):
        minUsingTime = float("inf")
        idxToInsert = -1
        startIdx = 0

        if statusRequest < 0:
            startIdx = orderOfRequestProcessed.index(abs(statusRequest)) + 1

        # index of delivery < index pickup
        for index in range(startIdx, len(orderOfRequestProcessed) + 1):
            orderOfRequestProcessed.insert(index, statusRequest)
            if conflictVehicleCapacity(vehicleDict, orderOfRequestProcessed, requestList) is False:
                conditionRoute, _, usingTime = self.checkValidTimePartRoute(orderOfRequestProcessed,
                                                                       beforeNode,
                                                                       vehicleDict,
                                                                       requestList,
                                                                       distanceMatrix)
                if conditionRoute is True:
                    if usingTime < minUsingTime:
                        minUsingTime = usingTime
                        idxToInsert = index
            orderOfRequestProcessed.pop(index)
        return idxToInsert, minUsingTime

    def addNewRequest(self,
                      route: Route,
                      vehicleDict: dict,
                      requestIndexCandidate: list,
                      requestList: list,
                      distanceMatrix: list,
                      ) -> bool:
        """
        try to add new request 
        """
        routeNodeList = route.routeNodeList
        orderOfRequestProcessed = route.orderOfRequestProcessed

        # Tổng thời gian di chuyển và chờ đợi = thời gian sử dụng
        minCost = float("inf")
        stopCondition = False
        selectedRequest = -1
        idxInsertPickUp = 0
        idxInsertDelivery = 0

        for requestIdx in requestIndexCandidate:
            pickupStatus = requestIdx
            deliveryStatus = -requestIdx

            # try to insert pickup request
            beforeNode = routeNodeList[-1]
            idxPickUp, _ = self.findPlaceToInsert(pickupStatus, orderOfRequestProcessed, beforeNode,
                                             vehicleDict, requestList, distanceMatrix)
            if idxPickUp != -1:
                orderOfRequestProcessed.insert(idxPickUp, pickupStatus)
                # try to insert delivery request
                beforeNode = routeNodeList[-1]
                idxDelivery, cost = self.findPlaceToInsert(deliveryStatus, orderOfRequestProcessed, beforeNode,
                                                      vehicleDict, requestList, distanceMatrix)
                # print(cost)
                orderOfRequestProcessed.pop(idxPickUp)
                if cost < minCost:
                    selectedRequest = requestIdx
                    idxInsertPickUp = idxPickUp
                    idxInsertDelivery = idxDelivery
                    minCost = cost
        # timeFrame =

        if selectedRequest == -1:
            return stopCondition
        requestIndexCandidate.remove(selectedRequest)
        orderOfRequestProcessed.insert(idxInsertPickUp, selectedRequest)
        orderOfRequestProcessed.insert(idxInsertDelivery, -selectedRequest)

    def processRequest(self,
                       statusRequest: int,
                       lastNode: RouteNode,
                       routeNodeList: list,
                       vehicleInfoDict: dict,
                       requestList: list,
                       distanceMatrix: list) -> int:
        """
        Create node to process request
        """
        usingTime = 0
        currentHub = lastNode.idHub
        requestObject = requestList[abs(statusRequest)]

        nextHub = 0
        if statusRequest > 0:
            nextHub = requestObject["pickupIdHub"]
        if statusRequest < 0:
            nextHub = requestObject["deliveryIdHub"]

        if nextHub == currentHub:
            # add request to last node
            lastNode.requestProcessStatus.append(statusRequest)
        else:
            # create and moving to new node
            distance = distanceMatrix[currentHub][nextHub]
            movingTime = self.estimateTimeMoving(
                distance, vehicleInfoDict["velocity"])
            timeGoToHub = lastNode.timeGo + movingTime
            usingTime += timeGoToHub
            newNode = RouteNode(0, idHub=nextHub,
                                timeCome=timeGoToHub,
                                timeGo=timeGoToHub,
                                requestProcessStatus=[statusRequest],
                                timeRequestProcessing=list(),)
            routeNodeList.append(newNode)
        return usingTime

    def performTheProcessRequest(self, node: RouteNode, requestList: list) -> (bool, int):
        """ 
        Try to update time to delivery or pickup request and time 
        to go out current hub 
        """

        usingTime = 0
        requestProcessStatus = node.requestProcessStatus
        timeRequestProcessing = node.timeRequestProcessing
        timeRequestProcessing.clear()
        timeCome = node.timeCome
        lastTimeAction = node.timeCome
        startProcessTime = 0
        endProcessTime = 0
        loadingTime = 0
        waitTime = 0

        for requestStatusIdx in requestProcessStatus:
            requestInfoDict = requestList[abs(requestStatusIdx)]
            if len(timeRequestProcessing) == 0:
                # is first request process
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime, waitTime = takeTimeStart(
                        timeCome, requestInfoDict["pickupTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                        return False, 0
                    loadingTime = requestInfoDict["pickupLoadingTime"]
                else:
                    # delivery request
                    startProcessTime, waitTime = takeTimeStart(
                        timeCome, requestInfoDict["deliveryTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                        return False, 0
                    loadingTime = requestInfoDict["deliveryLoadingTime"]
            else:
                lastTimeRequest = timeRequestProcessing[-1][1]
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime, waitTime = takeTimeStart(
                        lastTimeRequest, requestInfoDict["pickupTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                        return False, 0
                    loadingTime = requestInfoDict["pickupLoadingTime"]
                else:
                    # delivery request
                    startProcessTime, waitTime = takeTimeStart(
                        lastTimeRequest, requestInfoDict["deliveryTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                        return False, 0
                    loadingTime = requestInfoDict["deliveryLoadingTime"]

            usingTime += waitTime
            endProcessTime = startProcessTime + loadingTime

            timeRequestProcessing.append([startProcessTime, endProcessTime])
            lastTimeAction = endProcessTime
        node.timeGo = lastTimeAction
        return True, usingTime

    def getNewRoute(self,
                    vehicleDict: dict,
                    requestInfoList: list,
                    candidateRequests: list,
                    distanceMatrix: list,
                    timeStart: int) -> Route:
        newRoute = Route(list(), vehicleDict, list())
        self.addFirstNodeRoute(newRoute)

        while True:
            stopCondition = self.addNewRequest(newRoute, vehicleDict, candidateRequests,
                                          requestInfoList, distanceMatrix)

            if stopCondition is False:
                break
            if time.time() - timeStart > 290:
                break
        _, newRoute.routeNodeList, _ = self.checkValidTimePartRoute(newRoute.orderOfRequestProcessed,
                                                               newRoute.routeNodeList[-1],
                                                               vehicleDict,
                                                               requestInfoList,
                                                               distanceMatrix)
        return newRoute

    def main(self, solutionArr: list,
             dataModel: DataModel,
             candidateVehicle: list,
             candidateRequests: list,
             locationOfVehicle: list,
             timeStart: int
             ) -> NoReturn:
        """ Create new Route through loop"""

        distanceMatrix = dataModel.distanceMatrix
        vehicleList = dataModel.vehicleList
        requestList = dataModel.requestList
        numberOfRoute = 0
        while True:
            vehicleDict = self.pickVehicle(
                candidateVehicle, vehicleList, locationOfVehicle, numberOfRoute)
            newRoute = self.getNewRoute(vehicleDict,
                                   requestList,
                                   candidateRequests,
                                   distanceMatrix,
                                   timeStart)
            solutionArr.append(newRoute)
            numberOfRoute += 1
            if len(candidateVehicle) == 0 or len(candidateRequests) == 0:
                break
            if time.time() - timeStart > 290:
                break

    def solve(self, dataModel: DataModel) -> Solution:
        timeStart = time.time()
        solutionArr = list()
        candidateRequests = [i for i in range(1, len(dataModel.requestList))]
        candidateVehicle = [i for i in range(len(dataModel.vehicleList))]
        locationOfVehicle = [-1 for _ in range(len(dataModel.vehicleList))]
        self.main(solutionArr, dataModel, candidateVehicle,
             candidateRequests, locationOfVehicle, timeStart)
        initialSolution = Solution(solutionArr, locationOfVehicle)
        initialSolution.updateCostFuction(dataModel)
        return initialSolution



class solver:
    def __init__(self) -> None:
        pass
    
    def solving(self, dataModel: DataModel):
        if len(dataModel.requestList) - 3 > 500:
            sol = firstVersionGreedy().solve(dataModel)
        else:     
            sol = secondVersionGreedy().solve(dataModel)
            
        return sol
    
