from datetime import time

import networkx as nx


def evaluatePathsInteraction(G_swaps, pin, pen, dictator, soldier):
	"""
	Evaluate whether the dictator should go first or not, and how many more or how many less steps either the
	dictator or the soldier have to take. This will later on affect the paths
	"""
	dictatorPath = pin[3]
	soldierPath = pen[3]

	def adjustGuestPath(hostPath, guestPath):
		if not set(guestPath).issubset(set(hostPath)):  # If guestPath is not a subset of hostPath
			print("Function isInBetween has been called with guestPath %s not actually being contained in "
				  "hostPath %s" % (guestPath, hostPath))
			print("Adjusting path now...")
			print("Original guestPath: " + str(guestPath))

			# Redirect guestPath to be a subset

			# Get the indexes to know which section of hostPath to extract
			indexStartOfGuestPath = hostPath.index(guestPath[0])
			indexEndOfGuestPath = hostPath.index(guestPath[-1])

			# Adjust for the directions of each path
			newGuestPath = None
			if indexStartOfGuestPath < indexEndOfGuestPath:
				newGuestPath = hostPath[indexStartOfGuestPath:indexEndOfGuestPath + 1]
			elif indexStartOfGuestPath > indexEndOfGuestPath:
				newGuestPath = hostPath[indexStartOfGuestPath:indexEndOfGuestPath - 1: -1]

			print("New guestPath: " + str(newGuestPath))
			for i in range(len(guestPath)):
				guestPath[i] = newGuestPath[i]

			print("Check if this actually affected the original guestPath: " + str(guestPath))

	def isInBetween(startNode, toCheckNode, endNode, hostPath, guestPath):
		"""
		Checks if toCheckNode is along the path graph between startNode and endNode. By in between I mean genuinely
		in between, not that toCheckNode is also endNode (toCheckNode will never also be startNode).

		ASSUMPTIONS:
			1) This function is only called when the conditions (pinInSoldierPath, soldierInDictatorPath, etc.) suggest
			   that hostPath and guestPath have an aligned relation
			2) The paths have been aligned by mergePaths() in searchFunctions.py if they neede to be aligned
		"""
		# adjustGuestPath(hostPath, guestPath)

		if startNode == endNode:
			return False
		# First case is considered false, and will be handled by the other branch. Second case has no space in between
		elif toCheckNode == endNode or hostPath.index(startNode) + 1 == hostPath.index(endNode):
			return False

		# Now that there is a chance that toCheckNode may actually be in between the two nodes, let's check
		if toCheckNode in hostPath[hostPath.index(startNode)+1:hostPath.index(endNode)]:
			return True
		return False

	# Return variables
	dictatorFirst = None
	extraDictatorSwaps = 0
	extraSoldierSwaps = 0

	# Conditions. These allow us to determine what kind of situations we have
	pendulumInDictatorPath = False
	pinInSoldierPath = False
	soldierInDictatorPath = False
	dictatorInSoldierPath = False
	if pen[0] in dictatorPath:
		pendulumInDictatorPath = True
	if pin[0] in soldierPath:
		pinInSoldierPath = True
	if soldier in dictatorPath:
		soldierInDictatorPath = True
	if dictator in soldierPath:
		dictatorInSoldierPath = True

	# print("  Pendulum in dictator path: " + str(pendulumInDictatorPath))
	# print("  Pin in soldier path: " + str(pinInSoldierPath))
	# print("  Soldier in dictator path: " + str(soldierInDictatorPath))
	# print("  Dictator in soldier path: " + str(dictatorInSoldierPath))

	# NO CROSSING / WEAK CROSSING
	# The start and end node of each path are not inside the other path, so we don't need to worry, since we are
	# executing one path at a time. This can become a problem in the Weak crossing situation, causing a collision.
	if not pendulumInDictatorPath and not pinInSoldierPath and not soldierInDictatorPath and not dictatorInSoldierPath:
		dictatorFirst = True  # Default. Soldier could have gone first with no problem

	# STRONG CROSSING
	# Either the pin is in the soldier's path or the pen is in the dictator's path.
	if not dictatorInSoldierPath and not soldierInDictatorPath:
		if pendulumInDictatorPath and not pinInSoldierPath:
			# If the soldier were to go first, the dictator would later displace the soldier
			dictatorFirst = True
		elif not pendulumInDictatorPath and pinInSoldierPath:
			# If the dictator were to go first, the soldier would later displace the dictator
			dictatorFirst = False

	# REVERSE STRONG CROSSING
	# Either the soldier is in the dictator's path or the dictator is in the soldier's path, but the goal nodes are out
	elif not pendulumInDictatorPath and not pinInSoldierPath:
		if dictatorInSoldierPath and not soldierInDictatorPath:
			# If the soldier were to go first, the dictator would be displaced before it begins moving
			dictatorFirst = True
		elif soldierInDictatorPath and not dictatorInSoldierPath:
			# If the dictator were to go first, the soldier would be displaced before it begins moving
			dictatorFirst = False

	# PARALLEL REVERSED STRONG CROSSING
	# Same situation as normal reversed strong crossing, just that the pin is in the way of the soldier or the pendulum
	# is in the way of the dictator
	# DS (Dictator path contains soldier but not pendulum, and soldier path contains pin)
	elif not pendulumInDictatorPath and pinInSoldierPath and soldierInDictatorPath and not dictatorInSoldierPath:
		dictatorFirst = False
	# SD (Soldier path contains dictator but not pin, and dictator path contains pendulum)
	elif pendulumInDictatorPath and not pinInSoldierPath and not soldierInDictatorPath and dictatorInSoldierPath:
		dictatorFirst = True

	# CONTAINED
	# DS (Dictator path contains soldier path entirely)
	if not dictatorInSoldierPath and not pinInSoldierPath and soldierInDictatorPath and pendulumInDictatorPath:
		if isInBetween(dictator, pen[0], soldier, dictatorPath, soldierPath):  # Both going in opposite directions
			dictatorFirst = False
			extraSoldierSwaps = -1
		# Both going in the same direction or soldier is already pendulum
		elif soldier == pen[0] or isInBetween(dictator, soldier, pen[0], dictatorPath, soldierPath):
			dictatorFirst = False
			extraSoldierSwaps = 1
		else:
			print("Weird situation of dictatorPath containing soldierPath. Here are the paths:")
			print(" Dictator path: " + str(dictatorPath))
			print(" Soldier path: " + str(soldierPath))
			raise Exception("Check this out")
	# SD (Soldier path contains dictator path entirely)
	elif not soldierInDictatorPath and not pendulumInDictatorPath and dictatorInSoldierPath and pinInSoldierPath:
		if isInBetween(soldier, pin[0], dictator, soldierPath, dictatorPath):  # Both going in opposite directions
			dictatorFirst = True
			extraDictatorSwaps = -1
		# Both going in the same direction or dictator is already pin
		elif dictator == pin[0] or isInBetween(soldier, dictator, pin[0], soldierPath, dictatorPath):
			dictatorFirst = True
			extraDictatorSwaps = 1
		else:
			print("Weird situation of soldierPath containing dictatorPath. Here are the paths:")
			print(" Soldier path: " + str(soldierPath))
			print(" Dictator path: " + str(dictatorPath))
			raise Exception("Check this out")

	# OVERLAP
	# Situations in which there is an overlaps of the paths, and the directions of the paths are always opposing
	# Tails of the paths overlaps
	elif pendulumInDictatorPath and pinInSoldierPath and not soldierInDictatorPath and not dictatorInSoldierPath:
		dictatorFirst = True
		extraDictatorSwaps = -1

	# Heads of the paths overlap
	elif not pinInSoldierPath and not pendulumInDictatorPath and soldierInDictatorPath and dictatorInSoldierPath:
		dictatorFirst = True
		extraSoldierSwaps = -1  # Movement of the dictator moves soldier 1 swap closer to goal already

	# Pin is soldier and pen is dictator, so dictator and soldier just need to switch places
	elif pendulumInDictatorPath and pinInSoldierPath and soldierInDictatorPath and dictatorInSoldierPath:
		dictatorFirst = True
		extraDictatorSwaps = -1

	# Soldier path contains dictator path but dictator is pendulum
	elif pendulumInDictatorPath and pinInSoldierPath and not soldierInDictatorPath and dictatorInSoldierPath:
		dictatorFirst = True
		extraDictatorSwaps = -1

	# Dictator path contains soldier path but soldier is pin
	elif pendulumInDictatorPath and pinInSoldierPath and soldierInDictatorPath and not dictatorInSoldierPath:
		dictatorFirst = False
		extraSoldierSwaps = -1

	# Soldier path contains dictator path but soldier is pin
	elif not pendulumInDictatorPath and pinInSoldierPath and soldierInDictatorPath and dictatorInSoldierPath:
		dictatorFirst = True
		extraDictatorSwaps = -1

	# Dictator path contains soldier path but dictator is pendulum
	elif pendulumInDictatorPath and not pinInSoldierPath and soldierInDictatorPath and dictatorInSoldierPath:
		dictatorFirst = False
		extraSoldierSwaps = -1



	# If we don't have a case for this, raise an error
	if dictatorFirst is None:
		print("Unknown situation! Here are the conditions: ")
		print("  Pendulum in dictator path: " + str(pendulumInDictatorPath))
		print("  Pin in soldier path: " + str(pinInSoldierPath))
		print("  Soldier in dictator path: " + str(soldierInDictatorPath))
		print("  Dictator in soldier path: " + str(dictatorInSoldierPath))
		raise Exception("We don't know how to handle this situation")

	# print("Dictator moves first: " + str(dictatorFirst))
	# print("Extra swaps that dictator has to make: " + str(extraDictatorSwaps))
	# print("Extra swaps that soldier has to make: " + str(extraSoldierSwaps))

	return dictatorFirst, extraDictatorSwaps, extraSoldierSwaps
