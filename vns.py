import math
import random
import numpy as np
from numpy import ndarray
from typing import NoReturn
from copy import deepcopy
from qpsolvers import Problem, solve_problem


class Solution:
    def __init__(self, chosenAssetsList: list,) -> None:
        self.chosenAssetsList = chosenAssetsList
        self.proportionOfAssetsList = None
        self.objectiveFunction = None


def executionQP(currentSol: Solution, lamda: float,
                expectedVector: ndarray, covMatrix: ndarray,
                minProportion=0.01, maxProportion=1) -> NoReturn:

    chosenAssetsList = currentSol.chosenAssetsList
    numberOfAssets = len(chosenAssetsList)
    maxProportion = max(maxProportion, 1/numberOfAssets)

    # Create component for quadratic program solver
    P = np.zeros([numberOfAssets, numberOfAssets])
    for idx1, firstAsset in enumerate(chosenAssetsList):
        for idx2, secondAsset in enumerate(chosenAssetsList):
            P[idx1, idx2] = lamda*covMatrix[int(firstAsset), int(secondAsset)]

    q = -(1 - lamda)*np.array([expectedVector[asset] for asset in chosenAssetsList])
    A = np.ones(numberOfAssets)
    b = np.array([1.])
    lb = minProportion * np.ones(numberOfAssets)
    ub = maxProportion * np.ones(numberOfAssets)

    # Solve
    problem = Problem(P=P, q=q, A=A, b=b, lb=lb, ub=ub)
    sol = solve_problem(problem, solver="cvxopt")

    # Update solution
    currentSol.objectiveFunction = sol.obj
    currentSol.proportionOfAssetsList = sol.x


def calculateSharpeRatio(assetsList, proportionOfAssetsList, expectedArr, covMatrix):
    xichMa = 0
    sharpeRatio = 0
    avarageReturn = 0
    dim = len(assetsList)
    for i in range(0, dim):
        idxAsset1 = assetsList[i]
        avarageReturn += proportionOfAssetsList[i]*expectedArr[idxAsset1]
        for j in range(0, dim):
            idxAsset2 = assetsList[j]
            xichMa += (proportionOfAssetsList[i])*(
                proportionOfAssetsList[j])*covMatrix[idxAsset1, idxAsset2]
    sharpeRatio = avarageReturn/math.sqrt(xichMa)
    return sharpeRatio, avarageReturn, math.sqrt(xichMa)


class VNS:
    def __init__(self, maxIter=10000, poolShakingLevel=1, poolLocalSearchLevel=1,) -> None:
        self.maxIter = maxIter
        self.poolShakingLevel: int = poolShakingLevel
        self.poolLocalSearchLevel: int = poolLocalSearchLevel
        self.poolSizeShaking: int = None
        self.poolSizeLocalSearch: int = None
        self.bestSolution: int = None
        self.searchPool: ndarray = None

    def numberAssetsInPool(self, levelPool, numberOfAssetsChoosed, quantityOfAssests) -> int:
        if levelPool <= 1:
            return quantityOfAssests - 1
        else:
            return numberOfAssetsChoosed - 1 + int(quantityOfAssests/levelPool)

    def setPoolSize(self, numberOfAssetsChoosed, quantityOfAssests,) -> NoReturn:
        self.poolSizeLocalSearch = self.numberAssetsInPool(
            self.poolLocalSearchLevel, numberOfAssetsChoosed, quantityOfAssests)
        self.poolSizeShaking = self.numberAssetsInPool(
            self.poolLocalSearchLevel, numberOfAssetsChoosed, quantityOfAssests)

    def createSearchPool(self, lamda: float, expectedVector: ndarray, covMatrix: ndarray, quantityOfAssests) -> NoReturn:
        searchPool = np.zeros((quantityOfAssests, 2))
        thetaArr = np.zeros(quantityOfAssests + 1)
        rhoArr = np.zeros(quantityOfAssests + 1)

        for idxAsset in range(quantityOfAssests):
            rho = sum(covMatrix[idxAsset, secondIdxAsset]
                      for secondIdxAsset in range(quantityOfAssests))
            rhoArr[idxAsset] = 1 + lamda*rho/quantityOfAssests
            thetaArr[idxAsset] = 1 + (1 - lamda)*expectedVector[idxAsset]
        omega = -min(thetaArr)
        psi = -min(rhoArr)

        for idxAsset in range(quantityOfAssests):
            # Save index of asset
            searchPool[idxAsset, 0] = idxAsset
            # save value
            searchPool[idxAsset, 1] = (
                thetaArr[idxAsset] + omega)/(rhoArr[idxAsset] + psi)

        # Sort pool by value
        self.searchPool = searchPool[searchPool[:, 1].argsort()][::-1]

    def initialSolution(self, lamda: float, numberOfAssetsChoosed: int, expectedVector, covMatrix) -> Solution:
        chosenAssetsList = []
        searchPool = self.searchPool
        for num in range(numberOfAssetsChoosed):
            idxAsset, _ = searchPool[num]
            chosenAssetsList.append(int(idxAsset))
        currentSolution = Solution(chosenAssetsList)
        executionQP(currentSolution, lamda, expectedVector, covMatrix,)
        return currentSolution

    def shaking(self, levelNeighbor: int, currentSolution: Solution,) -> NoReturn:
        tempSolutionChosenAssetsList = currentSolution.chosenAssetsList
        chosenAssetsList = currentSolution.chosenAssetsList.copy()
        for _ in range(levelNeighbor):
            chosenAssetsList.remove(random.choice(chosenAssetsList))
            while True:
                newAsset = random.randint(0, self.poolSizeShaking)
                if newAsset not in tempSolutionChosenAssetsList:
                    chosenAssetsList.append(newAsset)
                    break
        return Solution(chosenAssetsList)

    def localSearch(self, lamda:float, currentSolution: Solution, numberOfAssetsChoosed: int,
                    expectedVector, covMatrix) -> Solution:
        tempSolution = deepcopy(currentSolution)
        bestFoundSolution = deepcopy(currentSolution)
        for idx, oldAsset in enumerate(currentSolution.chosenAssetsList):
            for newAssetIdx in range(self.poolSizeLocalSearch):
                if newAssetIdx not in tempSolution.chosenAssetsList:
                    # print(newAssetIdx)
                    tempSolution.chosenAssetsList[idx] = newAssetIdx
                    executionQP(tempSolution, lamda,
                                expectedVector, covMatrix,)
                    # print(f"tempSolution.objectiveFunction: {tempSolution.objectiveFunction}")
                    if bestFoundSolution.objectiveFunction > tempSolution.objectiveFunction:
                        bestFoundSolution = deepcopy(tempSolution)
                    else:
                        tempSolution.chosenAssetsList[idx] = oldAsset     
        return bestFoundSolution

    def solve(self,
              numberOfAssetsChoosed: int, lamda:float ,expectedVector: ndarray,
              covMatrix: ndarray, corMarix: ndarray) -> Solution:
        quantityOfAssests = expectedVector.shape[0]
        self.createSearchPool(lamda, expectedVector, covMatrix, quantityOfAssests)
        self.setPoolSize(numberOfAssetsChoosed,  quantityOfAssests)

        currentSolution = self.initialSolution(lamda, 
            numberOfAssetsChoosed, expectedVector, covMatrix)
        initialSolution = deepcopy(currentSolution)
        self.bestSolution = deepcopy(currentSolution)
        # print(currentSolution.objectiveFunction)
        # print(currentSolution.chosenAssetsList)
        # print(currentSolution.proportionOfAssetsList)
        
        numberLoop = 0
        while True:
            levelNeighbor = 1
            improvementCondition = False
            while levelNeighbor <= numberOfAssetsChoosed:
                solutionShaking = self.shaking(levelNeighbor, currentSolution)
                executionQP(solutionShaking, lamda, expectedVector, covMatrix,)
                numberLoop += 1
                # print(f"solutionShaking: {solutionShaking.objectiveFunction}")
                if currentSolution.objectiveFunction < solutionShaking.objectiveFunction:
                    solutionlocalSearch = self.localSearch(lamda,
                        solutionShaking, numberOfAssetsChoosed, expectedVector, covMatrix)
                    numberLoop += 1
                    # print(f"solutionlocalSearch: {solutionlocalSearch.objectiveFunction}")
                    if solutionlocalSearch.objectiveFunction > solutionShaking.objectiveFunction :
                        
                        currentSolution = solutionlocalSearch
                        levelNeighbor = 1
                    else:
                        levelNeighbor += 1
                else:
                    currentSolution = deepcopy(solutionShaking)
                    levelNeighbor = 1
                if numberLoop > self.maxIter:
                    break
            if self.bestSolution.objectiveFunction > currentSolution.objectiveFunction:
                self.bestSolution = deepcopy(currentSolution)    
            if numberLoop > self.maxIter:
                break                
        return self.bestSolution, initialSolution