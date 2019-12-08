import csv

import simulation as simulation
import sys
import pandas as pd
from igraph import *


# print(sys.argv[1])
# print(sys.argv[2])
# print(sys.argv[3])



# pp = float(sys.argv[1])
# size  = int(sys.argv[2])
# seeds = int(sys.argv[3])
pp = 0.1
seeds = 2


# pobieram graf
graphDataFrame = pd.read_csv('networks/2.txt', sep=" ", usecols=[0, 1], header=None)
tuples = [tuple(x1) for x1 in graphDataFrame.values]
graph = Graph.TupleList(tuples, directed=False)



# pobieram coordinated execution
edgesWieghtDataFrame = pd.read_csv('networks/2.txt', sep=" ", usecols=[0, 1, 2, 3], header=None,
                                   names=['source', 'target', 'w1', 'w2'])

print('1', edgesWieghtDataFrame.size)

df2 = pd.DataFrame({'source':edgesWieghtDataFrame['target'],
                    'target':edgesWieghtDataFrame['source'],
                    'w1':edgesWieghtDataFrame['w2']})



concatedEdgesWiegh = pd.concat([edgesWieghtDataFrame, df2], join='inner', ignore_index=True)

# concatedEdgesWiegh[]

concatedEdgesWiegh = concatedEdgesWiegh.rename(columns={'w1': 'weight'})

print('concatedEdgesWiegh', concatedEdgesWiegh)

simulation.simulation(pp = pp, seeds = seeds, graph = graph, coordinatedExecution = concatedEdgesWiegh)


# for i in graph.vs:
#
#     print(i)