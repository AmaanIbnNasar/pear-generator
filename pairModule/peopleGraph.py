import networkx as nx
import itertools


def doFullPairing(people, previousPairSets, peopleLocation):
    peopleGraph = convertPeopleToGraph(people)
    convertPreviousPairsToGraphWeights(peopleGraph, previousPairSets)
    weightHomeWorkers(peopleGraph, people, peopleLocation)
    return nx.max_weight_matching(peopleGraph, maxcardinality=True)


def convertPeopleToGraph(people):
    peopleGraph = nx.Graph()
    peopleEdges = itertools.combinations(people, 2)
    peopleGraph.add_edges_from(peopleEdges, weight=100)
    return peopleGraph


def convertPreviousPairsToGraphWeights(peopleGraph, previousPairSets):
    unmatchedPeople = []  # can include repeats
    # First apply the penalties for being matched previously
    for i, previousPairSet in enumerate(previousPairSets):
        for p1, p2 in previousPairSet.items():
            if p1 in peopleGraph.nodes and p2 == 0:
                unmatchedPeople.append(p1)
                continue
            if p1 not in peopleGraph.nodes or p2 not in peopleGraph.nodes:
                continue
            peopleGraph.edges[p1, p2]["weight"] *= 0.5 - 0.5**(i+1)

    # Then add the boost for being unpaired
    for unmatchedPerson in unmatchedPeople:
        for neighbor in peopleGraph.neighbors(unmatchedPerson):
            peopleGraph.edges[unmatchedPerson, neighbor]["weight"] += 15


def weightHomeWorkers(peopleGraph, people, peopleLocation):
    for p1, p2 in itertools.combinations(people, 2):
        if peopleLocation[p1] == peopleLocation[p2]:
            peopleGraph.edges[p1, p2]["weight"] += 150

def printPairings(pairings, apples):
    for (p1, p2) in pairings:
        print(f":pear: {p1} :pear: {p2} :pear:")
    for person in apples:
        print(f":apple: {person} :apple:")

    print()
