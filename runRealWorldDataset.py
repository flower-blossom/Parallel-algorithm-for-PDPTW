import numpy as np
from pandas import read_excel
from util import runRealworldDataset, getListSolution
from multiprocessing import Pool


# Experiments file to run real world dataset
if __name__ == '__main__': 
    # Read the data from the text
    listDataset = ["DowJones", "NASDAQ100",  "FTSE100", "FF49Industries"]
    path = 'data\\realworld dataset\\Datasets\\'
    
    for fileNameDataset in listDataset:
        data = read_excel(f"{path}{fileNameDataset}\\{fileNameDataset}.xlsx", header=0)
        print(fileNameDataset)
        startWindow = 52
        timeRebalance = 12
        max_processes = 5
        for lamda in np.linspace(0, 1, 10):
            results_async = []
            solutionsList = []
            
            with Pool(processes=max_processes) as pool:
                for windowTime in range(0, len(data), timeRebalance):
                    print(startWindow + windowTime+ timeRebalance)
                    data_in  = data.iloc[:startWindow +  windowTime, :]
                    data_out = data.iloc[startWindow + windowTime: startWindow + windowTime+ timeRebalance, :]
                    
                    results_async.append(pool.apply_async(runRealworldDataset, args=(data_in, lamda)))
                    if startWindow + windowTime+ timeRebalance >= len(data):
                        break
                results = [result.get() for result in results_async]
                solutionsList = [getListSolution(sol, data_in.shape[1]) for sol in results]
                matrixSolution = np.array(solutionsList).T
                np.savetxt(f'Output\\Realworld-dataset\\{fileNameDataset}\\OptPortfolios_VNS_{round(lamda, 1)}_{fileNameDataset}.txt', matrixSolution, fmt='%.4f')


