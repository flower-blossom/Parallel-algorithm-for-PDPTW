from vns import VNS
import pandas
import numpy as np
from random import seed
seed(2)


path = r'data\realworld dataset\\Datasets\\DowJones\\DowJones.xlsx'
# path = r'data\API binance\percentReturnsWeekData.xlsx'
# Read TestData
# my_data = pandas.read_excel(path, header=None)

# Read API Data
my_data = pandas.read_excel(path, index_col=0, header=0)

percentInOut = 0.2
data_in  = my_data.iloc[:round(percentInOut*my_data.shape[0]), :]
data_out = my_data.iloc[round(percentInOut*my_data.shape[0]):, :]
covMatrix = data_in.cov().to_numpy()
corrMatrix = data_in.corr().to_numpy()

expectedVector = np.mean(data_in.to_numpy(), axis=0)

covMatrixOut = data_out.cov().to_numpy()
corrMatrixOut = data_out.corr().to_numpy()
expectedVectorOut = np.mean(data_out.to_numpy(), axis=0)

for i in range(10):
    sol = VNS(maxIter=100, lamda=i/10, poolLocalSearchLevel=5,poolShakingLevel=5).solve(10, expectedVector, covMatrix, corrMatrix)
    print(sol.objectiveFunction)
    # print(sol.chosenAssetsList)
    # print(sol.proportionOfAssetsList)