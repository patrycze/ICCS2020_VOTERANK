import sequential_without_calculate
import pandas as pd
import networkx as nx
import copy
import csv
from igraph import *
from timeit import default_timer as timer
from datetime import timedelta
import random

# metoda oblicza voteRank
def selectSeeds(graph, forSequential):
    start = timer()
    voteRank = nx.voterank(createNxGraph(graph), forSequential)
    end = timer()

    return voteRank, timedelta(seconds=end-start)


# metoda do wycięcia grafu jedynie z niezainfekowanymi węzłami
def selectSeedsUninfected(graph, forSequential):

    # wyrzucam tutaj z sieci zainfekowane węzły
    try:
        to_delete_ids = [v.index for v in graph.vs if 1 is v['infected']]
    except:
        to_delete_ids = []

    # print(to_delete_ids)

    uninfectedGraph = copy.copy(graph)

    # usunięcie po idkach ale pamiętać że ciągle kierujemy się attr NAME!!!!
    uninfectedGraph.delete_vertices(to_delete_ids)

    return selectSeeds(graph = uninfectedGraph, forSequential = forSequential)

def mapEdgeList(graph, edgeList):
    mapped = []

    for edge in edgeList:
        mapped.append([graph.vs.select(edge[0])[0]['name'], graph.vs.select(edge[1])[0]['name']])

    return mapped

def createNxGraph(graph):
    A = mapEdgeList(graph, graph.get_edgelist())
    return nx.Graph(A)


def selectSeedsRandomly(uninfectedNodes, forSequential):
    print('selectSeedsRandomly =>', uninfectedNodes)
    if(len(uninfectedNodes) >= forSequential):
        return random.choices(uninfectedNodes, k=forSequential)
    else:
        return uninfectedNodes

def calculateUninfected(graph):
    uninfected = [v['name'] for v in graph.vs if 0 is v['infected']]
    return uninfected


def calculateLimiForSeeding(graph, limit):
    return int(len(graph.vs) * limit)/100

def calculateNumberOfSeeds(graph):
    seeds = [v.index for v in graph.vs if 1 is v['isSeed']]
    return len(seeds)

def simulation(pp, seeds, graph, coordinatedExecution, numberOfCoordinatedExecution, name, limit):

    step = 1;

    copyGraph = copy.copy(graph)

    timeArray = []
    seedsArray = []

    limitForSeeding = calculateLimiForSeeding(graph, limit)

    # robimy tylko 1 ranking na początku!! :)
    seedsForSequnetial, time = selectSeedsUninfected(graph = copyGraph, forSequential = limitForSeeding)

    seedsArray.append(seedsForSequnetial)

    timeArray.append(time)

    uninfected = [0, 0]

    while(len(uninfected) > 0 and len(seedsArray) < limitForSeeding):

        if(len(seedsForSequnetial) > seeds):
            selectedSeeds = copy.copy(seedsForSequnetial[:seeds])
            seedsArray.append(selectedSeeds)

        else:
            selectedSeeds = selectSeedsRandomly(uninfected, forSequential=seeds)
            seedsArray.append(selectedSeeds)

        #     selectedSeeds = copy.copy(seedsForSequnetial)

        infectedNodesBySequential = []
        copyGraph, step, totalInfected, timeArray = sequential_without_calculate.sequential(nr = numberOfCoordinatedExecution, network = name, pp = pp, step = step, graph = copyGraph, infectedNodes = infectedNodesBySequential, coordinatedExecution = coordinatedExecution, seeds = selectedSeeds, time = time, limit = limit, timeArray = timeArray)

        #zlicz niezainfekowanych
        uninfected = copy.copy(calculateUninfected(copyGraph))

        # usuwam wykorzystane seedy z tablicy
        if (len(seedsForSequnetial) > seeds):
            del seedsForSequnetial[:seeds]
        else:
            seedsForSequnetial = []


    myFields = ['nr', 'nazwa', 'pp', 'numberOfSeeds', 'seeds', 'totalNumberOfSeeds', 'numberOfNodes', 'steps', 'infectedTotal', 'infectedTotalPercentage', 'computionalTime', 'limitPercentage']

    myFile = open(str(pp) + '_results_without_calculate_last.csv', 'a')
    with myFile:
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writerow({'nr': numberOfCoordinatedExecution, 'nazwa': name, 'pp': pp, 'numberOfSeeds': seeds, 'seeds': seeds,
                         'totalNumberOfSeeds': calculateNumberOfSeeds(copyGraph), 'numberOfNodes': len(copyGraph.vs), 'steps': step, 'infectedTotal': len(totalInfected),
                         'infectedTotalPercentage': len(totalInfected) / len(copyGraph.vs) * 100, 'computionalTime': timeArray, 'limitPercentage': limit})