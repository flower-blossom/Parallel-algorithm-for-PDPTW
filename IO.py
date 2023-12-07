from numpy import ndarray, maximum, zeros
from util import calculateSharpeRatio
from json import dump

def processingORLibraryData(data: list) -> [ndarray, ndarray, ndarray, ndarray]:
    numberOfAssets = int(data[0])
    meanReturnVector = zeros((numberOfAssets,))
    standardDeviationVector = zeros((numberOfAssets,))
    corrMatrix = zeros((numberOfAssets, numberOfAssets))
    covMatrix = zeros((numberOfAssets, numberOfAssets))
    
    for assetIdx in range(1, 1 + numberOfAssets):
        meanReturn,  standardDeviation = data[assetIdx].split()
        meanReturnVector[assetIdx - 1] = float(meanReturn)
        standardDeviationVector[assetIdx - 1] = float(standardDeviation)
        
    for corrIdx in range(1 + numberOfAssets, len(data)):
        firstAsset, secondAsset, corrValue = data[corrIdx].split()
        corrMatrix[int(firstAsset) - 1, int(secondAsset) - 1] = float(corrValue)
        corrMatrix = maximum(corrMatrix, corrMatrix.transpose())
    
    for firstAsset in range(numberOfAssets):
        for secondAsset in range(numberOfAssets):
            covValue = standardDeviationVector[firstAsset] * standardDeviationVector[secondAsset] 
            covMatrix[firstAsset, secondAsset] = covValue * corrMatrix[firstAsset, secondAsset]

    return meanReturnVector, standardDeviationVector, covMatrix, corrMatrix

def getUnconstrainedFrontierData(file):
    return [ list(map(float, line.strip("\n").split()))  for line in file.readlines()]

 
def takeInfoAssetInAPI(sol, expectedVectorIn, stdIn ,expectedVectorOut, stdOut,):
    chosenAssetsList = sol.chosenAssetsList
    proportionOfAssetsList = sol.proportionOfAssetsList
    valueOut = calculateSharpeRatio(chosenAssetsList, proportionOfAssetsList, expectedVectorOut, stdIn)
    print(f"Sharpe Ratio in sample Out: {valueOut[0]}")

    valueIn = calculateSharpeRatio(chosenAssetsList, proportionOfAssetsList, expectedVectorIn, stdOut)
    print(f"Sharpe Ratio in sample In: {valueIn[0]}")

    # Print name assets if it use api data
    sol = {}
    if len(expectedVectorIn) == 16:
        nameOfAssets = ['BTC_USD', 'ETH_USD', 'XRP_USD', 'ADA_USD', 'TRX_USD', 'SOL_USD', 'UNI_USD', 'AVAX_USD', 'LINK_USD', 'BNB_USD', 'ATOM_USD', 'ETC_USD', 'NEAR_USD', 'FTM_USD', 'DOGE_USD', 'MATIC_USD']
        
        print(f"Chosen assets: ")
        for idx in range(len(chosenAssetsList)):
            sol[nameOfAssets[chosenAssetsList[idx]]] = round(proportionOfAssetsList[idx]*100, 2)
            print(f"{nameOfAssets[chosenAssetsList[idx]]} - {round(proportionOfAssetsList[idx]*100, 2)} %")
            
    elif len(expectedVectorIn) == 17:
         
        nameOfAssets = ['BTC_USD', 'ETH_USD', 'XRP_USD', 'ADA_USD', 'TRX_USD', 'SOL_USD', 'UNI_USD', 'AVAX_USD', 'LINK_USD', 'BNB_USD', 'ATOM_USD', 'ETC_USD', 'NEAR_USD', 'LUNC_USD', 'FTM_USD', 'DOGE_USD', 'MATIC_USD']
        print(f"Chosen assets: ")
        for idx in range(len(chosenAssetsList)):
            print(f"{nameOfAssets[chosenAssetsList[idx]]} - {round(proportionOfAssetsList[idx]*100, 2)} %")
            sol[nameOfAssets[chosenAssetsList[idx]]] = round(proportionOfAssetsList[idx]*100, 2)
    with open('output\\api\\data.json', 'w') as f:
        dump(sol, f)