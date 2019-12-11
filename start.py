import csv

import simulation_with_calculate as simulation_with_calculate
import simulation_without_calculate as simulation_without_calculate
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

network = 1

myFields = ['nr', 'nazwa', 'pp', 'numberOfSeeds', 'seeds', 'numberOfNodes', 'step', 'infectedPerStep', 'infectedTotal', 'infectedTotalPercentage']
myFile = open('results_calc_1_step.csv', 'w')

# myFile = open('results_calc_every_step.csv', 'w')
with myFile:
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader()



for file in os.listdir('networks/'):
    # print()
    # print(file.split('_')[1][0])
    name = file.split('_')[0]
    numberOfCoordinatedExecution = file.split('_')[1][0]

    # pobieram graf
    graphDataFrame = pd.read_csv('networks/' + name + '_' + numberOfCoordinatedExecution + '.txt', sep=" ", usecols=[0, 1], header=None)
    tuples = [tuple(x1) for x1 in graphDataFrame.values]
    graph = Graph.TupleList(tuples, directed=False)



    # pobieram coordinated execution
    edgesWieghtDataFrame = pd.read_csv('networks/' + name + '_' + numberOfCoordinatedExecution + '.txt', sep=" ", usecols=[0, 1, 2, 3], header=None,
                                       names=['source', 'target', 'w1', 'w2'])

    df2 = pd.DataFrame({'source':edgesWieghtDataFrame['target'],
                        'target':edgesWieghtDataFrame['source'],
                        'w1':edgesWieghtDataFrame['w2']})



    concatedEdgesWiegh = pd.concat([edgesWieghtDataFrame, df2], join='inner', ignore_index=True)

    # concatedEdgesWiegh[]

    concatedEdgesWiegh = concatedEdgesWiegh.rename(columns={'w1': 'weight'})

    # print('concatedEdgesWiegh', concatedEdgesWiegh)

    simulation_with_calculate.simulation(pp = pp, seeds = seeds, graph = graph, coordinatedExecution = concatedEdgesWiegh, numberOfCoordinatedExecution=numberOfCoordinatedExecution, name=name)


# for i in graph.vs:
#
#     print(i)