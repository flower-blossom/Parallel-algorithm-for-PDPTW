import numpy as np
import math
from time import time
from vns import VNS
from random import seed
from multiprocessing import Pool
seed(2)


def calculateSharpeRatio(assetsList, proportionOfAssetsList, expectedVector, std):
    xichMa = 0
    sharpeRatio = 0
    avarageReturn = 0
    dim = len(assetsList) 
    for i in range(0, dim):
        idxAsset = assetsList[i]
        avarageReturn += proportionOfAssetsList[i]*expectedVector[idxAsset]
        xichMa += (proportionOfAssetsList[i]) * std[idxAsset]
    sharpeRatio = avarageReturn/xichMa
    return sharpeRatio, avarageReturn, math.sqrt(xichMa)

def getReturnVarOfPortfolio(assetsList, proportionOfAssetsList, expectedVector, covMatrix):
    variance = 0
    avarageReturn = 0
    for firstAssetidx, firstAsset in enumerate(assetsList):
        avarageReturn += proportionOfAssetsList[firstAssetidx]*expectedVector[firstAsset]
        for secondAssetidx, secondAsset in enumerate(assetsList):
            variance += proportionOfAssetsList[firstAssetidx]*proportionOfAssetsList[secondAssetidx]*covMatrix[firstAsset ,secondAsset]
    return  avarageReturn, variance

def getListSolution(sol, numberOfAsset) -> list:    
    assetsChoosen = [0 for _ in range(numberOfAsset)]
    for idx, asset in enumerate(sol.chosenAssetsList):
        assetsChoosen[asset] =  sol.proportionOfAssetsList[idx]
    return assetsChoosen


def runRealworldDataset(data_in, lamda):
    covMatrix = data_in.cov().to_numpy()
    corrMatrix = data_in.corr().to_numpy()
    expectedVector = np.mean(data_in.to_numpy(), axis=0)
    maxIter = len(expectedVector)

    vnsAlgo = VNS(maxIter=maxIter, poolLocalSearchLevel=3,poolShakingLevel=3)
    sol = vnsAlgo.solve(10, lamda,expectedVector, covMatrix, corrMatrix)
    print("Done! ", time())
    return sol[0]
    
    # def getSolution
# def caculateOutPut():
    