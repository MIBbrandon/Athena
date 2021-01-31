import copy

import networkx as nx

from evaluation.pathsInteractions import evaluatePathsInteraction

CONST_gInteractionsHasNoActiveOrPassiveNodesMSG = "G_interaction has no edges. The function checkingG_interactions " \
                                                  "should have caught this."


def findActiveNeighbours(G_interactions, target):
    """
    Input is target, output is a list of nodes that aim at target
    """
    nodesAimingAtTarget = [node for node in range(len(list(G_interactions.nodes)))
                           if target in G_interactions.neighbors(node)]

    return nodesAimingAtTarget


def bfsCheckingNeighbours(G_swaps, G_interactions, root: int, lookForPassive=True, extraLevelsToConsider=0):
    """
    Checking all of the neighbours of the given start node to see if they are active or passive, depending on the
    boolean. Once we find a desired node, we add it to the list desiredNodes, and we only continue checking nodes that
    are on the same level as the first desired node found. We of course keep track of the path to get there. In the end,
    desiredNodes will be a list with at least one tuple of four elements:
        1) Node
        2) Depth (/distance from root/number of swaps for root to take the place of node
        3) Assigned Placeholder (whether the target or the source is meant to replace it)
        4) Path from root to node
    Note that we will not keep track of the assigned placeholder nor path until it is a desired node. This is just for
    performance improvement purposes.
    """
    # TODO: check how the parameter extraLevelsToConsider affects the number of swaps later on on average
    if extraLevelsToConsider < 0: # Negative numbers are invalid, so the default becomes 0
        extraLevelsToConsider = 0
    elif type(extraLevelsToConsider) != int:
        raise Exception("extraLevelsToConsider is not an int")

    # Visited will contain ints of the nodes visited
    # Queue will contain tuples of the form (node, depth of node from root)
    # When we obtain a desired node, we will add the assigned placeholder and the path from the root
    # This will later help to keep track of the number of swaps necessary and what it is supposed to replace
    # "s" is for "source" and "t" is for "target"
    visited = []  # List of ints
    queue = []  # List of tuples of ints
    visited.append(root)
    queue.append((root, 0))

    desiredNodes = []  # All of the nodes that meet the requirements

    while len(queue) > 0:
        newStartNode = queue.pop(0)

        # "SHORT BASE CASE"
        # If we have already some desired nodes and this newStartNode has a depth greater than the desired nodes plus
        # the extra levels that are to be considered, we stop the search and return the desired nodes.
        if len(desiredNodes) > 0 and newStartNode[1] > desiredNodes[0][1] + extraLevelsToConsider:
            # We have checked the entire level of the desired nodes, so we return the desired nodes
            return desiredNodes

        # NOTE: the last parameter in this function allows for admitting pins that are at a depth greater than the node
        # with the shallowest depth. There is a certain trade-off by increasing this number, since you could either find
        # a better option or have wasted time and effort looking for a non-existent better node.

        # LOOKING FOR DESIRED NODES
        #TODO: improve this if else. There is probably a nicer and shorter way to do this,since the only thing that
        # changes is the assigned placeholder ("s" and "t"). However, I don't want this to unpack and repack all nodes,
        # just the ones that meet the conditions, for the sake of performance.
        if lookForPassive and G_interactions.in_degree(newStartNode[0]) > 0:  # Looking for passive nodes
            # If this new node is a desired node, we first unpack it
            desiredNode, depth = newStartNode

            # Then we repack it into another node with more information
            pathIncludedDesiredNode = (desiredNode, depth, "t",
                                       nx.shortest_path(G_swaps, root, desiredNode))

            # Finally, we add it to the list of desiredNodes
            desiredNodes.append(pathIncludedDesiredNode)

        if not lookForPassive and G_interactions.out_degree(newStartNode[0]) > 0:  # Looking for active nodes
            # If this new node is a desired node, we first unpack it
            desiredNode, depth = newStartNode

            # Then we repack it into another node with more information
            pathIncludedDesiredNode = (desiredNode, depth, "s",
                                       nx.shortest_path(G_swaps, root, desiredNode))

            # Finally, we add it to the list of desiredNodes
            desiredNodes.append(pathIncludedDesiredNode)

        # PREPARING FOR THE NEXT ITERATIONS
        for neighbour in list(G_swaps.neighbors(newStartNode[0])):
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append((neighbour, newStartNode[1] + 1))  # These nodes will have a depth of 1 more

    if not desiredNodes:
        # If this point of the code is reached, then no passive nodes have been found, which means there is no edge in
        # G_interactions, which is a problem that the input critics should have caught
        raise Exception(CONST_gInteractionsHasNoActiveOrPassiveNodesMSG)

    # This point is reached when there are no more neighbours to explore (we reach the leaf nodes of the tree graph)
    return desiredNodes


def findBestPinPenCombo(G_swaps, G_interactions, allPinNodes, iSource, iTarget):
    """
    From all the pin nodes obtained, we want to find the corresponding best pendulum, and then we want to find the best
    combination of pin and pendulum, which is the one which will require the fewest swaps.
    """

    allPinNodes.sort(key=lambda tup: tup[1])  # Sort by swaps from dictator to pin
    # The first tuples in candidatePinNodes have the fewest swaps, so we will start by finding their pendulums

    bestPinPenCombo, bestPinPenComboSwaps, bestPinPenComboPaths = None, (float('inf'), float('inf'), float('inf'),
                                                                         float('inf')), None
    for pin in allPinNodes:
        dictator = None
        soldier = None
        if pin[2] == "s":  # If the pin is supposed to hold iSource
            dictator = iSource
            soldier = iTarget  # Then the pendulum is supposed to hold iTarget
        elif pin[2] == "t":  # If the pin is supposed to hold iTarget
            dictator = iTarget
            soldier = iSource  # Then the pendulum is supposed to hold iSource

        # We find the best pen for the pin
        pen = findBestPendulumForPin(G_swaps, G_interactions, soldier, pin)

        #TODO: from this point on is where shit gets crazy. Be prepared.

        # Align the paths if the situation requires it
        newPinPath, newPenPath = mergePaths(pin[3], pen[3])

        # Repackage pin and pen with their new paths
        pin = (pin[0], pin[1], pin[2], newPinPath)
        pen = (pen[0], pen[1], pen[2], newPenPath)

        dictatorFirst, extraDictatorSwaps, extraSoldierSwaps = evaluatePathsInteraction(G_swaps, pin, pen, dictator,
                                                                                        soldier)
        finalDictatorSwaps = (pin[1] + extraDictatorSwaps)
        finalSoldierSwaps = (pen[1] + extraSoldierSwaps)
        totalPinPenComboSwaps = finalDictatorSwaps + finalSoldierSwaps

        # Compare this pin-pen combo with the best one so far
        if totalPinPenComboSwaps < bestPinPenComboSwaps[0] + bestPinPenComboSwaps[1] + bestPinPenComboSwaps[2] + \
                bestPinPenComboSwaps[3]:
            bestPinPenCombo = (pin[0], pen[0])
            bestPinPenComboSwaps = (pin[1], pen[1], extraDictatorSwaps, extraSoldierSwaps)
            bestPinPenComboPaths = (pin[3], pen[3], dictatorFirst)

    if bestPinPenCombo is None or bestPinPenComboPaths[0] is None or bestPinPenComboPaths[1] is None:
        raise Exception("No pin pen combo found. This should not happen")

    return bestPinPenCombo, bestPinPenComboSwaps, bestPinPenComboPaths


def findBestPendulumForPin(G_swaps, G_interactions, soldier, pin):
    """
    Given a pin, find the best pendulum for the soldier
    """
    pendulumsToLookAt = None  # List of nodes we should be looking at
    associatedHolder = None  # iSource or iTarget
    if pin[2] == "s":  # Pin node will hold iSource, the dictator
        pendulumsToLookAt = list(G_interactions.neighbors(pin[0]))
        associatedHolder = "t"  # Pendulum will hold iTarget, the soldier
    elif pin[2] == "t":  # Pin node will hold iTarget, the dictator
        pendulumsToLookAt = findActiveNeighbours(G_interactions, pin[0])
        associatedHolder = "s"  # Pendulum will hold iSource, the soldier

    # The best pendulum is the one with the shortest path for the soldier
    bestPendulum, bestPendulumSwaps, bestPendulumPath = None, float('inf'), None
    for pendulum in pendulumsToLookAt:
        pendulumPath = nx.shortest_path(G_swaps, soldier, pendulum)
        pendulumSwaps = len(pendulumPath) - 1
        if pendulumSwaps < bestPendulumSwaps:
            bestPendulum = pendulum
            bestPendulumSwaps = pendulumSwaps
            bestPendulumPath = pendulumPath

    return bestPendulum, bestPendulumSwaps, associatedHolder, bestPendulumPath

def mergePaths(path1, path2):
    """
    Merge two paths depending on their relation with one another:
        1) path2 is contained inside of path1
        2) path1 is contained inside of path2
        3) Tails of paths overlap
        4) Heads of paths overlap

    Returns newPath1, newPath2
    """
    # path2 inside of path1
    if path2[0] in path1 and path2[-1] in path1:
        startIndex = path1.index(path2[0])
        endIndex = path1.index(path2[-1])
        if startIndex < endIndex:
            return path1, path1[startIndex:endIndex + 1]
        elif startIndex > endIndex:
            return path1, path1[endIndex:startIndex + 1:][::-1]
        else:
            return path1, path2

    # path1 inside of path2
    elif path1[0] in path2 and path1[-1] in path2:
        startIndex = path2.index(path1[0])
        endIndex = path2.index(path1[-1])
        if startIndex < endIndex:
            return path2[startIndex:endIndex + 1], path2
        elif startIndex > endIndex:
            return path2[endIndex:startIndex+1:][::-1], path2
        else:
            return path1, path2

    # For both following overlap cases, path2 will always be adjusted to path1
    # Tails overlap
    elif path1[-1] in path2 and path2[-1] in path1:
        startIndex = path2.index(path1[-1])
        x = 0
        alteredPath2 = copy.deepcopy(path2)
        for i in range(startIndex, len(path2)):
            # As path2 goes forward from startIndex to end, path1 goes backwards from end
            alteredPath2[i] = path1[-(1+x)]
            x += 1
        return path1, alteredPath2

    # Heads overlap
    elif path1[0] in path2 and path2[0] in path1:
        endIndex = path2.index(path1[0])
        path1StartIndex = path1.index(path2[0])
        alteredPath2 = copy.deepcopy(path2)
        for i in range(endIndex+1):
            # As path2 goes forward to endIndex, path1 goes backwards from path1StartIndex
            alteredPath2[i] = path1[path1StartIndex-i]
        return path1, alteredPath2

    # It's a situation that does not require path merging
    else:
        return path1, path2
