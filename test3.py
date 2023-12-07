# import numpy as np
# from numba import config, cuda, njit
# from time import perf_counter
# import sys
from util import calculate_sortino_ratio
import numpy as np
matrix = np.loadtxt('data\\realworld dataset\\Solutions\\DowJones\\OptPortfolios_CZeSD_DowJones.txt')
# print(len(matrix.T[0]))
returnVector = np.loadtxt("data\\realworld dataset\\Solutions\\FTSE100\\OutofSamplePortReturns_L_SSD_FTSE100_List.txt")
print(f"sortinoRatio: {calculate_sortino_ratio(returnVector, 0)}")
print(f"sharpe ratio: {np.mean(returnVector)/np.std(returnVector)}")
print(f"mean: {np.mean(returnVector)}")

    
    
        
        
        