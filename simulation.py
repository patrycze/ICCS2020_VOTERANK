import sequential
import pandas as pd
import networkx as nx
import copy
import csv

def selectSeeds(graph, forSequential):

    # print('voteRank', forSequential, nx.voterank(createNxGraph(graph), forSequential))
    # for v in graph.vs:
    #         print(v)

    return nx.voterank(createNxGraph(graph), forSequential)

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
    seedsForSequnetial = selectSeedsUninfected(graph = graph, forSequential = seeds)

    while(len(seedsForSequnetial) > 0):

        print('seedsForSequnetial', seedsForSequnetial)

        infectedNodesBySequential = []
        graph, step = sequential.sequential(nr = numberOfCoordinatedExecution, network = name, pp = pp, step = step, graph = graph, infectedNodes = infectedNodesBySequential, coordinatedExecution = coordinatedExecution, seeds = seedsForSequnetial)

        seedsForSequnetial = selectSeedsUninfected(graph=graph, forSequential=seeds)

