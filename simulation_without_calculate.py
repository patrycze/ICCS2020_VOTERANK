import sequential_without_calculate
import pandas as pd
import networkx as nx
import copy
import csv
from igraph import *

# metoda oblicza voteRank
def selectSeeds(graph, forSequential):
    return nx.voterank(createNxGraph(graph), forSequential)


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

def simulation(pp, seeds, graph, coordinatedExecution, numberOfCoordinatedExecution, name):

    step = 1;

    # robimy tylko 1 ranking na początku!! :)
    seedsForSequnetial = selectSeedsUninfected(graph = graph, forSequential = Graph.vcount(graph))

    while(len(seedsForSequnetial) > 0):

        if(len(seedsForSequnetial) > seeds):
            selectedSeeds = copy.copy(seedsForSequnetial[:seeds])
        else:
            selectedSeeds = copy.copy(seedsForSequnetial)

        infectedNodesBySequential = []
        graph, step = sequential_without_calculate.sequential(nr = numberOfCoordinatedExecution, network = name, pp = pp, step = step, graph = graph, infectedNodes = infectedNodesBySequential, coordinatedExecution = coordinatedExecution, seeds = selectedSeeds)


        # usuwam wykorzystane seedy z tablicy

        if (len(seedsForSequnetial) > seeds):
            del seedsForSequnetial[:seeds]
        else:
            seedsForSequnetial = []

