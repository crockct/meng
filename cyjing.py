import random
import networkx as nx
import io

# High transitions between networks (ASs) and intra network transitions
# Time in seconds, 10,000 ->2.7 hours
def highNetworkTransitionAndMobility(users = 1000, time = 10000):
    random.seed()
    transitions = []
    probTransitionPerSec = .01
    probNetworkTransitionPerSec = .005
    for i in range(users):
        userTrans = []
        for j in range(time):
            rand = random.random()
            if rand < probTransitionPerSec or rand < probNetworkTransitionPerSec:
                transition = [j,0]
                if rand < probNetworkTransitionPerSec:
                    transition = [j,1]
                userTrans.append(transition)
        transitions.append(userTrans) 
    return transitions


def createTrace(topologyFileName, clientList):
    graph = {}
    f = open(topologyFileName, 'r')
    for line in f:
        print line

    
    new_graph = nx.Graph()
    for source, targets in graph.iteritems():
        for inner_dict in targets:
            assert len(inner_dict) == 1
            new_graph.add_edge(int(source) - 1, int(inner_dict.keys()[0]) - 1,
                           weight=inner_dict.values()[0])
    adjacency_matrix = nx.adjacency_matrix(new_graph)

createTrace("topology.txt", [])
print highNetworkTransitionAndMobility(10, 100)
