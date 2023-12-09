from vns import VNS
from pandas import read_excel
import numpy as np
from random import seed
from multiprocessing import Pool
import time
import json
import subprocess

seed(2)



if __name__ == '__main__': 
    path = r'data\realworld dataset\\Datasets\\NASDAQ100\\NASDAQ100.xlsx'
    my_data = read_excel(path, header=0)

    percentInOut = 0.8
    data_in  = my_data.iloc[:round(percentInOut*my_data.shape[0]), :]
    data_out = my_data.iloc[round(percentInOut*my_data.shape[0]):, :]
    covMatrix = data_in.cov().to_numpy()
    corrMatrix = data_in.corr().to_numpy()
    expectedVector = np.mean(data_in.to_numpy(), axis=0)

    expectedVectorOut = np.mean(data_out.to_numpy(), axis=0)
    covMatrixOut = data_out.cov().to_numpy()
    corrMatrixOut = data_out.corr().to_numpy()
    
    timeComparing = {}
    processList = []
    timeComparing["Processes"] = processList
    assetInChoosen = 10
    numberScales = 10
    maxProcessesList = [1, 2, 3, 4, 5]
    loops = [1, 10, 50, 100, 200]
    for max_processes in maxProcessesList:
        print("-------------------------------------------------------------------")
        print("Max_Processes:", max_processes)
        processesInfo = {}
        timeInfo = {}
        processesInfo["number"] = max_processes
        processList.append(processesInfo)
        loopLists = []
        
        for maxIter in loops:
            print("Loop", maxIter)
            loopInfo = {}
            loopInfo["value"] = maxIter
            results_async = []
            startTime = time.time()
            with Pool(processes=max_processes) as pool:
                for lamda in np.linspace(0, 1, numberScales + 1):
                    vnsAlgo = VNS(maxIter=maxIter, poolLocalSearchLevel=3,poolShakingLevel=3)
                    results_async.append(pool.apply_async(vnsAlgo.solve, args=(assetInChoosen, lamda, expectedVector, covMatrix, corrMatrix)))
                results = [result.get() for result in results_async]
                
            timeParallel =  time.time()- startTime               
            print("Parallel time:", timeParallel)   
            
            startTime = time.time()
            for lamda in np.linspace(0, 1, numberScales + 1):
                vnsAlgo = VNS(maxIter=maxIter, poolLocalSearchLevel=3,poolShakingLevel=3)
                p = vnsAlgo.solve(assetInChoosen, lamda, expectedVector, covMatrix, corrMatrix)

            timeSequence = time.time()- startTime
            print("Sequence time:", timeSequence)
            print("Done")
            loopInfo["time"] = {"parallel": timeParallel,"sequence": timeSequence}
            loopLists.append(loopInfo)
        processesInfo["loop"] = loopLists    
         
    print(timeComparing)
    with open('result.json', 'w') as fp:
        json.dump(timeComparing, fp)        
        
    subprocess.check_call('react-webpack\\npm start', shell=True)        

