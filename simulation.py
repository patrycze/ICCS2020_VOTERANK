import sequential
import pandas as pd
import networkx as nx

# def selectSeeds(graph, forSingleStage):
#
#     seedsForSingleStage = []
#     seedsForSequnetial = []
#
#     # TODO: Robimy dataFrame z rankingiem węzłów np po degree i z niego losujemy przynależność dla procesów
#     ranking = pd.DataFrame(columns=['nodes', 'degree'])
#
#     for v in graph.vs:
#         ranking = ranking.append({'nodes': v, 'degree': graph.degree(v)}, ignore_index=True).sort_values('degree',
#                                                                                                      ascending=False)
#
#     ranking.index = pd.RangeIndex(len(ranking.index))
#
#     narrowedRanking = ranking.iloc[0 : forSingleStage + forSequential]
#
#     # losuje dla seedsForSingleStage wezły z puli najlepszych
#     seedsForSingleStage = narrowedRanking.sample(forSingleStage)
#
#     # wycinam z puli najlepsze węzły
#     narrowedRanking = narrowedRanking.drop(seedsForSingleStage.index)
#
#     # przekazuje to co zostało dla seedsForSequnetial
#     seedsForSequnetial = narrowedRanking
#
#     return seedsForSingleStage, seedsForSequnetial

def selectSeeds(graph, forSingleStage):

    print('voteRank', nx.voterank(createNxGraph(graph), 2))

    return nx.voterank(createNxGraph(graph), 2)


def mapEdgeList(graph, edgeList):
    mapped = []

    for edge in edgeList:
        mapped.append([graph.vs.select(edge[0])[0]['name'], graph.vs.select(edge[1])[0]['name']])

    return mapped

def createNxGraph(graph):
    A = mapEdgeList(graph, graph.get_edgelist())
    return nx.Graph(A)

def simulation(pp, seeds, graph, coordinatedExecution):


    seedsForSequnetial = selectSeeds(graph, 2)

    # TODO napisać jakiś fajny warunek stopu np kiedy już infectedNodes jednego i drugiego procesu nie zwiększają się od kilkunastu kroków
    # seedsForSingleStage, seedsForSequnetial = selectSeedsForBeginProceses(graph = graph, forSingleStage = 3, forSequential = 3)

    # while True:

    infectedNodesBySequential = []

    infectedNodesBySequential = sequential.sequential(pp = pp, step = 1, graph = graph, infectedNodes = infectedNodesBySequential, coordinatedExecution = coordinatedExecution,                                                                            seeds = seedsForSequnetial)