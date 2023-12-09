from vns import VNS
import numpy as np
from random import seed
from copy import deepcopy
from multiprocessing import Pool
from IO import *
from util import *
import time
import matplotlib.pyplot as plt
seed(3)


with open('D:\\Code\\ttss\\data\\OR-Library\\unconstrained_efficient_frontiers\\portef5.txt', 'r') as file:
    data = getUnconstrainedFrontierData(file)
x = []
y = []
for point in data:
    x.append(point[1])
    y.append(point[0])
plt.plot(x, y, label="UCEF")
# plt.gca().ticklabel_format(useMathText=True)
plt.ticklabel_format(useMathText=True, axis='both', scilimits=(-3,-3) )
plt.ylabel('Return')
plt.xlabel('Variance')
# plt.show()


with open('data\\OR-Library\\format_data\\port5.txt', 'r') as file:
    data = [line.strip("\n") for line in file.readlines()]

meanReturnVector, standardDeviationVector, covMatrix, corrMatrix = processingORLibraryData(data)

if __name__ == '__main__': 
    processes  = []
    startTime = time.time()
    numberScalesLamda = 100
    maxIter = 10
    max_processes = 4
    results_async = []
    startTime = time.time()
    with Pool(processes=max_processes) as pool:
        for lamda in np.linspace(0, 1, numberScalesLamda):
            vnsAlgo = VNS(maxIter=maxIter, poolLocalSearchLevel=3, poolShakingLevel=3)
            results_async.append(pool.apply_async(vnsAlgo.solve, args=(10, lamda, deepcopy(meanReturnVector), deepcopy(covMatrix), deepcopy(corrMatrix))))
        results = [result.get() for result in results_async]
        
    meanBestSol = []    
    varBestSol = []
    meanInitSol = []    
    varInitSol = []
    for sol in results:
        print("----------------------------------------------------------")
        bestSol = sol[0]
        # print(bestSol.objectiveFunction)
        # print(bestSol.chosenAssetsList)
        # print(bestSol.proportionOfAssetsList)
        mean, var = getReturnVarOfPortfolio(bestSol.chosenAssetsList, bestSol.proportionOfAssetsList, meanReturnVector, covMatrix)
        meanBestSol.append(mean)
        varBestSol.append(var)
        initialSol = sol[1]
        # print(initialSol.objectiveFunction)
        # print(initialSol.chosenAssetsList)
        # print(initialSol.proportionOfAssetsList)
        mean, var = getReturnVarOfPortfolio(initialSol.chosenAssetsList, initialSol.proportionOfAssetsList, meanReturnVector, covMatrix)
        meanInitSol.append(mean)
        varInitSol.append(var)
        
    print("Parallel time",time.time()- startTime) 
    plt.scatter(varBestSol, meanBestSol, color='blue', label="VNS",marker="x")            
    plt.scatter(varInitSol, meanInitSol,color='red', label="Initial solution",marker="*")            
    plt.legend()  
    plt.savefig('output\\OR-Library\\port.png')
    plt.show()
    

