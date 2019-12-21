import sequential_with_calculate
import pandas as pd
import networkx as nx
import copy
import csv
from timeit import default_timer as timer
from datetime import timedelta
import random

# metoda oblicza voteRank
def selectSeeds(graph, forSequential):
    start = timer()
    voteRank = nx.voterank(createNxGraph(graph), forSequential)
    end = timer()

    if(len(voteRank) < forSequential):
        voteRank = copy.copy(selectSeedsRandomly(graph, forSequential))

    return voteRank, timedelta(seconds=end-start)

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

def calculateLimiForSeeding(graph, limit):
    return int(len(graph.vs) * limit)/100

def calculateNumberOfSeeds(graph):
    print(len(graph.vs))
    if(len(graph.vs) > 0):
        seeds = [v.index for v in graph.vs if 1 is v['isSeed']]
    else:
        seeds = []
    return len(seeds)

def simulation(pp, seeds, graph, coordinatedExecution, numberOfCoordinatedExecution, name, limit):

    copyGraph = copy.copy(graph)
    step = 1;
    seedsArray = []
    timeArray = []

    limitForSeeding = calculateLimiForSeeding(copyGraph, limit)

    seedsForSequnetial, time = selectSeedsUninfected(graph = copyGraph, forSequential = seeds)

    seedsArray.append(seedsForSequnetial)
    timeArray.append(time)

    while(len(seedsForSequnetial) > 0 and len(seedsArray) < limitForSeeding):

        infectedNodesBySequential = []
        copyGraph, step, totalInfected, timeArray = sequential_with_calculate.sequential(nr = numberOfCoordinatedExecution, network = name, pp = pp, step = step, graph = copyGraph, infectedNodes = infectedNodesBySequential, coordinatedExecution = coordinatedExecution, seeds = seedsForSequnetial, time = time, limit = limit, timeArray = timeArray)

        # przeliczam co krok ranking
        seedsForSequnetial, time = selectSeedsUninfected(graph = copyGraph, forSequential=seeds)
        seedsArray.append(seedsForSequnetial)
        timeArray.append(time)
        # print('seedsForSequnetial', seedsForSequnetial, time)

    myFields = ['nr', 'nazwa', 'pp', 'numberOfSeeds', 'seeds', 'totalNumberOfSeeds', 'numberOfNodes', 'steps',
                'infectedTotal', 'infectedTotalPercentage', 'computionalTime', 'limitPercentage']

    myFile = open(str(pp) + '_results_with_calculate_last.csv', 'a')
    with myFile:
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writerow(
            {'nr': numberOfCoordinatedExecution, 'nazwa': name, 'pp': pp, 'numberOfSeeds': seeds, 'seeds': seeds,
             'totalNumberOfSeeds': calculateNumberOfSeeds(copyGraph), 'numberOfNodes': len(copyGraph.vs), 'steps': step,
             'infectedTotal': len(totalInfected),
             'infectedTotalPercentage': len(totalInfected) / len(copyGraph.vs) * 100, 'computionalTime': timeArray,
             'limitPercentage': limit})