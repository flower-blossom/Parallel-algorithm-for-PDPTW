from solve import *
from IO import *

dataName = "data//test_data.txt"
with open(dataName) as f_obj:
    data = [line.strip("\n") for line in f_obj.readlines()]

dataModel = readInputFile(data)
time1 = time.time()
sol = solver().solving(dataModel)
print("Time run", time.time()-time1)
print("costFuction:", sol.costFuction)

# run it if you want to looking output
# writeOutFile(sol, dataModel)
