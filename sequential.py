from igraph import *
import random

def sequential(pp, step, graph, infectedNodes, coordinatedExecution, seeds):

    nodes = Graph.vcount(graph)

    # for v in graph.vs:
    #     print(v)

    # print('number of nodes => ', nodes)
    # print('pp => ', pp)

    for i in range(0, nodes):
        graph.vs[i]["infected"] = 0
        graph.vs[i]["used"] = 0
        graph.vs[i]["stepinfected"] = 0

    infections = 0
    isInfecting = True

    # for index, node in seeds.iterrows():
    for name in seeds:

        node = graph.vs.select(name=name)[0]
        # print(node, graph.neighbors(name, mode="out"))

        node["infected"] = 1
        node["stepinfected"] = 0
        node["used"] = 0
        node["color"] = "green"
    infections = 0;

    while(isInfecting):

        infecting = infections

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

                                # tru = ((coordinatedExecution['A'] == j) & (coordinatedExecution['B'] == k)).any()

                                # print(j, k)
                                # print('neighborstab', neighborstab)
                                # print('graph.vs[j]', graph.vs[j]['name'], graph.vs[[k]]['name'])
                                x = coordinatedExecution.loc[((coordinatedExecution['source'] == graph.vs[j]['name']) & (
                                        coordinatedExecution['target'] == graph.vs[[k]]['name'])), 'weight'].iloc[0]

                                if x <= pp:
                                    # print('zarażony')

                                    graph.vs[k]["infected"] = 1
                                    graph.vs[k]["stepinfected"] = step
                                    graph.vs[k]["used"] = 0
                                    graph.vs[k]["color"] = "blue"

                                    infections = infections + 1

                                    infectedNodes.append(graph.vs[k]['name'])

            # TODO: TO DO WYNIESIENIA

        if (infecting == infections):
            isInfecting = False
        else:
            step = step + 1

    # plot(graph)
    print('step', step)
    print('infections', infections + len(seeds))
    print('infections', (infections + len(seeds)) / nodes * 100)
    print('infectedNodes', infectedNodes)

    return infectedNodes
