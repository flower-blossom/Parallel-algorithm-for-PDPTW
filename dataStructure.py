from typing import NoReturn
class DataModel:
    """
    Contains lists about description of problem
    """

    def __init__(self,
                 distanceMatrix: list,
                 vehicleList: list,
                 requestList: list,):
        self.distanceMatrix = distanceMatrix
        self.vehicleList = vehicleList
        self.requestList = requestList


class RouteNode:
    def __init__(self,
                 idx: int,
                 idHub: int,
                 timeCome: int,
                 timeGo: int,
                 requestProcessStatus: list,
                 timeRequestProcessing=list(),
                 ) -> None:
        self.idx = idx
        self.idHub = idHub
        self.timeCome = timeCome
        self.timeGo = timeGo
        self.requestProcessStatus = requestProcessStatus
        self.timeRequestProcessing = timeRequestProcessing
        # self.locationOfProcessRequest: RouteNode = locationOfProcessRequest

    def __repr__(self) -> str:
        return f"idHub: {self.idHub + 1} \n requestProcessStatus: {self.requestProcessStatus} \n {self.timeCome} \n {self.timeGo} \n timeRequestProcessing: {self.timeRequestProcessing} "


class Route:
    """_summary_
    """

    def __init__(self,
                 routeNodeList: RouteNode,
                 vehicleDict: dict,
                 orderOfRequestProcessed: RouteNode = []):
        self.routeNodeList = routeNodeList
        self.vehicleDict = vehicleDict
        self.orderOfRequestProcessed = orderOfRequestProcessed
        self.requestProcess = set()
        self.locationOfProcessRequest: RouteNode = dict()


WEIGHTOFREQUEST = 10**9
WEIGHTOFVEHICLE = 10**6
WEIGHTOFTIME = 1/10**3


def updateRequestProcess(routeList: RouteNode) -> NoReturn:
    for routeObject in routeList:
        for order in routeObject.orderOfRequestProcessed:
            routeObject.requestProcess.add(abs(order))


def totalCostFuction(routeList: RouteNode,
                     quantityOfRequest: int,
                     quantityOfVehicle: int) -> int:
    totalCost = 0
    costTime = 0
    numberOfVehicleServe = 0
    listOrderServe = set()

    for routeObject in routeList:
        costTime += routeObject.routeNodeList[-1].timeCome - \
            routeObject.routeNodeList[0].timeCome
        numberOfVehicleServe += 1
        for order in routeObject.orderOfRequestProcessed:
            listOrderServe.add(abs(order))

    totalCost += WEIGHTOFREQUEST*len(listOrderServe)/quantityOfRequest
    totalCost -= WEIGHTOFVEHICLE*numberOfVehicleServe/quantityOfVehicle
    totalCost -= WEIGHTOFTIME*costTime
    return totalCost


class Solution():
    """
    """

    def __init__(self, routeList: RouteNode, locationOfVehicle: RouteNode):
        self.routeList = routeList
        self.positionOfProcessingRequest: RouteNode = None
        self.locationOfVehicle: RouteNode = locationOfVehicle
        self.weightOfCost = dict()
        self.costFuction = 0

    def updateCostFuction(self, dataModel: DataModel):
        quantityOfRequest = len(dataModel.requestList) - 1
        quantityOfVehicle = len(dataModel.vehicleList)
        self.weightOfCost["request"] = WEIGHTOFREQUEST/quantityOfRequest
        self.weightOfCost["vehicle"] = WEIGHTOFVEHICLE/quantityOfVehicle
        self.costFuction = totalCostFuction(self.routeList,
                                            quantityOfRequest,
                                            quantityOfVehicle)

    def objective(self):
        return self.costFuction

