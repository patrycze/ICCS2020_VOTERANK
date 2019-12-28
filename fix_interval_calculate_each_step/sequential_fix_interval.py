from __future__ import division
from igraph import *
import random
import csv
import copy
import datetime
import networkx as nx

# metoda a właściwie marshaller do reprezentacji nie przez indexy a przez nazwy, (ciągle kierujemy się nazwami a nie idkami!!!)
def mapEdgeList(graph, edgeList):
    mapped = []

    for edge in edgeList:
        mapped.append([graph.vs.select(edge[0])[0]['name'], graph.vs.select(edge[1])[0]['name']])

    return mapped

# metoda do utowrzenia grafu zrozumiałego przez networkx w celu obliczenia voteranka
def createNxGraph(graph):
    A = mapEdgeList(graph, graph.get_edgelist())
    return nx.Graph(A)



# metoda oblicza voteRank
def selectSeeds(graph, forSequential):
    start = datetime.datetime.now()
    voteRank = nx.voterank(createNxGraph(graph), forSequential)
    end = datetime.datetime.now()

    if (len(voteRank) < forSequential):
        voteRank = copy.copy(selectSeedsRandomly(graph, forSequential))

    return voteRank, (end - start)

def selectSeedsRandomly(graph, forSequential):
    ids = [v['name'] for v in graph.vs]

    print('ids =>', ids)

    if(len(ids) >= forSequential):
        return random.choices(ids, k=forSequential)
    else:
        return ids



# metoda do wycięcia grafu jedynie z niezainfekowanymi węzłami
def selectSeedsUninfected(graph, forSequential):

    # wyrzucam tutaj z sieci zainfekowane węzły
    try:
        to_delete_ids = [v.index for v in graph.vs if 1 is v['infected']]
    except:
        to_delete_ids = []

    uninfectedGraph = copy.copy(graph)

    # usunięcie po idkach ale pamiętać że ciągle kierujemy się attr NAME!!!!
    uninfectedGraph.delete_vertices(to_delete_ids)

    return selectSeeds(graph = uninfectedGraph, forSequential = forSequential)


def markAsSeeds(seeds, graph, step):
    for name in seeds:

        node = graph.vs.select(name=name)[0]
        # print(node, graph.neighbors(name, mode="out"))

        node["infected"] = 1

        if(step > 1):
            node["stepinfected"] = step
        else:
            node["stepinfected"] = 0

        node["used"] = 0
        node["color"] = "green"
        node["isSeed"] = 1



def calculateNumberOfSeeds(graph):
    seeds = [v.index for v in graph.vs if 1 is v['isSeed']]
    return len(seeds)

def sequential(nr, network, pp, step, graph, infectedNodes, coordinatedExecution, seeds, time, interval, limit, limitPercentage, timeArray):


    myFields = ['nr', 'nazwa', 'pp', 'numberOfSeeds', 'seeds', 'totalNumberOfSeeds', 'numberOfNodes', 'step', 'infectedPerStep', 'infectedTotal', 'infectedTotalPercentage', 'computionalTime', 'interval', 'limitPercentage']

    nodes = Graph.vcount(graph)

    limit = int(limit)
    # selectedSeeds = copy.copy(seeds)

    # print('number of nodes => ', nodes)
    # print('pp => ', pp)

    if(step == 0):
        for i in range(0, nodes):
            graph.vs[i]["infected"] = 0
            graph.vs[i]["used"] = 0
            graph.vs[i]["stepinfected"] = 0
            graph.vs[i]["isSeed"] = 0

    infections = 0
    isInfecting = True

    numberOfSeeds = seeds

    print(numberOfSeeds)

    # for index, node in seeds.iterrows():
    # for name in seeds[0:numberOfSeeds]:
    #
    #     node = graph.vs.select(name=name)[0]
    #     # print(node, graph.neighbors(name, mode="out"))
    #
    #     node["infected"] = 1
    #
    #     if (step > 1):
    #         node["stepinfected"] = step
    #     else:
    #         node["stepinfected"] = 0
    #
    #     node["used"] = 0
    #     node["color"] = "green"
    #     node["isSeed"] = 1


    infections = 0;

    # usuwamy z tablicy wykorzystane seedy
    # del seeds[0:numberOfSeeds]

    while(isInfecting):

        print('step', step)
        # limit poniewaz liczymy tylko z 1 2 3 4 5% z calej sieci
        if(calculateNumberOfSeeds(graph) < limit):
            if(calculateNumberOfSeeds(graph) + numberOfSeeds > limit):
                print('(limit - calculateNumberOfSeeds(graph))', limit,  calculateNumberOfSeeds(graph), (limit - calculateNumberOfSeeds(graph)))
                if (step % interval == 0):
                    seeds, time = selectSeedsUninfected(graph, numberOfSeeds * interval)
                    selectedSeeds = copy.copy(seeds[0:(limit - calculateNumberOfSeeds(graph))])

                    print('przeliczam in step ==>', step, 'we selected =>', seeds[0:numberOfSeeds], 'in time =>', time,
                          'but whole ranking =>', seeds)
                    markAsSeeds(seeds[0:numberOfSeeds], graph, step)

                    # usuwamy z tablicy wykorzystane seedy
                    del seeds[0:numberOfSeeds]
                if (step % interval != 0):
                    markAsSeeds(seeds[0:(limit - calculateNumberOfSeeds(graph))], graph, step)
                    print('we selected =>', seeds[0:(limit - calculateNumberOfSeeds(graph))], 'in time =>', time)
                    selectedSeeds = copy.copy(seeds[0:(limit - calculateNumberOfSeeds(graph))])

                    # usuwamy z tablicy wykorzystane seedy
                    del seeds[0:numberOfSeeds]

                    print('whole ranking =>', seeds)

            else:
                # sprawdzamy czy przeliczac ranking
                if(step % interval == 0):
                    seeds, time = selectSeedsUninfected(graph, numberOfSeeds * interval)
                    selectedSeeds = copy.copy(seeds[0:numberOfSeeds])

                    print('przeliczam in step ==>', step, 'we selected =>', seeds[0:numberOfSeeds], 'in time =>', time, 'but whole ranking =>', seeds)
                    markAsSeeds(seeds[0:numberOfSeeds], graph, step)

                    #usuwamy z tablicy wykorzystane seedy
                    del seeds[0:numberOfSeeds]

                if(step % interval != 0):
                    markAsSeeds(seeds[0:numberOfSeeds], graph, step)
                    print('we selected =>', seeds[0:numberOfSeeds], 'in time =>', time)
                    selectedSeeds = copy.copy(seeds[0:numberOfSeeds])

                    #usuwamy z tablicy wykorzystane seedy
                    del seeds[0:numberOfSeeds]

                    print('whole ranking =>', seeds)

            # print('Moje seedy', seeds, step % interval == 0)
        infecting = infections


        infectionsPerStep = 0

        for j in range(0, nodes):

            if (graph.vs[j]["infected"] == 1 and graph.vs[j]["used"] == 0 and graph.vs[j]["stepinfected"] != step):

                graph.vs[j]["used"] = 1
                neighborstab = graph.neighbors(j, mode="out")

                if (len(neighborstab) > 0):

                    n = 0
                    notinfected = []
                    for i in range(0, len(neighborstab)):
                        if (graph.vs[neighborstab[i]]["infected"] == 0):
                            notinfected.append(neighborstab[i])

                    numberofneighbors = len(notinfected)

                    if notinfected:
                        for k in notinfected:

                            if (numberofneighbors >= 1):

                                x = coordinatedExecution.loc[((coordinatedExecution['source'] == graph.vs[j]['name']) & (
                                        coordinatedExecution['target'] == graph.vs[[k]]['name'][0])), 'weight'].iloc[0]

                                if x <= pp:
                                    # print('zarażony')

                                    graph.vs[k]["infected"] = 1
                                    graph.vs[k]["stepinfected"] = step
                                    graph.vs[k]["used"] = 0
                                    graph.vs[k]["color"] = "blue"

                                    infections = infections + 1
                                    infectionsPerStep = infectionsPerStep + 1

                                    infectedNodes.append(graph.vs[k]['name'])

            # TODO: TO DO WYNIESIENIA

        totalInfected = [v.index for v in graph.vs if 1 is v['infected']]

        myFile = open(str(pp) + '_results_fix_interval.csv', 'a')
        with myFile:
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writerow({'nr': nr, 'nazwa': network, 'pp': pp, 'numberOfSeeds': len(selectedSeeds), 'seeds': selectedSeeds, 'totalNumberOfSeeds': calculateNumberOfSeeds(graph), 'numberOfNodes': nodes, 'step': step,
                             'infectedPerStep': infectionsPerStep, 'infectedTotal': len(totalInfected),  'infectedTotalPercentage': len(totalInfected) / nodes * 100, 'computionalTime': time, 'interval': interval,
                             'limitPercentage': limitPercentage})

            timeArray.append(time)

        step = step + 1

        # print(infecting, infections)
        # print(infecting == infections)
        # print(isInfecting)

        if (infecting == infections):
            # seeds, time = selectSeedsUninfected(graph, 2)
            if(len(selectedSeeds) == 0 or calculateNumberOfSeeds(graph) >= limit):
                isInfecting = False

    #plot(graph)
    return graph, step, totalInfected, timeArray
