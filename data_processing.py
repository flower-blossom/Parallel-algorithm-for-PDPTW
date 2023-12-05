import math
import numpy as np
from numpy import ndarray

def processingORLibraryData(data: list) -> [ndarray, ndarray, ndarray, ndarray]:
    numberOfAssets = int(data[0])
    meanReturnVector = np.zeros((numberOfAssets,))
    standardDeviationVector = np.zeros((numberOfAssets,))
    corrMatrix = np.zeros((numberOfAssets, numberOfAssets))
    covMatrix = np.zeros((numberOfAssets, numberOfAssets))
    
    for assetIdx in range(1, 1 + numberOfAssets):
        meanReturn,  standardDeviation = data[assetIdx].split()
        meanReturnVector[assetIdx - 1, 0] = float(meanReturn)
        standardDeviationVector[assetIdx - 1, 1] = float(standardDeviation)
        
    for corrIdx in range(1 + numberOfAssets, len(data)):
        firstAsset, secondAsset, corrValue = data[corrIdx].split()
        corrMatrix[int(firstAsset) - 1, int(secondAsset) - 1] = float(corrValue)
        corrMatrix = np.maximum(corrMatrix, corrMatrix.transpose())
    
    for firstAsset in range(numberOfAssets):
        for secondAsset in range(numberOfAssets):
            covValue = standardDeviationVector[firstAsset] * standardDeviationVector[secondAsset] 
            covMatrix[firstAsset, secondAsset] = covValue * corrMatrix[firstAsset, secondAsset]

    return meanReturnVector, standardDeviationVector, covMatrix, corrMatrix

def processUnconstrainedFrontierORLibraryData(data: list):
    pointsFrontier = [[float(x), float(y)] for x, y in data]
    return pointsFrontier


def calculateSharpeRatio(assetsList, proportionOfAssetsList, expectedArr, std):
    
    xichMa = 0
    sharpeRatio = 0
    avarageReturn = 0
    dim = len(assetsList) 
    for i in range(0, dim):
        idxAsset = assetsList[i]
        avarageReturn += proportionOfAssetsList[i]*expectedArr[idxAsset]
        xichMa += (proportionOfAssetsList[i]) * std[idxAsset]
    sharpeRatio = avarageReturn/xichMa
    return sharpeRatio, avarageReturn, math.sqrt(xichMa)
 
def takeInfoAssetInAPI(sol, expectedVectorIn, stdIn ,covMatrixIn, expectedVectorOut, stdOut, covMatrixOut):
    chosenAssetsList = sol.chosenAssetsList
    proportionOfAssetsList = sol.proportionOfAssetsList
    valueOut = calculateSharpeRatio(chosenAssetsList, proportionOfAssetsList, expectedVectorOut, stdIn)
    print(f"Sharpe Ratio in sample Out: {valueOut[0]}")

    valueIn = calculateSharpeRatio(chosenAssetsList, proportionOfAssetsList, expectedVectorIn, stdOut)
    print(f"Sharpe Ratio in sample In: {valueIn[0]}")


    # Print name assets if it use api data
    if len(covMatrixIn) == 16:
        nameOfAssets = ['BTC_USD', 'ETH_USD', 'XRP_USD', 'ADA_USD', 'TRX_USD', 'SOL_USD', 'UNI_USD', 'AVAX_USD', 'LINK_USD', 'BNB_USD', 'ATOM_USD', 'ETC_USD', 'NEAR_USD', 'FTM_USD', 'DOGE_USD', 'MATIC_USD']
        print(f"Chosen assets: ")
        for idx in range(len(chosenAssetsList)):
            print(f"{nameOfAssets[chosenAssetsList[idx]]} - {round(proportionOfAssetsList[idx]*100, 2)} %")
    elif len(covMatrixIn) == 17: 
        nameOfAssets = ['BTC_USD', 'ETH_USD', 'XRP_USD', 'ADA_USD', 'TRX_USD', 'SOL_USD', 'UNI_USD', 'AVAX_USD', 'LINK_USD', 'BNB_USD', 'ATOM_USD', 'ETC_USD', 'NEAR_USD', 'LUNC_USD', 'FTM_USD', 'DOGE_USD', 'MATIC_USD']
        print(f"Chosen assets: ")
        for idx in range(len(chosenAssetsList)):
            print(f"{nameOfAssets[chosenAssetsList[idx]]} - {round(proportionOfAssetsList[idx]*100, 2)} %")