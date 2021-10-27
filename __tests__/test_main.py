import itertools
from unittest import TestCase

import networkx as nx

from main import convertPreviousPairsToGraphWeights


def setupGraph():
    graph = nx.Graph()
    graph.add_edges_from(itertools.combinations(range(1, 5), 2), weight=100)
    return graph


class Test(TestCase):
    def test_basic_graph_gets_converted(self):
        graph = setupGraph()
        convertPreviousPairsToGraphWeights(graph, [])
        self.assertEqual([(1, 2, 100), (1, 3, 100), (1, 4, 100), (2, 3, 100), (2, 4, 100), (3, 4, 100)],
                         list(graph.edges.data("weight")))

    def test_correctly_discounts_one_pair(self):
        graph = setupGraph()
        convertPreviousPairsToGraphWeights(graph, [{1:2}])
        self.assertEqual([(1, 2, 0), (1, 3, 100), (1, 4, 100), (2, 3, 100), (2, 4, 100), (3, 4, 100)],
                         list(graph.edges.data("weight")))

    def test_correctly_discounts_one_pair_over_multiple_weeks(self):
        graph = setupGraph()
        convertPreviousPairsToGraphWeights(graph, [{1:2},{2:3}])
        self.assertEqual([(1, 2, 0), (1, 3, 100), (1, 4, 100), (2, 3, 25), (2, 4, 100), (3, 4, 100)],
                         list(graph.edges.data("weight")))

    def test_correctly_adds_apple_bonus(self):
        graph = setupGraph()
        convertPreviousPairsToGraphWeights(graph, [{1:2},{2:0}])
        self.assertEqual([(1, 2, 15), (1, 3, 100), (1, 4, 100), (2, 3, 115), (2, 4, 115), (3, 4, 100)],
                         list(graph.edges.data("weight")))
