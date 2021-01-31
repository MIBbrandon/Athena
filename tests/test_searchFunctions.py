import unittest
import networkx as nx

from searching.searchFunctions import findActiveNeighbours, CONST_gInteractionsHasNoActiveOrPassiveNodesMSG, \
	bfsCheckingNeighbours, findBestPendulumForPin, findBestPinPenCombo, mergePaths


class TestFindActiveNeighbours(unittest.TestCase):
	"""
	This function is basically a version of neighbours.
	On a directed graph, G.neighbors() only returns the nodes which have an edge with our input edge going from our
	input edge towards the node edge. findActiveNeighbours will instead return the nodes which have and edge with our
	input edge but go from all the other nodes to our input node.
	"""
	def test_NodeHasNoNeighbours(self):
		# Test than it returns an empty list when the node has no neighbours

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1])

		inputNode = 0
		expectedOutput = []
		obtainedOutput = findActiveNeighbours(G_interactions, inputNode)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_NodeHasOnePassiveNeighbour(self):
		# Test than it returns an empty list when the node has no active neighbours

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1])
		G_interactions.add_edge(0, 1)  # Edge from 0 to 1, not from 1 to 0.

		inputNode = 0
		expectedOutput = []
		obtainedOutput = findActiveNeighbours(G_interactions, inputNode)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_NodeHasOneOrMoreActiveNeighbours(self):
		# Test that it returns the correct list of active neighbours

		# One active neighbour
		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3])
		G_interactions.add_edge(1, 0)  # Edge from 1 to 0, so 1 is an active neighbour of 0

		inputNode = 0
		expectedOutput = [1]
		obtainedOutput = findActiveNeighbours(G_interactions, inputNode)
		self.assertEqual(expectedOutput, obtainedOutput)

		# Two active neighbours
		G_interactions.add_edge(2, 0)

		inputNode = 0
		expectedOutput = [1, 2]
		obtainedOutput = findActiveNeighbours(G_interactions, inputNode)
		self.assertEqual(expectedOutput, obtainedOutput)

		# Three active neighbours
		G_interactions.add_edge(3, 0)

		inputNode = 0
		expectedOutput = [1, 2, 3]
		obtainedOutput = findActiveNeighbours(G_interactions, inputNode)
		self.assertEqual(expectedOutput, obtainedOutput)

class TestBFSCheckingNeighbours(unittest.TestCase):
	"""
	This function executes a BFS search through all of the neighbours and neighbours of neighbours of the input node to
	check if they are an active or passive node (not necessarily in relation to the input node given). Whether the
	function searches for active or passive node depends on the boolean parameter inputted
	"""

	# Output is tuple: (node, depth of node, assignedPlaceholder, path root-node)

	def test_rootMeetsCriteriaAlready(self):
		# Test that a list with just the tuple of root is returned if the root already is a desired node

		# G_swaps is the graph through which the function will traverse
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4])
		G_swaps.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (3, 4)])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4])
		G_interactions.add_edges_from([(1, 0)])  # Root will be passive

		# Test when lookForPassive=True
		inputNode = 0
		expectedOutput = [(0, 0, 't', [0])]
		obtainedOutput = bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=True)
		self.assertEqual(expectedOutput, obtainedOutput)

		# Test when lookForPassive=False
		inputNode = 1
		# Output is tuple: (node, depth of node, assignedPlaceholder, path root-node)
		expectedOutput = [(1, 0, 's', [1])]
		obtainedOutput = bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=False)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_NoNeighboursMeetCriteria(self):
		# Test that an exception is thrown when the function searches and there are no neighbours that meet the criteria
		# If this function runs and it does not find any nodes as either active or passive, it means that there is no
		# edge, and the input critic checkingG_interactions() should have caught this

		# G_swaps is the graph through which the function will traverse
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4])
		G_swaps.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (3, 4)])
		# No edge will be made in G_interactions
		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4])

		# Test when lookForPassive=True
		inputNode = 0
		with self.assertRaises(Exception, msg=CONST_gInteractionsHasNoActiveOrPassiveNodesMSG):
			bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=True)

		# Test when lookForPassive=False (looking for active nodes
		inputNode = 0
		with self.assertRaises(Exception, msg=CONST_gInteractionsHasNoActiveOrPassiveNodesMSG):
			bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=False)

	def test_returnsAllDesiredNodesAtTheSameLevel(self):
		# Test that the function returns ALL of the nodes that meet the criteria of being active/passive and that are
		# on the same level

		# G_swaps is the graph through which the function will traverse
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4])
		G_swaps.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (3, 4)])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4])
		# 4 and 3 are active and on the same level in G_swaps, 1 and 2 are passive and on the same level in G_swaps
		G_interactions.add_edges_from([(4, 1), (4, 2), (3, 1)])

		# With lookForPassive=True (looking for passive nodes on the same level)
		inputNode = 0
		expectedOutput = [(1, 1, "t", [0, 1]), (2, 1, "t", [0, 2])]
		obtainedOutput = bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=True)
		self.assertEqual(expectedOutput, obtainedOutput)

		# With lookForPassive=False (looking for active nodes on the same level)
		inputNode = 0
		expectedOutput = [(3, 2, "s", [0, 1, 3]), (4, 2, "s", [0, 1, 4])]
		obtainedOutput = bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=False)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_IncludesPinsAtGreaterDepth(self):
		# Test that the function includes pins at a greater depth when specified
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_swaps.add_edges_from([(0, 1), (0, 2), (2, 3), (3, 4), (4, 5)])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_interactions.add_edges_from([(2, 1), (3, 1), (4, 1), (5, 1)])

		# lookForPassive=False, since 2, 3, 4 and 5 are active nodes
		inputNode = 0

		# Test for extraLevelsToConsider = -1. Should just default to 0
		expectedOutput = [(2, 1, "s", [0, 2])]
		obtainedOutput = bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=False,
											   extraLevelsToConsider=-1)
		self.assertEqual(expectedOutput, obtainedOutput)

		# Test for extraLevelsToConsider = 1
		expectedOutput = [(2, 1, "s", [0, 2]), (3, 2, "s", [0, 2, 3])]
		obtainedOutput = bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=False,
											   extraLevelsToConsider=1)
		self.assertEqual(expectedOutput, obtainedOutput)

		# Test for extraLevelsToConsider = 2
		expectedOutput = [(2, 1, "s", [0, 2]), (3, 2, "s", [0, 2, 3]), (4, 3, 's', [0, 2, 3, 4])]
		obtainedOutput = bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=False,
											   extraLevelsToConsider=2)
		self.assertEqual(expectedOutput, obtainedOutput)

		# Test for extraLevelsToConsider = 3
		expectedOutput = [(2, 1, "s", [0, 2]), (3, 2, "s", [0, 2, 3]), (4, 3, 's', [0, 2, 3, 4]),
						  (5, 4, "s", [0, 2, 3, 4, 5])]
		obtainedOutput = bfsCheckingNeighbours(G_swaps, G_interactions, inputNode, lookForPassive=False,
											   extraLevelsToConsider=3)
		self.assertEqual(expectedOutput, obtainedOutput)

class TestFindBestPendulumForPin(unittest.TestCase):
	"""
	Given a pin and a soldier, find the best pendulum for the soldier
	"""
	def test_iSourceAsDictator(self):
		# Test that the best pendulum is found when iSource is the dictator and iTarget is the soldier
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5, 6])
		G_swaps.add_edges_from([(0, 1), (0, 2), (0, 3), (3, 4), (3, 5), (5, 6)])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5, 6])
		G_interactions.add_edges_from([(1, 4), (1, 6)])

		dictator = 0
		soldier = 3

		# We will consider the case that we are evaluating the pin (1, 1, "s", [0, 1])
		pin = (1, 1, "s", [0, 1])

		# As the situation is set up now, 1 is an active node going to 4 and 6. However, 4 is closer to our soldier than
		# 6 is. As a result, we want findBestPendulumForPin to give us node 4 as a result

		expectedOutput = (4, 1, "t", [3, 4])
		obtainedOutput = findBestPendulumForPin(G_swaps, G_interactions, soldier, pin)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_iTargetAsDictator(self):
		# Test that the best pendulum is found when iTarget is the dictator and iSource is the soldier
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5, 6])
		G_swaps.add_edges_from([(0, 1), (0, 2), (0, 3), (2, 6), (3, 4), (3, 5) ])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5, 6])
		G_interactions.add_edges_from([(1, 4), (6, 4)])

		dictator = 3
		soldier = 0

		# We will consider the case that we are evaluating the pin (4, 1, "t", [3, 4])
		pin = (4, 1, "t", [3, 4])

		# As the situation is set up now, 1 and 6 are passive nodes going to 4. However, 1 is closer to our soldier than
		# 6 is. As a result, we want findBestPendulumForPin to give us node 1 as a result

		expectedOutput = (1, 1, "s", [0, 1])
		obtainedOutput = findBestPendulumForPin(G_swaps, G_interactions, soldier, pin)
		self.assertEqual(expectedOutput, obtainedOutput)

class TestMergePaths(unittest.TestCase):
	def test_OddCase1(self):
		# This was giving an error due to empty paths being returned from slicing. Make sure it's not the case
		path1 = [15, 0, 23, 1, 10, 13]
		path2 = [1, 23, 0, 15]
		newPath1, newPath2 = mergePaths(path1, path2)
		if not newPath1:
			raise Exception("Empty newPath1")
		elif not newPath2:
			raise Exception("Empty newPath2")

class TestFindBestPinPenCombo(unittest.TestCase):  #TODO: fixing a subfunction
	"""
	Finds the best pin-pendulum combination
	"""
	def test_NoNeedToMoveAtAll(self):
		# Test whether the function detects properly that neither iSource nor iTarget have to move
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_swaps.add_edges_from([(0, 1), (1, 3), (5, 0), (2, 0), (4, 3)])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_interactions.add_edges_from([(0, 1), (5, 1), (0, 3)])

		iSource = 0
		iTarget = 1
		closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
		closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

		allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

		# Now for the real test
		expectedOutput = ((0, 1), (0, 0, 0, 0), ([0], [1], True))
		obtainedOutput = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_OnlyISourceMoves(self):
		# Testing the cases when only iSource needs to move
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_swaps.add_edges_from([(0, 1), (1, 3), (5, 0), (2, 0), (4, 5)])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_interactions.add_edges_from([(5, 1), (4, 1)])

		iSource = 0
		iTarget = 1
		closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
		closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

		allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

		# Finally, we test the output to be correct when iSource has to move once
		expectedOutput = ((1, 5), (0, 1, 0, 0), ([1], [0, 5], True))
		obtainedOutput = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)
		self.assertEqual(expectedOutput, obtainedOutput)

		# Now let's set it up so that iSource has to move twice
		G_interactions.remove_edge(5, 1)

		# Get all the pins again
		iSource = 0
		iTarget = 1
		closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
		closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

		allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

		# The only interaction left is (4, 1), which is 2 swaps away for iSource and 0 swaps away for iTarget
		expectedOutput = ((1, 4), (0, 2, 0, 0), ([1], [0, 5, 4], True))
		obtainedOutput = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_OnlyITargetMoves(self):
		# Testing the cases when only iTarget needs to move
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_swaps.add_edges_from([(0, 1), (1, 3), (5, 0), (2, 0), (4, 3)])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_interactions.add_edges_from([(0, 3), (0, 4)])

		iSource = 0
		iTarget = 1
		closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
		closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

		allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

		# Finally, we test the output to be correct when iTarget has to move once
		expectedOutput = ((0, 3), (0, 1, 0, 0), ([0], [1, 3], True))
		obtainedOutput = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)
		self.assertEqual(expectedOutput, obtainedOutput)

		# Now let's set it up so iTarget has to move twice
		G_interactions.remove_edge(0, 3)

		# Get all the pins again
		iSource = 0
		iTarget = 1
		closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
		closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

		allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

		# The only interaction left is (0, 4), which is 2 swaps away for iTarget and 0 swaps away for iSource
		expectedOutput = ((0, 4), (0, 2, 0, 0), ([0], [1, 3, 4], True))
		obtainedOutput = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_BothITargetAndISourceMove(self):
		# Testing that the correct output is given when both iTarget and iSource have to move
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_swaps.add_edges_from([(0, 1), (1, 3), (3, 4), (0, 5), (5, 2)])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_interactions.add_edges_from([(5, 3), (2, 4)])

		iSource = 0
		iTarget = 1
		closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
		closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

		allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

		# Finally, we test the output to be correct when both iSource and iTarget have to move once
		expectedOutput = ((5, 3), (1, 1, 0, 0), ([0, 5], [1, 3], True))
		obtainedOutput = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)
		self.assertEqual(expectedOutput, obtainedOutput)

		# Now let's make both of them have to move twice
		G_interactions.remove_edge(5, 3)

		# Get all the pins again
		iSource = 0
		iTarget = 1
		closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
		closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

		allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

		# The only interaction left is (2, 4), which is 2 swaps away for iTarget and 2 swaps away for iSource
		expectedOutput = ((2, 4), (2, 2, 0, 0), ([0, 5, 2], [1, 3, 4], True))
		obtainedOutput = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)
		self.assertEqual(expectedOutput, obtainedOutput)

	def test_ITargetAndISourceCrossPaths(self):
		# Test that the output is correct despite the path of iTarget crossing with iSource and viceversa
		G_swaps = nx.Graph()
		G_swaps.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_swaps.add_edges_from([(0, 1), (1, 3), (3, 4), (0, 5), (5, 2)])

		G_interactions = nx.DiGraph()
		G_interactions.add_nodes_from([0, 1, 2, 3, 4, 5])
		G_interactions.add_edges_from([(3, 5)])

		iSource = 0
		iTarget = 1
		closestActiveNodesToSource = bfsCheckingNeighbours(G_swaps, G_interactions, iSource, lookForPassive=False)
		closestPassiveNodesToTarget = bfsCheckingNeighbours(G_swaps, G_interactions, iTarget, lookForPassive=True)

		allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

		expectedOutput = ((3, 5), (2, 2, 0, -1), ([0, 1, 3], [1, 0, 5], True))
		obtainedOutput = findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget)
		self.assertEqual(expectedOutput, obtainedOutput)

	#TODO: continue here


if __name__ == '__main__':
	unittest.main()
