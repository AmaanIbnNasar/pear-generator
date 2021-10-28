"""
File filled with helper functions to work out why the network is making the decisions it is.
"""
import networkx as nx


def plotGraph(graph):
    import matplotlib.pyplot as plt
    pos = nx.drawing.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(
        graph, pos, width=[edge[2]/100 for edge in graph.edges.data("weight")])
    nx.draw_networkx_labels(graph, pos)
    plt.show()


def getNeighborWeightsOfPerson(person, peopleGraph):
    for neigh in peopleGraph.neighbors(person):
        print(neigh, peopleGraph.edges[person, neigh]['weight'])
