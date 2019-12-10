import sequential
import pandas as pd
import networkx as nx
import copy
import csv

def selectSeeds(graph, forSingleStage):

    # print('voteRank', nx.voterank(createNxGraph(graph), forSingleStage))

    return nx.voterank(createNxGraph(graph), forSingleStage)


def mapEdgeList(graph, edgeList):
    mapped = []

    for edge in edgeList:
        mapped.append([graph.vs.select(edge[0])[0]['name'], graph.vs.select(edge[1])[0]['name']])

    return mapped

def createNxGraph(graph):
    A = mapEdgeList(graph, graph.get_edgelist())
    return nx.Graph(A)

def simulation(pp, seeds, graph, coordinatedExecution, numberOfCoordinatedExecution, name):


    seedsForSequnetial = selectSeeds(graph, 1)

    step = 1;

    infectedNodesBySequential = []

    infectedNodesBySequential = sequential.sequential(nr = numberOfCoordinatedExecution, name = name, pp = pp, step = step, graph = graph, infectedNodes = infectedNodesBySequential, coordinatedExecution = coordinatedExecution,                                                                            seeds = seedsForSequnetial)


