import networkx as nx

from typing import Final, List

CONST_SODDINodesOutOfRange = "One or more values inside the tuples are not within range of the nodes in G_swaps"

CONST_SODDIInvalidSelfInteractions = "Interactions of one node to itself are not valid"

CONST_SODDIbadFormat = "SODDI must be a list of lists of two integers (List[List[int, int]])"

CONST_tooFewNodesMSG: Final = "The number of nodes must be at least 2"
CONST_gSwapsMustBeUndirectedMSG: Final = "G_swaps cannot be a directed graph"
CONST_gSwapsMustBeConnectedMSG: Final = "G_swaps must be a connected graph"

CONST_nodesAreNotCorrectIntsMSG: Final = "Nodes are not integers from 0 to "

CONST_gInteractionsIsUndirectedMSG: Final = "G_interactions must be a directed graph"
CONST_gInteractionsLoopsMSG: Final = "G_interactions cannot have nodes with edges pointing towards themselves (loops)"
CONST_gInteractionsHasNoEdgeMSG = "G_interactions must have at least one edge"


def checkingG_swaps(G_swaps):
    if len(list(G_swaps.nodes)) < 2:
        raise ValueError(CONST_tooFewNodesMSG)
    if nx.is_directed(G_swaps):
        raise Exception(CONST_gSwapsMustBeUndirectedMSG)
    if not nx.is_connected(G_swaps):
        raise Exception(CONST_gSwapsMustBeConnectedMSG)
    nodesInG_swaps = list(G_swaps.nodes)
    for i in range(len(nodesInG_swaps)):
        if i != nodesInG_swaps[i]:
            raise ValueError(CONST_nodesAreNotCorrectIntsMSG + (str(len(nodesInG_swaps))))


def checkingG_interactions(G_interactions):
    if not nx.is_directed(G_interactions):
        raise Exception(CONST_gInteractionsIsUndirectedMSG)
    nodesInG_interactions = list(G_interactions)
    for i in range(len(nodesInG_interactions)):
        if G_interactions.has_edge(nodesInG_interactions[i], nodesInG_interactions[i]):
            raise Exception(CONST_gInteractionsLoopsMSG)
        if i != nodesInG_interactions[i]:
            raise ValueError(CONST_nodesAreNotCorrectIntsMSG + (str(len(nodesInG_interactions))))
    if len(list(G_interactions.edges)) == 0:
        raise Exception(CONST_gInteractionsHasNoEdgeMSG)


def checkingSODDI(soddi, nodesInGswap):
    if type(soddi) is not list:
        raise Exception(CONST_SODDIbadFormat)
    for desiredInteraction in soddi:
        if (type(desiredInteraction) is not tuple or type(desiredInteraction[0]) is not int or
                type(desiredInteraction[1]) is not int):
            raise Exception(CONST_SODDIbadFormat)
    for desiredInteraction in soddi:
        if desiredInteraction[0] == desiredInteraction[1]:
            raise Exception(CONST_SODDIInvalidSelfInteractions)
        if not (0 <= desiredInteraction[0] < nodesInGswap and 0 <= desiredInteraction[1] < nodesInGswap):
            raise Exception(CONST_SODDINodesOutOfRange)
