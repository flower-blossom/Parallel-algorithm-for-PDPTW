import numpy as np
from pandas import read_excel
from util import calculate_sortino_ratio, calculate_sharpe_ratio
import numpy as np

chooseLamda = ["0.0", "0.6", "1.0"]

listDataset = ["DowJones", "NASDAQ100",  "FTSE100", "FF49Industries"]
for fileNameDataset in listDataset:
    print("------------------------------------")
    print(fileNameDataset)
    pathData = 'data\\realworld dataset\\Datasets\\'
    pathSol  = 'output\\Realworld-dataset'
    data = read_excel(f"{pathData}{fileNameDataset}\\{fileNameDataset}.xlsx", header=0)
    
    startWindow = 51
    timeRebalance = 12
    for lamda in chooseLamda:
        sol = np.loadtxt(f'{pathSol}\\{fileNameDataset}\\OptPortfolios_VNS_{lamda}_{fileNameDataset}.txt')
        sol = sol.T
        count = 0
        returnsVector = []
        for windowTime in range(0, len(data), timeRebalance):
            solWeel = sol[count]
            count += 1
            # print(startWindow + windowTime + timeRebalance)
            data_out = data.iloc[startWindow + windowTime: startWindow + windowTime+ timeRebalance, :].to_numpy()
            for week in data_out:
                returns = sum([solWeel[i]*week[i]  for i in range(len(week))])
                returnsVector.append(returns)
                # print(len(week))
            if startWindow + windowTime+ timeRebalance >= len(data):
                break
        # print(len(returnsVector))
        print(f"Lamda: {lamda}")
        print(f"Sharpe ratio: {calculate_sharpe_ratio(returnsVector)}")
        print(f"Average return: {np.mean(returnsVector)}")
        
        
