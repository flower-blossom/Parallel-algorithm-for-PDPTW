from solve import *
from IO import *

with open("data//50h_100v_1000r.txt") as f_obj:
    data = [line.strip("\n") for line in f_obj.readlines()]

dataModel = readInputFile(data)
time1 = time.time()
sol = solver().solving(dataModel)
print("Time run", time.time()-time1)
print("costFuction:", sol.costFuction)
dataModel = readInputFile(data)
# writeOutFile(sol, dataModel)
