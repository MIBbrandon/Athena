import unittest
import networkx as nx
from critics.inputCritics import checkingG_swaps, checkingG_interactions, checkingSODDI, \
    CONST_gSwapsMustBeUndirectedMSG, CONST_nodesAreNotCorrectIntsMSG, CONST_gSwapsMustBeConnectedMSG, \
    CONST_tooFewNodesMSG, CONST_gInteractionsIsUndirectedMSG, CONST_gInteractionsLoopsMSG, \
    CONST_gInteractionsHasNoEdgeMSG, CONST_SODDIbadFormat, CONST_SODDINodesOutOfRange, \
    CONST_SODDIInvalidSelfInteractions


class TestGSwapInputCritic(unittest.TestCase):
    def test_G_swapsTooFewNodes(self):
        # Test that an exception is raised when the number of nodes in G_swaps is less than 2

        # We create a G_swaps with no nodes
        G_swaps = nx.Graph()
        with self.assertRaises(ValueError, msg=CONST_tooFewNodesMSG):
            checkingG_swaps(G_swaps)

        # We create a G_swaps with 1 node
        G_swaps.add_node(0)
        with self.assertRaises(ValueError, msg=CONST_tooFewNodesMSG):
            checkingG_swaps(G_swaps)

    def test_G_swapsDirected(self):
        # Test that an exception is raised when G_swaps is a directed graph

        # We create a directed G_swaps with at least 2 nodes
        G_swaps = nx.DiGraph()
        G_swaps.add_nodes_from([0, 1])
        with self.assertRaises(Exception, msg=CONST_gSwapsMustBeUndirectedMSG):
            checkingG_swaps(G_swaps)

    def test_G_swapsConnected(self):
        # Test that an exception is raised when G_swaps is a directed graph

        # We create an undirected G_swaps with at least 2 nodes, but not connected
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1])
        with self.assertRaises(Exception, msg=CONST_gSwapsMustBeConnectedMSG):
            checkingG_swaps(G_swaps)

    def test_G_swapsIncorrectNodeLabels(self):
        # Test that an exception is raised when the nodes of G_swaps are not from 0 to the number of nodes - 1

        # We create an undirected and connected G_swaps with at least 2 nodes, but the labels are not in range(nodes)
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 9, 5])
        G_swaps.add_edge(0, 9)
        G_swaps.add_edge(5, 9)
        with self.assertRaisesRegex(Exception, CONST_nodesAreNotCorrectIntsMSG + str(len(list(G_swaps.nodes)))):
            checkingG_swaps(G_swaps)


class TestGInteractionsInputCritic(unittest.TestCase):
    def test_G_interactionsDirected(self):
        # Test that an exception is thrown if G_interactions is not a DiGraph
        G_interactions = nx.Graph()
        with self.assertRaises(Exception, msg=CONST_gInteractionsIsUndirectedMSG):
            checkingG_interactions(G_interactions)

    def test_G_interactionsLoops(self):
        # Test that an exception is thrown if G_interactions has nodes with edges pointing towards themselves (loops)
        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1])
        G_interactions.add_edges_from([[0, 1], [0, 0]])
        with self.assertRaises(Exception, msg=CONST_gInteractionsLoopsMSG):
            checkingG_interactions(G_interactions)

    def test_G_interactionsIncorrectNodeLabels(self):
        # Test that an exception is thrown when the labels of nodes of G_interactions are not in range(nodes) in order
        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([1, 0])
        G_interactions.add_edge(0, 1)
        with self.assertRaisesRegex(Exception, CONST_nodesAreNotCorrectIntsMSG + str(len(list(G_interactions.nodes)))):
            checkingG_interactions(G_interactions)

    def test_G_interactionsHasNoEdge(self):
        # Test that an exception is thrown when G_interactions doesn't have any edges
        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])
        with self.assertRaises(Exception, msg=CONST_gInteractionsHasNoEdgeMSG):
            checkingG_interactions(G_interactions)

class TestSODDIInputCritic(unittest.TestCase):
    def test_SODDIInputType(self):
        # Test that an exception is thrown when SODDI is not a list of tuples of ints

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])

        # Checking for soddi not being a list
        soddi = "#"
        with self.assertRaises(Exception, msg=CONST_SODDIbadFormat):
            checkingSODDI(soddi, len(list(G_interactions.nodes)))

        # Checking for soddi not being a list of tuples
        soddi = [42]
        with self.assertRaises(Exception, msg=CONST_SODDIbadFormat):
            checkingSODDI(soddi, len(list(G_interactions.nodes)))

        # Checking for soddi not being a list of tuples of ints
        soddi = [("#", 2.5)]
        with self.assertRaises(Exception, msg=CONST_SODDIbadFormat):
            checkingSODDI(soddi, len(list(G_interactions.nodes)))

    def test_SODDIInvalidSelfInteractions(self):
        # Test that an exception is thrown when there is a desired interaction in SODDI of a node with itself
        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])

        # There is no node 4, since there are only 4 nodes going from 0 to 3
        soddi = [(1, 1)]
        with self.assertRaises(Exception, msg=CONST_SODDIInvalidSelfInteractions):
            checkingSODDI(soddi, len(list(G_interactions.nodes)))

    def test_SODDIIntegersWithinRange(self):
        # Test that an exception is thrown when the ints in SODDI are not within range

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])

        # There is no node 4, since there are only 4 nodes going from 0 to 3
        soddi = [(2, 4)]
        with self.assertRaises(Exception, msg=CONST_SODDINodesOutOfRange):
            checkingSODDI(soddi, len(list(G_interactions.nodes)))

        # There is no node -1, since there are labelled from 0 to the number of nodes - 1
        soddi = [(2, -1)]
        with self.assertRaises(Exception, msg=CONST_SODDINodesOutOfRange):
            checkingSODDI(soddi, len(list(G_interactions.nodes)))


if __name__ == '__main__':
    unittest.main()
