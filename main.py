from vns import VNS
from pandas import read_excel
import pandas
import numpy as np
from random import seed
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
    number = 50
    processes  = []
    # pool = Pool(processes=3)
    startTime = time.time()
    maxIter = 30
    for i in range(number):
        vnsAlgo = VNS(maxIter=maxIter, lamda=i/number, poolLocalSearchLevel=3,poolShakingLevel=3)
        p = Process(target=vnsAlgo.solve, args=(10, expectedVector, covMatrix, corrMatrix))
        p.start()
        processes.append(p)
    for t in processes:
        t.join()
    print("Done")
    print("parallel time",time.time()- startTime)
    
    startTime = time.time()
    for i in range(number):
        vnsAlgo = VNS(maxIter=maxIter, lamda=i/number, poolLocalSearchLevel=3,poolShakingLevel=3)
        p = vnsAlgo.solve(10, expectedVector, covMatrix, corrMatrix)

    print("Done")
    print("Sequence time",time.time()- startTime)

