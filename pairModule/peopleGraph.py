import networkx as nx
import itertools


def doFullPairing(people, previousPairObjs, peopleLocation):
    peopleGraph = convertPeopleToGraph(people)
    applyPreviousPairWeightDiscount(peopleGraph, previousPairObjs)
    applyUnpairedWeightBoost(peopleGraph, previousPairObjs)
    applySameLocationBoost(peopleGraph, people, peopleLocation)
    pairingsAsSet = nx.max_weight_matching(peopleGraph, maxcardinality=True)
    pairings = convertPairingSetToDict(pairingsAsSet)
    unpaired = calculateUnpaired(people, pairings)
    return pairings, unpaired


def convertPeopleToGraph(people):
    peopleGraph = nx.Graph()
    peopleEdges = itertools.combinations(people, 2)
    peopleGraph.add_edges_from(peopleEdges, weight=100)
    return peopleGraph


def applyPreviousPairWeightDiscount(peopleGraph, previousPairObjs):
    for i, previousPairObj in enumerate(previousPairObjs):
        for p1, p2 in previousPairObj["pairings"].items():
            if p1 not in peopleGraph.nodes or p2 not in peopleGraph.nodes:
                continue
            peopleGraph.edges[p1, p2]["weight"] *= 0.5 - 0.5**(i+1)


def applyUnpairedWeightBoost(peopleGraph, previousPairObjs):
    for previousPairObj in previousPairObjs:
        for unpairedPerson in previousPairObj["unpaired"]:
            for neighbor in peopleGraph.neighbors(unpairedPerson):
                peopleGraph.edges[unpairedPerson, neighbor]["weight"] += 15


def applySameLocationBoost(peopleGraph, people, peopleLocation):
    for p1, p2 in itertools.combinations(people, 2):
        if peopleLocation[p1] == peopleLocation[p2]:
            peopleGraph.edges[p1, p2]["weight"] += 150


def convertPairingSetToDict(pairingsAsSet):
    return {
        p1: p2
        for p1, p2 in pairingsAsSet
    }


def calculateUnpaired(people, pairings):
    unpaired = people.copy()
    for p1, p2 in pairings.items():
        unpaired.remove(p1)
        unpaired.remove(p2)
    return unpaired


def printPairings(pairings, apples):
    for p1, p2 in pairings.items():
        print(f":pear: {p1} :pear: {p2} :pear:")
    for person in apples:
        print(f":apple: {person} :apple:")

    print()
