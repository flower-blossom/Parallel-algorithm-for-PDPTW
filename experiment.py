from vns import VNS
from pandas import read_excel
import numpy as np
from random import seed
from copy import deepcopy
from multiprocessing import Pool, Process
import time
seed(2)


path = r'data\realworld dataset\\Datasets\\DowJones\\DowJones.xlsx'
# path = r'data\API binance\percentReturnsWeekData.xlsx'
# Read TestData
# my_data = pandas.read_excel(path, header=None)

# Read API Data
my_data = read_excel(path, index_col=0, header=0)

percentInOut = 0.2
data_in  = my_data.iloc[:round(percentInOut*my_data.shape[0]), :]
data_out = my_data.iloc[round(percentInOut*my_data.shape[0]):, :]
covMatrix = data_in.cov().to_numpy()
corrMatrix = data_in.corr().to_numpy()

expectedVector = np.mean(data_in.to_numpy(), axis=0)

covMatrixOut = data_out.cov().to_numpy()
corrMatrixOut = data_out.corr().to_numpy()
expectedVectorOut = np.mean(data_out.to_numpy(), axis=0)



if __name__ == '__main__': 
    number = 10
    processes  = []
    startTime = time.time()
    maxIter = 200
    max_processes = 4
    results_async = []
    startTime = time.time()
    with Pool(processes=max_processes) as pool:
        for i in range(number):
            vnsAlgo = VNS(maxIter=maxIter, poolLocalSearchLevel=3,poolShakingLevel=3)
            results_async.append(pool.apply_async(vnsAlgo.solve, args=(10, i/number, deepcopy(expectedVector), deepcopy(covMatrix), deepcopy(corrMatrix))))
        results = [result.get() for result in results_async]
    print("parallel time1",time.time()- startTime)   
    
    startTime = time.time()
    with Pool(processes=max_processes) as pool:
        for i in range(number):
            vnsAlgo = VNS(maxIter=maxIter, poolLocalSearchLevel=3,poolShakingLevel=3)
            results_async.append(pool.apply_async(vnsAlgo.solve, args=(10, i/number,expectedVector, covMatrix, corrMatrix)))
        results = [result.get() for result in results_async]
    print("parallel time2 ",time.time()- startTime) 
    
    startTime = time.time()
    for i in range(number):
        vnsAlgo = VNS(maxIter=maxIter, poolLocalSearchLevel=3,poolShakingLevel=3)
        p = vnsAlgo.solve(10, i/number, expectedVector, covMatrix, corrMatrix)

    print("Done")
    print("Sequence time",time.time()- startTime)

