from vns import VNS
from pandas import read_excel
import numpy as np
from random import seed
from copy import deepcopy
from multiprocessing import Pool, Process
from data_processing import takeInfoAssetInAPI
import time
seed(2)


# path = r'data\realworld dataset\\Datasets\\DowJones\\DowJones.xlsx'
path = r'data\API binance\percentReturnsWeekData.xlsx'
# Read TestData
my_data = read_excel(path, header=None)

# Read API Data
# my_data = read_excel(path, index_col=0, header=0)

percentInOut = 0.2
data_in  = my_data.iloc[:round(percentInOut*my_data.shape[0]), :]
data_out = my_data.iloc[round(percentInOut*my_data.shape[0]):, :]
covMatrixIn = data_in.cov().to_numpy()
corrMatrixIn = data_in.corr().to_numpy()
expectedVectorIn = np.mean(data_in.to_numpy(), axis=0)
stdIn = data_in.std().to_numpy()

covMatrixOut = data_out.cov().to_numpy()
corrMatrixOut = data_out.corr().to_numpy()
expectedVectorOut = np.mean(data_out.to_numpy(), axis=0)
stdOut = data_out.std().to_numpy()


if __name__ == '__main__': 
    processes  = []
    startTime = time.time()
    maxIter = 100
    number = 2
    max_processes = 3
    results_async = []
    startTime = time.time()
    with Pool(processes=max_processes) as pool:
        for i in range(number + 1):
            vnsAlgo = VNS(maxIter=maxIter, poolLocalSearchLevel=5,poolShakingLevel=5)
            results_async.append(pool.apply_async(vnsAlgo.solve, args=(5, i/number, deepcopy(expectedVectorIn), deepcopy(covMatrixIn), deepcopy(corrMatrixIn))))
        results = [result.get() for result in results_async]
    for sol in results:
        print("----------------------------------------------------------")
        takeInfoAssetInAPI(sol, expectedVectorIn, stdIn, covMatrixIn ,expectedVectorOut,stdOut, covMatrixOut)
        
    print("parallel time",time.time()- startTime)   
    

