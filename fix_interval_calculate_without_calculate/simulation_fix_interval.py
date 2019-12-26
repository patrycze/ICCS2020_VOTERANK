from __future__ import division

import sequential_fix_interval
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

    if (len(voteRank) < forSequential):
        voteRank = copy.copy(selectSeedsRandomly(graph, forSequential))

    return voteRank, timedelta(seconds=end - start)

def selectSeedsRandomly(graph, forSequential):
    ids = [v['name'] for v in graph.vs]

    # print('ids =>', ids)

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

def calculateLimiForSeeding(graph, limit):
    # print((len(graph.vs) * limit)/100)
    return int(len(graph.vs) * limit)/100

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

def calculateNumberOfSeeds(graph):
    seeds = [v.index for v in graph.vs if 1 is v['isSeed']]
    return len(seeds)


def calculateUninfected(graph):
    uninfected = [v['name'] for v in graph.vs if 0 is v['infected']]
    return uninfected


def simulation(pp, seeds, graph, coordinatedExecution, numberOfCoordinatedExecution, name, interval, limit):

    step = 1;

    graphCopy = copy.copy(graph)
    seedsArray = []
    timeArray = []


    limitForSeeding = calculateLimiForSeeding(graph, limit)

    # robimy tylko 1 ranking na początku!! :)
    seedsForSequnetial, time = selectSeedsUninfected(graph = graphCopy, forSequential = limitForSeeding)
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
        # print('numberOfSeeds', seeds, seedsForSequnetial)

        infectedNodesBySequential = []
        graphCopy, step, totalInfected, timeArray = sequential_fix_interval.sequential(nr = numberOfCoordinatedExecution, network = name, pp = pp, step = step, graph = graphCopy, infectedNodes = infectedNodesBySequential, coordinatedExecution = coordinatedExecution, seeds = seedsForSequnetial, time = time, interval = interval, limit = limitForSeeding, timeArray = timeArray)

        # zlicz niezainfekowanych
        uninfected = copy.copy(calculateUninfected(graphCopy))

        # usuwam wykorzystane seedy z tablicy
        if (len(seedsForSequnetial) > seeds):
            del seedsForSequnetial[:seeds]
        else:
            seedsForSequnetial = []


    myFields = ['nr', 'nazwa', 'pp', 'numberOfSeeds', 'seeds', 'totalNumberOfSeeds', 'numberOfNodes', 'steps',
                'infectedTotal', 'infectedTotalPercentage', 'computionalTime', 'limitPercentage']

    myFile = open(str(pp) + '_results_without_calculate_last.csv', 'a')
    with myFile:
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writerow(
            {'nr': numberOfCoordinatedExecution, 'nazwa': name, 'pp': pp, 'numberOfSeeds': seeds, 'seeds': seeds,
             'totalNumberOfSeeds': calculateNumberOfSeeds(graphCopy), 'numberOfNodes': len(graphCopy.vs), 'steps': step,
             'infectedTotal': len(totalInfected),
             'infectedTotalPercentage': len(totalInfected) / len(graphCopy.vs) * 100, 'computionalTime': timeArray,
             'limitPercentage': limit})