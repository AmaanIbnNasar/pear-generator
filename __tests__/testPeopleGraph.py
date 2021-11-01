import itertools
from unittest import TestCase

import networkx as nx

from pairModule.peopleGraph import applyPreviousPairWeightDiscount


def setupGraph():
    graph = nx.Graph()
    graph.add_edges_from(itertools.combinations(range(1, 5), 2), weight=100)
    return graph


class Test(TestCase):
    def test_basic_graph_gets_converted(self):
        graph = setupGraph()
        applyPreviousPairWeightDiscount(graph, [])
        self.assertEqual([(1, 2, 100), (1, 3, 100), (1, 4, 100), (2, 3, 100), (2, 4, 100), (3, 4, 100)],
                         list(graph.edges.data("weight")))

    def test_correctly_discounts_one_pair(self):
        graph = setupGraph()
        applyPreviousPairWeightDiscount(graph, [{"pairings": {1: 2}}])
        self.assertEqual([(1, 2, 0), (1, 3, 100), (1, 4, 100), (2, 3, 100), (2, 4, 100), (3, 4, 100)],
                         list(graph.edges.data("weight")))

    def test_correctly_discounts_one_pair_over_multiple_sets(self):
        graph = setupGraph()
        applyPreviousPairWeightDiscount(
            graph, [{"pairings": {1: 2}}, {"pairings": {2: 3}}])
        self.assertEqual([(1, 2, 0), (1, 3, 100), (1, 4, 100), (2, 3, 25), (2, 4, 100), (3, 4, 100)],
                         list(graph.edges.data("weight")))
