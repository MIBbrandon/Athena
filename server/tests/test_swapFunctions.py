import unittest
import networkx as nx

from server.critics.inputCritics import checkingG_swaps, checkingG_interactions, checkingSODDI
from server.searching.searchFunctions import bfsCheckingNeighbours, findBestPinPenCombo
from server.swapping.swapFunctions import representSwaps, CONST_notListOfIntsOrNotBool, executeSwaps, swapsRequired


class TestRepresentSwaps(unittest.TestCase):
    """
    The function representSwaps simply receives a given path and a boolean, and it simply returns the path once we
    have swapped the node at path[0] to the end of the path, and the boolean simply determines whether we want that
    node to go to the penultimate or last position of the path.
    """
    def test_representSwapsIncorrectInput(self):
        # Test that an exception is thrown when the wrong input parameters are given
        G_swaps = nx.Graph()
        G_swaps.add_edges_from([(0, 1), (1, 2), (2, 3)])

        # Enter something that is not a list as first parameter
        with self.assertRaises(ValueError, msg=CONST_notListOfIntsOrNotBool):
            representSwaps(G_swaps, 42, True)

        # Enter something that is not a list of ints as first parameter
        with self.assertRaises(ValueError, msg=CONST_notListOfIntsOrNotBool):
            representSwaps(G_swaps, ["#"], True)

        # Enter something that is not a boolean as second parameter
        with self.assertRaises(ValueError, msg=CONST_notListOfIntsOrNotBool):
            representSwaps(G_swaps, [0, 1], "#")

    def test_swapPathOfLength1(self):
        # Test that it can output the correct result when the path is of length 1
        G_swaps = nx.Graph()
        G_swaps.add_edges_from([(0, 1), (1, 2), (2, 3)])

        # With swapEndNodes=False
        inputPath = [0]
        expectedOutputPath = [0]
        obtainedOutputPath = representSwaps(G_swaps, inputPath, swapEndNodes=False)
        self.assertEqual(expectedOutputPath, obtainedOutputPath)

        # With swapEndNodes=True
        obtainedOutputPath = representSwaps(G_swaps, inputPath, swapEndNodes=True)
        self.assertEqual(expectedOutputPath, obtainedOutputPath)

    def test_swapPathOfLength2(self):
        # Test that it can output the correct result when the path is of length 2
        G_swaps = nx.Graph()
        G_swaps.add_edges_from([(0, 1), (1, 2), (2, 3)])

        # With swapEndNodes=False
        inputPath = [0, 1]
        expectedOutputPath = [0, 1]
        obtainedOutputPath = representSwaps(G_swaps, inputPath, swapEndNodes=False)
        self.assertEqual(expectedOutputPath, obtainedOutputPath)

        # With swapEndNodes=True
        inputPath = [0, 1]
        expectedOutputPath = [1, 0]
        obtainedOutputPath = representSwaps(G_swaps, inputPath, swapEndNodes=True)
        self.assertEqual(expectedOutputPath, obtainedOutputPath)

    def test_swapPathOfLengthGreaterThan2(self):
        # Test that it can output the correct result when the path is of length 3 or more
        G_swaps = nx.Graph()
        G_swaps.add_edges_from([(0, 1), (1, 2), (2, 3)])

        # Length 3
        # With swapEndNodes=False
        inputPath = [0, 1, 2]
        expectedOutputPath = [1, 0, 2]
        obtainedOutputPath = representSwaps(G_swaps, inputPath, swapEndNodes=False)
        self.assertEqual(expectedOutputPath, obtainedOutputPath)

        # With swapEndNodes=True
        inputPath = [0, 1, 2]
        expectedOutputPath = [1, 2, 0]
        obtainedOutputPath = representSwaps(G_swaps, inputPath, swapEndNodes=True)
        self.assertEqual(expectedOutputPath, obtainedOutputPath)

        # Length 4
        # With swapEndNodes=False
        inputPath = [0, 1, 2, 3]
        expectedOutputPath = [1, 2, 0, 3]
        obtainedOutputPath = representSwaps(G_swaps, inputPath, swapEndNodes=False)
        self.assertEqual(expectedOutputPath, obtainedOutputPath)

        # With swapEndNodes=True
        inputPath = [0, 1, 2, 3]
        expectedOutputPath = [1, 2, 3, 0]
        obtainedOutputPath = representSwaps(G_swaps, inputPath, swapEndNodes=True)
        self.assertEqual(expectedOutputPath, obtainedOutputPath)

class TestExecuteSwaps(unittest.TestCase):
    #TODO: test all of the different intersection of paths and the order of execution
    # Test whether the function detects properly that neither iSource nor iTarget have to move

    # COMMON WITH TEST_SEARCHFUNCTIONS.PY ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def test_NoNeedToMoveAtAll(self):
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_swaps.add_edges_from([(0, 1), (1, 3), (5, 0), (2, 0), (4, 3)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(0, 1), (5, 1), (0, 3)])

        # There already exists an interaction edge (0, 1)
        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {1: 1, 0: 0}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    def test_OnlyISourceMoves(self):
        # Testing the cases when only iSource needs to move
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_swaps.add_edges_from([(0, 1), (1, 3), (5, 0), (2, 0), (4, 5)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(5, 1), (4, 1)])

        # We want to use the interaction (5, 1), so 0 should go to 5
        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 5, 1: 1, 5: 0}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    def test_OnlyITargetMoves(self):
        # Testing the cases when only iTarget needs to move
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_swaps.add_edges_from([(0, 1), (1, 3), (5, 0), (2, 0), (4, 3)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(0, 3), (0, 4)])

        # We want to use the interaction (0, 3), so 1 should go to 3
        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 0, 1: 3, 3: 1}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    def test_BothITargetAndISourceMove(self):
        # Testing that the correct output is given when both iTarget and iSource have to move
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_swaps.add_edges_from([(0, 1), (1, 3), (3, 4), (0, 5), (5, 2)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(5, 3), (2, 4)])

        # We want to use the interaction (5, 3), so 0 should go to 5 and 1 should go to 3
        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 5, 5: 0, 1: 3, 3: 1}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    def test_ITargetAndISourceCrossPaths(self):
        # Test that the output is correct despite the path of iTarget crossing with iSource and viceversa
        # Testing that the correct output is given when both iTarget and iSource have to move
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_swaps.add_edges_from([(0, 1), (1, 3), (3, 4), (0, 5), (5, 2)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(3, 5)])

        # We want to use the interaction (3, 5), so 0 should go to 3 and 1 should go to 5, crossing paths
        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {1: 3, 0: 5, 5: 1, 3: 0}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # COMMON WITH TEST_PATHSINTERACTINOS.PY ****************************************************************************
    def test_NoCrossingAndWeakCrossing(self):
        # Testing that the function evaluates the interaction between the paths correctly when they don't cross
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3])
        G_swaps.add_edges_from([(0, 1), (1, 2), (0, 3)])
        # Basically a path graph [3, 0, 1, 2]

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(3, 2)])
        # Only interaction is (3, 2)

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 3, 3: 0, 1: 2, 2: 1}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    def test_StrongCrossing(self):
        # Testing that the function evaluates the interaction between the paths correctly when they strong-cross
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_swaps.add_edges_from([(0, 2), (2, 3), (1, 4), (4, 5), (5, 2)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(3, 2)])
        # Only interaction is (3, 2)

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 2, 1: 4, 2: 1, 3: 0, 4: 5, 5: 3}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

        ################################################################################################################

        # Now let's set it up so that the soldier must go first
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_swaps.add_edges_from([(0, 4), (4, 5), (5, 2), (2, 3), (1, 2)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(3, 2)])
        # Only interaction is (3, 2)

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 4, 1: 3, 2: 1, 3: 0, 4: 5, 5: 2}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    def test_ReversedStrongCrossing(self):
        # Testing that the function evaluates the interaction between the paths correctly when they reverse-strong-cross
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_swaps.add_edges_from([(0, 1), (1, 3), (1, 5), (5, 4), (4, 2)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(3, 2)])

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 5, 1: 3, 2: 1, 3: 0, 4: 2, 5: 4}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

        ################################################################################################################

        # Now let's set up the situation so that the dictator has to get out of the way of the soldier first
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_swaps.add_edges_from([(1, 5), (5, 4), (4, 0), (0, 3), (0, 2)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
        G_interactions.add_edges_from([(2, 3)])

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 3, 1: 5, 2: 0, 3: 1, 4: 2, 5: 4}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    def test_ContainedTypeI(self):
        # Test that the function can detect Contained Type I cases
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3])
        G_swaps.add_edges_from([(0, 1), (1, 2), (2, 3)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])
        G_interactions.add_edges_from([(3, 2)])

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 2, 1: 3, 2: 1, 3: 0}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

        ################################################################################################################

        # Now let's set up the situation so that the function detects a Contained Type I, opposite side
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3])
        G_swaps.add_edges_from([(0, 2), (2, 1), (1, 3)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])
        G_interactions.add_edges_from([(3, 2)])

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 2, 1: 3, 2: 1, 3: 0}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    def test_ContainedTypeII(self):
        # Test that the function can detect Contained Type II cases

        # SAME SIDE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Tail overlaps with head
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3])
        G_swaps.add_edges_from([(0, 1), (1, 2), (2, 3)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])
        G_interactions.add_edges_from([(2, 3)])

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 2, 1: 3, 2: 0, 3: 1}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

        ################################################################################################################

        # Alternate to making the dictator go first
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3])
        G_swaps.add_edges_from([(1, 0), (0, 2), (2, 3)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])
        G_interactions.add_edges_from([(3, 2)])

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 3, 1: 2, 2: 1, 3: 0}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

        # OPPOSITE SIDE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Tails overlap
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3])
        G_swaps.add_edges_from([(0, 2), (2, 3), (3, 1)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])
        G_interactions.add_edges_from([(3, 2)])

        iSource = 0
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 2, 1: 3, 2: 1, 3: 0}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

    def test_tinyContained(self):
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from([0, 1, 2, 3])
        G_swaps.add_edges_from([(0, 1), (1, 2), (2, 3)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from([0, 1, 2, 3])
        G_interactions.add_edges_from([(0, 1)])

        iSource = 2
        iTarget = 1
        closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPen = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)

        swapSteps, mapping = executeSwaps(G_swaps, G_interactions, bestPinPen)

        expectedOutput = {0: 2, 1: 1, 2: 0}
        obtainedOutput = mapping
        self.assertEqual(expectedOutput, obtainedOutput)

class TestSwapsRequired(unittest.TestCase):

    def test_OddCase1(self):
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from(range(25))
        G_swaps.add_edges_from(
            [(0, 10), (0, 14), (1, 13), (1, 15), (1, 21), (2, 4), (2, 9), (3, 5), (3, 16), (3, 19), (4, 21), (5, 20),
             (6, 8), (7, 10), (7, 22), (7, 23), (8, 11), (8, 17), (8, 21), (8, 22), (9, 21),
             (10, 16), (10, 24), (11, 21), (12, 19), (13, 18), (15, 16)])
        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from(range(25))
        G_interactions.add_edges_from([(4, 10), (6, 23), (24, 23)])
        soddi = [(6, 7), (6, 20), (15, 5), (20, 6), (15, 7), (7, 13), (21, 5), (0, 12), (4, 12), (18, 12), (6, 22), (14, 7),
                 (7, 18), (4, 10), (5, 20), (18, 13), (5, 20), (2, 14), (7, 2), (15, 17), (24
                                                                                           , 9), (23, 15), (14, 3), (22, 2),
                 (5, 7), (18, 12), (19, 1), (1, 24), (13, 14), (12, 14), (17, 18), (9, 12), (1, 13), (2, 10), (8, 16),
                 (13, 8), (8, 17), (2, 7), (7, 21), (11, 8), (11,
                                                              7), (13, 3), (16, 20), (24, 11), (10, 1), (17, 2), (15, 10),
                 (1, 19), (18, 16), (7, 17), (21, 4), (5, 0), (4, 10), (13, 9), (8, 20), (5, 18), (7, 5), (19, 8), (15, 8),
                 (6, 13), (10, 11)
            , (4, 6), (12, 4), (19, 9), (12, 16), (2, 0), (8, 20), (18, 23), (21, 22), (5, 20), (10, 9), (10, 18), (24, 12),
                 (22, 14), (10, 23), (23, 12), (19, 10), (5, 1), (5, 9), (0, 21), (17, 11
                                                                                   ), (4, 16), (0, 15), (17, 8), (3, 20),
                 (3, 12), (3, 6), (13, 17), (22, 13), (18, 24), (18, 23), (21, 1), (24, 8), (5, 9), (14, 22), (20, 2),
                 (18, 8), (5, 10), (0, 21), (4, 11), (2, 9),
                 (19, 23), (1, 0), (17, 4), (5, 19), (10, 13), (2, 9), (8, 15), (0, 4), (7, 6), (14, 24), (16, 14), (24, 7),
                 (23, 4), (7, 21), (16, 22), (5, 2), (16, 5), (10, 22), (24, 23), (15, 8), (6,
                                                                                            17), (12, 2), (15, 23), (18, 0),
                 (19, 1), (18, 19), (1, 3), (5, 16), (7, 19), (12, 24), (16, 0), (16, 4), (12, 5), (2, 19), (8, 19), (7, 3),
                 (8, 5), (17, 19), (7, 14), (20, 7), (2, 15)
            , (17, 20), (6, 0), (21, 2), (24, 1), (24, 23), (0, 18), (24, 9), (11, 22), (19, 15), (7, 22), (2, 1), (13, 15),
                 (11, 6), (21, 7), (12, 24), (3, 23), (12, 24), (13, 18), (2, 10), (14, 18), (20, 1), (2, 6), (2, 10),
                 (3, 13), (21, 0), (13, 8), (13, 10), (7, 20), (12, 5), (1, 20), (2, 21), (11, 8), (4, 11), (16, 23),
                 (24, 17), (10, 12), (6, 5), (22, 1), (13, 10), (12, 24
                                                                 ), (0, 20), (15, 18), (9, 2), (1, 15), (10, 18), (2, 6),
                 (8, 19), (15, 22), (17, 5), (7, 6), (14, 0), (21, 12), (24, 18), (15, 9), (5, 18), (21, 1), (18, 23),
                 (5, 1), (4, 5), (21, 4), (
                     22, 10), (9, 13), (2, 0), (3, 7), (10, 15), (8, 1), (10, 15), (23, 6), (13, 14), (6, 13), (4, 7),
                 (15, 9), (14, 8), (7, 2), (10, 4), (0, 1), (1, 17), (5, 17), (7, 8), (13, 11), (24, 11)
            , (21, 23), (4, 8), (10, 16), (20, 12), (16, 18), (21, 6), (15, 24), (17, 5), (10, 5), (18, 9), (10, 13),
                 (6, 15), (13, 7), (23, 13), (1, 3), (12, 0), (8, 18), (13, 8), (0, 22), (7, 15)
            , (8, 7), (24, 14), (16, 2), (12, 10), (8, 14), (15, 21), (11, 9), (9, 12), (1, 19), (14, 17), (12, 14),
                 (14, 12), (17, 18), (5, 24), (10, 20), (19, 24), (24, 23), (6, 14), (16, 6), (3,
                                                                                               23), (6, 15), (9, 15),
                 (6, 10), (12, 5), (8, 13), (1, 22), (22, 12), (18, 24), (14, 16), (18, 11), (12, 24), (14, 8), (7, 0),
                 (17, 0), (5, 13), (3, 6), (16, 3), (7, 1), (0, 3), (13, 9)
            , (13, 9), (13, 9), (12, 3), (23, 0), (9, 1), (10, 23), (5, 14), (1, 14), (14, 9), (3, 6), (21, 9), (3, 12),
                 (21, 12), (24, 20), (10, 0), (19, 7), (0, 1), (9, 3), (7, 23), (13, 22), (23
                                                                                           , 12), (24, 18), (0, 24),
                 (6, 24), (5, 23), (8, 15), (8, 13), (18, 2), (4, 9), (11, 4), (19, 10), (12, 5), (6, 18), (14, 22),
                 (18, 9), (24, 13), (5, 0), (14, 5), (12, 1), (4, 16), (4, 24), (19, 14), (12, 11), (13, 7), (24, 16),
                 (4, 15), (19, 12), (8, 23), (9, 24), (6, 21), (20, 11), (19, 13), (17, 11), (12, 8), (5, 13), (17, 5),
                 (0, 21), (1, 17), (3, 1), (1, 24), (3,
                                                     21), (8, 11), (24, 1), (5, 23), (16, 10), (10, 17), (22, 2), (4, 23),
                 (11, 1), (15, 3), (3, 22), (21, 19), (14, 7), (4, 20), (23, 6), (1, 20), (18, 2), (2, 10), (11, 20),
                 (9, 8), (0, 13
                          ), (14, 6), (9, 8), (13, 15), (10, 1), (10, 23), (3, 18), (0, 19), (8, 23), (6, 16), (4, 12)]

        # Checking requirement 1
        checkingG_swaps(G_swaps)

        # Checking requirement 2
        checkingG_interactions(G_interactions)

        # Checking requirement 3
        checkingSODDI(soddi, len(list(G_swaps.nodes)))

        newG_swaps, newG_interactions, swaps = swapsRequired(G_swaps, G_interactions, soddi)

    def test_OddCase2(self):
        G_swaps = nx.Graph()
        G_swaps.add_nodes_from(range(25))
        G_swaps.add_edges_from([(0, 6), (0, 11), (0, 15), (0, 12), (1, 16), (1, 11), (1, 23), (2, 18), (2, 17), (3, 15), (3, 17), (3, 5), (4, 5), (5, 19), (5, 18), (7, 11), (8, 10), (9, 13), (10, 23), (12, 20), (12, 13), (14, 23), (15, 21), (16, 21), (18, 20), (21, 24), (22, 24)])

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from(range(25))
        G_interactions.add_edges_from([(8, 19)])
        soddi = [(15, 1)]
#                 [(1, 2), (21, 14), (24, 21), (11, 6), (7, 8),
#  (23, 10), (8, 24), (8, 12), (4, 17), (22, 21), (24, 19), (23, 21), (15, 21), (12, 8), (3, 5), (16, 13), (8, 12), (8, 9), (20, 14), (20, 6), (4, 17), (22, 6), (19, 11), (19, 12), (5, 15
# ), (17, 9), (8, 17), (7, 11), (3, 21), (0, 9), (9, 11), (7, 3), (23, 10), (14, 4), (0, 16), (20, 21), (19, 9), (10, 18), (12, 11), (15, 5), (17, 2), (7, 1), (8, 19), (19, 21), (13, 21),
#  (0, 1), (12, 6), (22, 16), (6, 16), (14, 19), (8, 24), (9, 8), (10, 7), (1, 13), (22, 4), (0, 16), (24, 4), (13, 1), (7, 17), (12, 16), (12, 14), (21, 4), (24, 18), (9, 11), (17, 12),
# (16, 15), (18, 17), (6, 4), (5, 12), (14, 24), (16, 2), (21, 20), (5, 23), (24, 2), (19, 1), (22, 1), (1, 20), (0, 12), (10, 5), (10, 20), (16, 9), (23, 4), (16, 21), (13, 14), (8, 22),
#  (7, 22), (8, 23), (3, 0), (3, 13), (13, 15), (0, 10), (20, 11), (19, 8), (3, 15), (4, 0), (7, 23), (6, 7), (18, 24), (20, 0), (12, 2), (4, 17), (1, 13), (6, 17), (23, 13), (16, 9), (3,
#  15), (18, 19), (17, 2), (13, 21), (23, 11), (3, 19), (23, 8), (19, 16), (10, 15), (16, 13), (8, 22), (3, 4), (1, 21), (9, 0), (7, 18), (7, 2), (6, 1), (21, 7), (11, 3), (0, 2), (18, 8)
# , (16, 4), (9, 24), (10, 1), (6, 17), (19, 15), (22, 9), (17, 22), (7, 19), (1, 24), (19, 2), (19, 20), (7, 11), (9, 1), (17, 3), (2, 7), (15, 19), (13, 6), (19, 24), (9, 7), (15, 22),
# (24, 7), (14, 23), (7, 16), (1, 12), (24, 2), (22, 2), (6, 2), (5, 0), (11, 0), (24, 2), (6, 17), (23, 12), (15, 12), (7, 15), (20, 19), (16, 22), (2, 7), (4, 3), (23, 17), (13, 19), (1
# , 5), (20, 23), (15, 21), (6, 24), (17, 22), (14, 1), (22, 21), (4, 2), (3, 22), (19, 5), (24, 22), (5, 23), (9, 5), (1, 18), (20, 6), (7, 0), (3, 8), (17, 5), (1, 15), (6, 0), (3, 14),
#  (22, 6), (10, 7), (12, 23), (17, 9), (18, 12), (14, 4), (24, 3), (5, 18), (24, 5), (10, 15), (22, 21), (24, 2), (22, 6), (18, 12), (8, 9), (16, 6), (4, 16), (14, 20), (18, 6), (18, 11)
# , (22, 24), (12, 11), (13, 12), (22, 15), (20, 17), (22, 16), (10, 11), (21, 17), (16, 1), (10, 7), (8, 15)]


        # Checking requirement 1
        checkingG_swaps(G_swaps)

        # Checking requirement 2
        checkingG_interactions(G_interactions)

        # Checking requirement 3
        checkingSODDI(soddi, len(list(G_swaps.nodes)))

        # Now that we have checked the inputs, let's evaluate what is the minimum number of swaps required to achieve
        # all of the desired interactions

        # First, we want to measure how many swaps are necessary with the initial configuration
        newG_swaps, newG_interactions, swaps = swapsRequired(G_swaps, G_interactions, soddi)

if __name__ == '__main__':
    unittest.main()
