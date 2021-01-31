import math
import sys

import networkx as nx

from config import *
from critics.argsGatekeeper import checkValidArgs
from critics.inputCritics import checkingG_swaps, checkingG_interactions, checkingSODDI
from critics.jsonCritics import retrieveJSONFields, checkExtractedContents
from graphDrawing.graphDrawingMethods import drawOriginalGSwap, drawGInteractions, drawNewGSwaps
from swapping.swapFunctions import swapsRequired

script_dir = os.path.dirname(__file__)
edgelist_dir = os.path.join(script_dir, "edgelist.txt")


def obtainRandomValidInputForJS(numNodes, soddiLength, edgeCreationChance=0.4):
    G_swaps = None
    connected = False
    planar = False
    while not (connected and planar):
        G_swaps = nx.erdos_renyi_graph(numNodes, edgeCreationChance, directed=False)
        connected = nx.is_connected(G_swaps)
        planar = nx.check_planarity(G_swaps)

    G_interactions = nx.DiGraph()
    while len(G_interactions) < 1:
        for i in range(numNodes*2):
            gSwapsNodes = list(G_swaps.nodes)
            random.shuffle(gSwapsNodes)
            G_interactions.add_edge(gSwapsNodes[0], gSwapsNodes[1])


    soddi = []
    while len(soddi) < soddiLength:
        firstNum = random.randint(0, len(G_swaps.nodes)-1)
        secondNum = random.randint(0, len(G_swaps.nodes)-1)
        if firstNum != secondNum:
            soddi.append((firstNum, secondNum))

    return {"gSwaps": str(list(G_swaps.edges)), "gInteractions": str(list(G_interactions.edges)), "soddi": str(soddi)}


def randomInput():
    for i in range(rounds):
        ####################################################
        # INPUT 1: Graph representing real swappable nodes #
        ####################################################
        G_swaps = G_preSwaps = None
        connected = False
        planar = False
        print("Searching for connected graph...")
        while not (connected and planar):
            G_swaps = G_preSwaps = nx.erdos_renyi_graph(numberOfNodes, edgeCreationProbabilitySwaps, directed=False)
            connected = nx.is_connected(G_preSwaps)
            planar = nx.check_planarity(G_preSwaps)
        print("\nConnected graph found!")

        drawOriginalGSwap(G_preSwaps)

        ################################################################
        # INPUT 2: Graph representing direct interaction possibilities #
        ################################################################

        G_interactions = nx.DiGraph()
        G_interactions.add_nodes_from(range(numberOfNodes))  # G_interactions has the same nodes as G_swaps

        def createRandomGInteractions(G_interactions):
            if randomInteractionGraph:
                hasOneEdge = False
                while not hasOneEdge:
                    for x in range(random.randint(0, round(numberOfNodes * 2))):
                        if random.uniform(0, 1) < 0.5:
                            firstNode = random.randint(0, numberOfNodes - 1)
                            secondNode = random.randint(0, numberOfNodes - 1)
                            while firstNode == secondNode:  # Avoid edges from node to itself
                                firstNode = random.randint(0, numberOfNodes - 1)
                                secondNode = random.randint(0, numberOfNodes - 1)
                            if not G_interactions.has_edge(firstNode, secondNode):
                                G_interactions.add_edge(firstNode, secondNode)
                        else:
                            firstNode = random.randint(0, numberOfNodes - 1)
                            secondNode = random.randint(0, numberOfNodes - 1)
                            while firstNode == secondNode:  # Avoid edges from node to itself
                                firstNode = random.randint(0, numberOfNodes - 1)
                                secondNode = random.randint(0, numberOfNodes - 1)
                            if G_interactions.has_edge(firstNode, secondNode):
                                G_interactions.remove_edge(firstNode, secondNode)
                    hasOneEdge = G_interactions.edges

        createRandomGInteractions(G_interactions)

        print("Edges in G_swaps:")
        print([e for e in G_swaps.edges])
        print()
        print("Edges in G_interactions:")
        print([e for e in G_interactions.edges])
        print()
        print("G_interactions isolates: " + str(list(nx.isolates(G_interactions))) + "\n")

        drawGInteractions(G_interactions)

        ############################################################
        # INPUT 3: Sequence of desired direct interactions (SODDI) #
        ############################################################

        # Just a simple tuple of tuples which represents which nodes we want interaction between and in what order
        soddi = [valid_interaction for valid_interaction in
                 ((random.randrange(numberOfNodes), random.randrange(numberOfNodes)) for i in range(random.randint(*nInteractions)))
                 if valid_interaction[0] != valid_interaction[1]]

        print("SODDI: ")
        print(soddi)

        #############################################################################################
        #										END OF INPUTS 										#
        #############################################################################################

        """
		We must check that the inputs are valid. Here are the requirements:
			1) G_swaps must be an undirected connected graph of nodes labelled 0 to (nodes-1)
			2) G_interactions must have the same nodes as G_swaps, it must have at least one edge somewhere and no node may have
			   an edge pointing to itself
			3) SODDI must be a list of tuples, with each tuple containing a pair of numbers, and each number must correspond to
			   one node. No tuple may have both numbers be the same
		"""
        # Checking requirement 1
        checkingG_swaps(G_swaps)

        # Checking requirement 2
        checkingG_interactions(G_interactions)

        # Checking requirement 3
        checkingSODDI(soddi, len(list(G_swaps.nodes)))

        # Now that we have checked the inputs, we want to evaluate what is the minimum number of swaps required to achieve
        # all of the desired interactions

        # First, we want to measure how many swaps are necessary with the initial configuration
        newG_swaps, newG_interactions, swaps = swapsRequired(G_swaps, G_interactions, soddi)

        drawNewGSwaps(newG_swaps)




def coreExecution(inputG_swaps, inputG_interactions, soddi):
    # Check that the data types of the contents are valid
    checkExtractedContents(inputG_swaps, inputG_interactions, soddi)
    # Map each node to a number (index in list) which will be used to identify it afterwards
    ids = idNodes(inputG_swaps)
    adaptedG_swapsEdges, adaptedG_interactionsEdges, adaptedSODDI = adaptNodeNamesToIDs(ids, inputG_interactions,
                                                                                        inputG_swaps, soddi)
    # Create the actual graphs and check them
    G_swaps = nx.Graph()
    G_swaps.add_nodes_from(range(len(ids)))
    G_swaps.add_edges_from(adaptedG_swapsEdges)
    checkingG_swaps(G_swaps)
    G_interactions = nx.DiGraph()
    G_interactions.add_nodes_from(range(len(ids)))
    G_interactions.add_edges_from(adaptedG_interactionsEdges)
    checkingG_interactions(G_interactions)
    # Check SODDI
    checkingSODDI(adaptedSODDI, len(ids))
    # From this point on, we are ready to manipulate the graphs as we wish
    newG_swaps, newG_interactions, allSwapSteps = swapsRequired(G_swaps, G_interactions, adaptedSODDI)
    # Rename every node in allSwapSteps to the original names
    renamedAllSwapSteps = revertAllSwapStepsNames(allSwapSteps, ids)
    totalSwaps = len([x for x in renamedAllSwapSteps if type(x) is tuple])
    print("SODDI: " + str(soddi))
    print("Swap steps: " + str(renamedAllSwapSteps))
    print("Total number of swaps required: " + str(totalSwaps))
    return totalSwaps, renamedAllSwapSteps, ids


def processNodesAndEdgesForJSVisual(inputG_swaps, inputG_interactions, soddi, node_colour="#9CC3D5FF", node_size=50,
			swap_edge_colour="#0a3780", swap_edge_width=4, interaction_edge_colour="#FFC400", interaction_edge_width=4,
			overlap_edge_colour="#ff00ae", overlap_edge_width=4):
    """
    Returns lists with dictionaries with information regarding the nodes and edges
    """

    # Check that the data types of the contents are valid
    checkExtractedContents(inputG_swaps, inputG_interactions, soddi)
    # Map each node to a number (index in list) which will be used to identify it afterwards
    ids = idNodes(inputG_swaps)

    #WARNING remember that went making edges, you want to join the IDs and not the labels. For the IDs, use ids.index()

    #Lists of dictionaries to be returned
    nodes = []
    edges = []

    # We want the nodes to be placed in a circular path
    increment = (2 * math.pi) / len(ids)
    radius = 200 / increment
    pos = 0
    for node in ids:
        nodes.append({"color": node_colour,
                      "id": ids.index(node),
                      "label": str(node),
                      "title": "Label: " + str(node) + "\nID: " + str(ids.index(node)),
                      "shape": "circle",  "size": node_size,
                      "scaling": {
                          "label": {
                              "enabled": True,
                              "min": node_size,
                              "max": node_size+1,
                          }
                      },
                      "font": {
                          "size": node_size,
                          "color": "#0063B2FF",
                      },
                      "x": radius * math.cos(pos), "y": -radius * math.sin(pos)})
        pos += increment

    for edge in inputG_swaps:  # Swap edges go both ways
        edges.append({"arrows": "to", "color": swap_edge_colour, "from": ids.index(edge[0]), "to": ids.index(edge[1]),
                      "width": swap_edge_width})
        edges.append({"arrows": "to", "color": swap_edge_colour, "from": ids.index(edge[1]), "to": ids.index(edge[0]),
                      "width": swap_edge_width})

    for edge in inputG_interactions:
        # Special colour if it is an edge that overlaps with a swap edge
        if (edge[0], edge[1]) in inputG_swaps or (edge[1], edge[0]) in inputG_swaps or [edge[0], edge[1]] in inputG_swaps or [edge[1], edge[0]] in inputG_swaps:
            edges.append({"arrows": "to", "color": overlap_edge_colour, "from": ids.index(edge[0]), "to": ids.index(edge[1]), "width": overlap_edge_width, "arrowStrikethrough": False})
        else:
            edges.append({"arrows": "to", "color": interaction_edge_colour, "from": ids.index(edge[0]), "to": ids.index(edge[1]), "width": interaction_edge_width, "arrowStrikethrough": False})

    return {"nodes": nodes, "edges": edges}

def revertAllSwapStepsNames(allSwapSteps, ids):
    renamedAllSwapSteps = []
    for tup in allSwapSteps:
        if type(tup) is tuple:
            renamedAllSwapSteps.append((ids[tup[0]], ids[tup[1]]))
        else:
            renamedAllSwapSteps.append(tup)
    return renamedAllSwapSteps


def adaptNodeNamesToIDs(ids, inputG_swaps, inputG_interactions, soddi):
    try:
        print("IDs: " + str(ids))
        adaptedG_swapsEdges = [[ids.index(x), ids.index(y)] for x, y in inputG_swaps]
        adaptedG_interactionsEdges = [[ids.index(x), ids.index(y)] for x, y in inputG_interactions]
        adaptedSODDI = [(ids.index(x), ids.index(y)) for x, y in soddi]
    except ValueError:
        print("Nodes in G_interactions and SODDI must be in G_swaps")
        sys.exit(-1)
    return adaptedG_interactionsEdges, adaptedG_swapsEdges, adaptedSODDI


def idNodes(inputG_swaps):
    ids = []
    for edge in inputG_swaps:  # We use inputG_swaps to get all the nodes since it must be a connected graph
        if not edge[0] in ids:
            ids.append(edge[0])
        if not edge[1] in ids:
            ids.append(edge[1])
    return ids

def main(argv):
    # Check that the arguments input in the shell are valid
    inputFileName, outputFileName, opts = checkValidArgs(argv)

    # Check that these files are in the correct format (JSON, G_swaps, G_interactions, SODDI, etc.)
    inputG_swaps, inputG_interactions, soddi = retrieveJSONFields(inputFileName)

    coreExecution(inputG_interactions, inputG_swaps, soddi)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        randomInput()
    else:
        main(sys.argv[1:])
########################################################################################################################
########################################################################################################################
