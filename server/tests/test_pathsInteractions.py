import unittest
import networkx as nx

from server.evaluation.pathsInteractions import evaluatePathsInteraction
from server.searching.searchFunctions import bfsCheckingNeighbours


class TestEvaluatePathsInteractions(unittest.TestCase):
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		dictator = 0
		soldier = 1
		pin = (3, 1, "s", [0, 3])
		pen = (2, 1, "t", [1, 2])

		# When both paths don't cross or at least the end nodes don't cross, then the dictator moves first, and nobody
		# needs to take any extra steps
		expectedOutput = (True, 0, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		dictator = 0
		soldier = 1
		pin = (3, 2, 's', [0, 2, 3])
		pen = (2, 3, 't', [1, 4, 5, 2])

		# When there is a strong crossing, whichever path contains the goal node of the other must go first
		# For this case here, the dictator must go first
		expectedOutput = (True, 0, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		dictator = 1
		soldier = 0
		pin = (2, 1, 't', [1, 2])
		pen = (3, 4, 's', [0, 4, 5, 2, 3])

		# When there is a strong crossing, whichever path contains the goal node of the other must go first
		# For this case here, the dictator must go first
		expectedOutput = (False, 0, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		dictator = 0
		soldier = 1
		pin = (3, 2, 's', [0, 1, 3])
		pen = (2, 3, 't', [1, 5, 4, 2])

		# When there is a strong crossing, whichever path contains the goal node of the other must go first
		# For this case here, the dictator must go first
		expectedOutput = (False, 0, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		dictator = 0
		soldier = 1
		pin = (2, 1, 's', [0, 2])
		pen = (3, 4, 't', [1, 5, 4, 0, 3])

		# When there is a strong crossing, whichever path contains the goal node of the other must go first
		# For this case here, the dictator must go first
		expectedOutput = (True, 0, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		dictator = 1
		soldier = 0
		pin = (2, 1, 't', [1, 2])
		pen = (3, 3, 's', [0, 1, 2, 3])

		# Expecting the situation of Contained Type I, same side
		expectedOutput = (True, 1, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		dictator = 1
		soldier = 0
		pin = (2, 1, 't', [1, 2])
		pen = (3, 3, 's', [0, 2, 1, 3])

		# Expecting the situation of Contained Type I, same side
		expectedOutput = (True, -1, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_ContainedTypeII(self):
		# Test that the function can detect Contained Type II cases

		# SAME SIDE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		#DS
		dictator = 0
		soldier = 1
		pin = (2, 2, 's', [0, 1, 2])
		pen = (3, 2, 't', [1, 2, 3])

		# Expecting the situation of Contained Type I, same side
		expectedOutput = (False, 0, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		# SD
		dictator = 0
		soldier = 1
		pin = (3, 2, 's', [0, 2, 3])
		pen = (2, 2, 't', [1, 0, 2])

		# Expecting the situation of Contained Type I, same side
		expectedOutput = (True, 0, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
		self.assertEqual(expectedOutput, obtainedOutput)

		# OPPOSITE SIDE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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

		# Simulate first section of findBestPinPenCombo(), until getting into the for-loop and findBestPendulumForPin()
		# DS == SD, but we will always make dictator go first
		dictator = 0
		soldier = 1
		pin = (3, 2, 's', [0, 2, 3])
		pen = (2, 2, 't', [1, 3, 2])

		# Expecting the situation of Contained Type I, same side
		expectedOutput = (True, -1, 0)
		obtainedOutput = evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier)
		self.assertEqual(expectedOutput, obtainedOutput)

if __name__ == '__main__':
	unittest.main()
