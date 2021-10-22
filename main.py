import networkx as nx, json, itertools, matplotlib.pyplot as plt

def getPeople():
    with open("./__pairfiles__/people.json") as f:
        people = json.load(f)
    return people["people"]

def getPreviousPairs():
    with open("./__pairfiles__/previous_pears.JSON") as f:
        previousPairWeeks = json.load(f)
    return previousPairWeeks

def convertPeopleToGraph(people):
    peopleGraph = nx.Graph()
    peopleEdges = itertools.combinations(people, 2)
    peopleGraph.add_edges_from(peopleEdges, weight=100)
    return peopleGraph

def convertPreviousPairsToGraphWeights(peopleGraph, previousPairWeeks):
    for i, previousPairWeek in enumerate(previousPairWeeks):
        for p1, p2 in previousPairWeek.items():
            if p1 in peopleGraph.nodes and p2 == 0:
                for p1Neigh in peopleGraph.neighbors(p1):
                    peopleGraph.edges[p1, p1Neigh]["weight"] += 5
                continue
            if p1 not in peopleGraph.nodes or p2 not in peopleGraph.nodes:
                # print("WARNING")
                continue
            peopleGraph.edges[p1, p2]["weight"] *= 0.5 - 0.5**(i+1)


def plotGraph(graph):
    pos = nx.drawing.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos, width=[edge[2]/100 for edge in graph.edges.data("weight")])
    nx.draw_networkx_labels(graph, pos)
    plt.show()

def main():
    people = getPeople()
    previousPairWeeks = getPreviousPairs()
    peopleGraph = convertPeopleToGraph(people)
    convertPreviousPairsToGraphWeights(peopleGraph, previousPairWeeks)
    plotGraph(peopleGraph)
    print(nx.max_weight_matching(peopleGraph))




if __name__=="__main__":
    main()