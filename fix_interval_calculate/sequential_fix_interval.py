from igraph import *
import random
import csv
from fix_interval_calculate.simulation_fix_interval import selectSeedsUninfected



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

def sequential(nr, network, pp, step, graph, infectedNodes, coordinatedExecution, seeds, time, interval, limit):


    myFields = ['nr', 'nazwa', 'pp', 'numberOfSeeds', 'seeds', 'totalNumberOfSeeds', 'numberOfNodes', 'step', 'infectedPerStep', 'infectedTotal', 'infectedTotalPercentage', 'computionalTime', 'interval']

    nodes = Graph.vcount(graph)



    # print('number of nodes => ', nodes)
    # print('pp => ', pp)

    if(step == 1):
        for i in range(0, nodes):
            graph.vs[i]["infected"] = 0
            graph.vs[i]["used"] = 0
            graph.vs[i]["stepinfected"] = 0
            graph.vs[i]["isSeed"] = 0

    infections = 0
    isInfecting = True

    numberOfSeeds = len(seeds)
    # for index, node in seeds.iterrows():
    for name in seeds:

        node = graph.vs.select(name=name)[0]
        # print(node, graph.neighbors(name, mode="out"))

        node["infected"] = 1

        if (step > 1):
            node["stepinfected"] = step
        else:
            node["stepinfected"] = 0

        node["used"] = 0
        node["color"] = "green"
        node["isSeed"] = 1

    infections = 0;

    while(isInfecting):

        # print('step', step)
        # ponieważ fix_interval zakłada że dodajemy seedy w stale okreslonym czasie musimy tutaj sprawdzać w przypadku odstępu 2 kroków step mod 2 == 0
        if(step > 1 and step % interval == 0):

            # limit poniewaz liczymy tylko z 1 2 3 4 5% z calej sieci
            if(calculateNumberOfSeeds(graph) < limit):
                seeds, time = selectSeedsUninfected(graph, numberOfSeeds)
                # print('in step ==>', step, 'we selected =>', seeds, 'in time =>', time)
                markAsSeeds(seeds, graph, step)

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

        myFile = open('results_fix_interval.csv', 'a')
        with myFile:
            writer = csv.DictWriter(myFile, fieldnames=myFields)
            writer.writerow({'nr': nr, 'nazwa': network, 'pp': pp, 'numberOfSeeds': len(seeds), 'seeds': seeds, 'totalNumberOfSeeds': calculateNumberOfSeeds(graph), 'numberOfNodes': nodes, 'step': step,
                             'infectedPerStep': infectionsPerStep, 'infectedTotal': len(totalInfected),  'infectedTotalPercentage': len(totalInfected) / nodes * 100, 'computionalTime': time, 'interval': interval})


        step = step + 1

        # print(infecting, infections)
        # print(infecting == infections)
        # print(isInfecting)

        if (infecting == infections):
            # seeds, time = selectSeedsUninfected(graph, 2)
            if(len(seeds) == 0 or calculateNumberOfSeeds(graph) >= limit):
                isInfecting = False

    # plot(graph)
    return graph, step
