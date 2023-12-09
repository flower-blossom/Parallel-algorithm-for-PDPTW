import json
import plotly.express as px
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


# Opening JSON file
listScaleTime = [0 for _ in range(5)]
for idx in range(1 ,4):

    f = open(f'output\\analyst\\result{idx}.json')
    data = json.load(f)
    for i in data['Processes']:
        parallelTime = i["loop"][4]['time']['parallel']
        sequenceTime = i["loop"][4]['time']['sequence']
        listScaleTime[i["number"] - 1] += (sequenceTime/parallelTime)      
listScaleTime = [round(i/3, 2) for i in listScaleTime]  
          

ypoints = np.array([3, 8, 1, 10])
fig, ax = plt.subplots() 
ax.plot([1, 2, 3, 4, 5], listScaleTime, 'bo-')

# plt.plot([1, 2, 3, 4, 5], listScaleTime ,color = 'r')
for X, Y, Z in zip([1, 2, 3, 4, 5], listScaleTime, listScaleTime):
    # Annotate the points 5 _points_ above and to the left of the vertex
    ax.annotate('{}'.format(Z), xy=(X,Y), xytext=(-5, 5), ha='right',
                textcoords='offset points')
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.xlabel("Number of processors")
plt.ylabel("Speed up")
   
plt.grid()
plt.savefig('output\\analyst\\timeComparing.png')
plt.show()
