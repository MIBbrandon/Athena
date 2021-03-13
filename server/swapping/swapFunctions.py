import copy
from typing import List, Tuple

from critics.processingCritics import checkSwapStepsMakesSense, checkDesiredInteractionIsAchieved
from graphDrawing.graphDrawingMethods import drawStepsInGraph
from graphDrawing.graphRelabelling import relabelGraphs
from searching.searchFunctions import bfsCheckingNeighbours, findBestPinPenCombo

CONST_notListOfIntsOrNotBool = "First parameter must be a list of ints and second parameter must be a boolean"


def representSwaps(G_swaps, path: List[int], swapEndNodes: bool):
    """
    This method executes all of the swaps necessary to get path[0] to path[-2]. If swapEndNodes == True, then path[0]
    will be swapped up to path[-1]. The altered path is returned
    """
    if not(isinstance(path, list) and type(swapEndNodes) == bool):
        raise ValueError(CONST_notListOfIntsOrNotBool)
    for element in path:
        if not(type(element) == int):
            raise ValueError(CONST_notListOfIntsOrNotBool)
    if len(path) <= 1:  # If the path is just of length 1, return it as is, there is nothing to do
        return path

    # # Check that there actually exists a path
    # for i in range(1, len(path)-1):
    #     if not G_swaps.has_edge(path[i-1], path[i]):
    #         raise Exception("Path is invalid. The swap-edge %s does not exist" % str((path[i-1], path[i])))

    toReturnPath = copy.deepcopy(path)
    if swapEndNodes:
        toReturnPath.append(toReturnPath.pop(0))
    else:
        toReturnPath.insert(-1, toReturnPath.pop(0))
    return toReturnPath


def executeSwaps(G_swaps, G_interactions, pinPen):
    """
    Executes the swaps accordingly
    """
    mapping = {}
    swapSteps = []

    # Unpacking pinPen
    dictator, soldier = pinPen[0]
    dictatorSwaps, soldierSwaps, extraDictatorSwaps, extraSoldierSwaps = pinPen[1]
    dictatorPath, soldierPath, dictatorFirst = pinPen[2]

    if not dictatorPath:
        raise Exception("Dictator path is empty. This should not happen")
    if not soldierPath:
        raise Exception("Soldier path is empty. This should not happen")
    if dictatorFirst is None:
        raise Exception("Boolean dictatorFirst is empty. This should not happen")

    def getNextNode(hostPath, guestPath):
        """
        Gets the next node in hostPath that will follow guestPath.
        Example:
            hostPath = [0, 1, 2, 3]
            guestPath = [1, 2]
            print(getNextNode(hostPath, guestPath))

            >Output: 3
        """
        lastElementInGuestPath = guestPath[-1]
        correspondingIndexInHostPath = hostPath.index(lastElementInGuestPath)
        return hostPath[correspondingIndexInHostPath + 1]

    def mapChanges(alteredFirstPath, alteredSecondPath, indexesOfIntersectionNodesOnFirstPath, mapping,
                   originalFirstPath,
                   originalSecondPath):
        for i in range(len(alteredSecondPath)):
            mapping.update({originalSecondPath[i]: alteredSecondPath[i]})
        for i in range(len(alteredFirstPath)):
            if i not in indexesOfIntersectionNodesOnFirstPath:  # Ignoring firstPath where there is an intersection
                mapping.update({originalFirstPath[i]: alteredFirstPath[i]})

    def updateSwapSteps(originalFirstPath, swapSteps):
        """
        Simply inserts tuples into swapSteps which represent the swaps that are necessary to carry out the desired
        interaction
        """
        if len(originalFirstPath) != 1:
            for i in range(1, len(originalFirstPath)):
                swapSteps.append((originalFirstPath[0], originalFirstPath[i]))

    def preparePathsAccordingToEvaluationResults(dictatorFirst, dictatorPath, extraDictatorSwaps, extraSoldierSwaps,
                                                 getNextNode, soldierPath):
        if dictatorFirst:
            if extraDictatorSwaps == -1 and len(dictatorPath) > 1:
                dictatorPath.pop()
            elif extraDictatorSwaps == 1:
                dictatorPath.append(getNextNode(soldierPath, dictatorPath))
        else:
            if extraSoldierSwaps == -1 and len(soldierPath) > 1:
                soldierPath.pop()
            elif extraSoldierSwaps == 1:
                soldierPath.append(getNextNode(dictatorPath, soldierPath))

    if dictatorFirst:
        firstPath = dictatorPath
        secondPath = soldierPath
    else:
        firstPath = soldierPath
        secondPath = dictatorPath

    # Check that the original length of the path matches the number of swaps for each path
    if dictatorSwaps != len(dictatorPath)-1 or soldierSwaps != len(soldierPath)-1:
        raise Exception("Error: path lengths don't match originally assigned swaps")

    preparePathsAccordingToEvaluationResults(dictatorFirst, dictatorPath, extraDictatorSwaps, extraSoldierSwaps,
                                             getNextNode, soldierPath)

    # Check that the altered path (due to conditions) has the expected length
    if dictatorFirst and len(dictatorPath) - 1 != dictatorSwaps + extraDictatorSwaps:
        raise Exception("Length of dictator path (firstPath) is not as expected")
    elif not dictatorFirst and len(soldierPath) - 1 != soldierSwaps + extraSoldierSwaps:
        raise Exception("Length of soldier path (firstPath) is not as expected")

    # Keep a copy of what the "original" paths look like
    originalFirstPath = copy.deepcopy(firstPath)
    originalSecondPath = copy.deepcopy(secondPath)

    intersectionNodes = list(set(firstPath).intersection(secondPath))  # Get nodes that will change for secondPath
    indexesOfIntersectionNodesOnFirstPath = []  # These are to be ignored by mapping, since secondPath will be correct

    # Get the list that represents what the path will look like once all the swaps have been executed
    alteredFirstPath = representSwaps(G_swaps, firstPath, swapEndNodes=True)

    for common in intersectionNodes:
        # Updates nodes for mapping to ignore from firstPath
        index = originalFirstPath.index(common)
        indexesOfIntersectionNodesOnFirstPath.append(index)

        # Updating the labels on the nodes of the second path
        secondPath[originalSecondPath.index(common)] = alteredFirstPath[index]

    # Get what the second path looks like after the first path has been executed
    somewhatOriginalSecondPath = copy.deepcopy(secondPath)

    # If the start node of the second path has been displaced to the second position
    toReinsert = None
    if originalSecondPath[0] != somewhatOriginalSecondPath[0]:
        toReinsert = somewhatOriginalSecondPath.pop(0)  # Remove the node in the first position

    # Check that the altered path due to firstPath's execution has the expected length
    if not dictatorFirst and len(somewhatOriginalSecondPath) - 1 != dictatorSwaps + extraDictatorSwaps:
        raise Exception("Length of dictator path (secondPath) is not as expected")
    elif dictatorFirst and len(somewhatOriginalSecondPath) - 1 != soldierSwaps + extraSoldierSwaps:
        raise Exception("Length of soldier path (secondPath) is not as expected")

    alteredSecondPath = representSwaps(G_swaps, somewhatOriginalSecondPath, swapEndNodes=True)

    # Reinsert the node in the first position
    if toReinsert is not None:
        alteredSecondPath.insert(0, toReinsert)

    # Mapping the node alterations
    mapChanges(alteredFirstPath, alteredSecondPath, indexesOfIntersectionNodesOnFirstPath, mapping, originalFirstPath,
               originalSecondPath)

    # print("-------------------------------------------------------------------------------")
    # print("Original First Path: " + str(originalFirstPath))
    # print("Altered First Path: " + str(alteredFirstPath))
    # print("\nIntersection nodes: " + str(intersectionNodes))
    # print("\nOriginal Second Path: " + str(originalSecondPath))
    # print("Second Path after First Path effects: " + str(somewhatOriginalSecondPath))
    # print("Altered Second Path: " + str(alteredSecondPath))
    # print("Final mapping: " + str(mapping))
    # print("-------------------------------------------------------------------------------")

    # Keep track of all the swaps that are done along the first path
    updateSwapSteps(originalFirstPath, swapSteps)

    # Keep track of all the swaps that are done along the second path
    updateSwapSteps(somewhatOriginalSecondPath, swapSteps)

    # We add a # to swapSteps to signal the end of swaps necessary to achieve this SODDI
    swapSteps.append("#")

    return swapSteps, mapping

def swapsRequired(G_swaps, G_interactions, soddi: List[Tuple[int, int]]):
    """
    Determines the number of swaps required to implement the SODDI with the given G_swaps and G_interactions graphs
    :param G_swaps: Graph with all the swap edges possible
    :param G_interactions: Graph with all of the interaction edges
    :param soddi: Sequence of Desired Direct Interactions as a tuple of tuples
    :return: swaps: Total number of swaps required to execute the soddi given G_swaps and G_interactions
    """
    swaps = 0
    allSwapSteps = []

    # Make copies of G_swaps and G_interactions to use them as we wish without compromising the original versions
    newG_swaps, newG_interactions = copy.deepcopy(G_swaps), copy.deepcopy(G_interactions)

    for desiredInteraction in soddi:
        # Step 1: find the interaction we want to accomplish
        iSource, iTarget = desiredInteraction

        # Step 2: check if the target is source interaction neighbour already
        # If so, move onto next desired interaction
        if iTarget in newG_interactions.neighbors(iSource):
            allSwapSteps.append("Done already")
            continue

        # Step 3: find the closes pin-pen combo to iSource and iTarget
        closestActiveNodesToSource = bfsCheckingNeighbours(newG_swaps, newG_interactions, iSource, lookForPassive=False)
        closestPassiveNodesToTarget = bfsCheckingNeighbours(newG_swaps, newG_interactions, iTarget, lookForPassive=True)

        allPinNodes = closestActiveNodesToSource + closestPassiveNodesToTarget

        bestPinPenCombo, bestPinPenComboSwaps, bestPinPenComboPaths = findBestPinPenCombo(newG_swaps, newG_interactions,
                                                                                          allPinNodes,
                                                                                          iSource, iTarget)
        # Add to the total (dictatorSwaps, soldierSwaps, extraDictatorSwaps, extraSoldierSwaps)
        swaps += bestPinPenComboSwaps[0] + bestPinPenComboSwaps[1] + bestPinPenComboSwaps[2] + bestPinPenComboSwaps[3]

        # Pack all information about the combination into one tuple for compactness and readability
        bestPinPen = (bestPinPenCombo, bestPinPenComboSwaps, bestPinPenComboPaths)

        # Step 4: execute the swaps necessary to get the nodes to where they need to be (know what to relabel where)
        swapSteps, mapping = executeSwaps(newG_swaps, newG_interactions, bestPinPen)

        # Step 5: check that each swapStep makes sense
        checkSwapStepsMakesSense(desiredInteraction, swapSteps)

        # Step 6: update the list containing all of the swaps needed
        allSwapSteps += swapSteps

        # Step 7: relabel the graphs
        newG_swaps, newG_interactions = relabelGraphs(newG_swaps, newG_interactions, mapping)

        # Step 8: check that the desired interaction is happening
        checkDesiredInteractionIsAchieved(desiredInteraction, newG_interactions)

        drawStepsInGraph(newG_swaps)

    i = len([x for x in allSwapSteps if type(x) is tuple])
    if swaps != i:
        print("Total number of swaps required: " + str(swaps))
        print("List of swaps necessary: " + str(allSwapSteps))
        print("Count of swaps in list: " + str(i))
        raise Exception("The numbers don't match")
    return newG_swaps, newG_interactions, allSwapSteps


