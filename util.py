import numpy as np
import math
from time import time
from vns import VNS

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
    
#  def caculateReturnSolutionOutSample(path, data: DataFrame):
#     matrix = np.loadtxt(path)
#     matrix = matrix.T
#     for windowTime in range(0, len(data), timeRebalance):
#         # data_in  = data.iloc[:startWindow +  windowTime, :]
#         data_out = data.iloc[startWindow + windowTime: startWindow + windowTime+ timeRebalance, :]
        
#         results_async.append(pool.apply_async(runRealworldDataset, args=(data_in, lamda)))
#         if startWindow + windowTime+ timeRebalance >= len(data):
#             break
    
def calculate_sortino_ratio(returns, risk_free_rate = 0):
    # Calculating the average return.
    average_return = np.mean(returns)
 
    # Calculating the downside deviation of the returns.
    downside_returns = [r - risk_free_rate for r in returns if r < risk_free_rate]
    downside_deviation = np.std(downside_returns)
 
    # Calculating the Sortino ratio.
    sortino_ratio = average_return / downside_deviation
 
    # Returning the calculated Sortino ratio.
    return sortino_ratio
    
def calculate_sharpe_ratio(returns):
    # Calculating the average return.
    average_return = np.mean(returns)
 
    # Calculating the standard deviation of the returns.
    std_deviation = np.std(returns)
 
    # Calculating the Sharpe ratio.
    sharpe_ratio = average_return / std_deviation
 
    # Returning the calculated Sharpe ratio.
    return sharpe_ratio    