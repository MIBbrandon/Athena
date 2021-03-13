import math

from pyvis.network import Network
import json

file = "json_files/test3.json"


def getData():
	with open(file, "r") as json_file:
		data = json.load(json_file)
		return data


def mapData(graph_edges_swaps, graph_edges_interactions, node_colour="#03DAC6", node_size=30,
			swap_edge_colour="#0a3780", swap_edge_width=6, interaction_edge_colour="#FFC400", interaction_edge_width=6,
			overlap_edge_colour="#ff00ae", overlap_edge_width=6):
	g = Network(directed=True, height="100%", width="100%", bgcolor="#222222", font_color="white")
	g.toggle_physics(False)
	g.show_buttons()
	allNodes = []
	for edge in graph_edges_swaps:
		if edge[0] not in allNodes:
			allNodes.append(edge[0])
		if edge[1] not in allNodes:
			allNodes.append(edge[1])

	addElementsToGraph(allNodes, g, graph_edges_interactions, graph_edges_swaps, interaction_edge_colour,
					   interaction_edge_width, node_colour, node_size, overlap_edge_colour, overlap_edge_width,
					   swap_edge_colour, swap_edge_width)

	g.show("graphs.html")


def addElementsToGraph(allNodes, g, graph_edges_interactions, graph_edges_swaps, interaction_edge_colour,
					   interaction_edge_width, node_colour, node_size, overlap_edge_colour, overlap_edge_width,
					   swap_edge_colour, swap_edge_width):
	# Add the nodes to the visualization
	# We want the nodes to be placed in a circular path
	increment = (2 * math.pi) / len(allNodes)
	radius = 200 / increment
	pos = 0
	for node in allNodes:
		g.add_node(node, color=node_colour, size=node_size, x=radius * math.cos(pos), y=-radius * math.sin(pos))
		pos += increment
	# NOTE: swap edges are added first so that they appear underneath the interaction edges
	# Add the swap edges
	for edge in graph_edges_swaps:
		g.add_edge(*edge, color=swap_edge_colour, width=swap_edge_width)
		g.add_edge(edge[1], edge[0], color=swap_edge_colour, width=swap_edge_width)
	# Add the interaction edges
	for edge in graph_edges_interactions:
		# Special colour if it is an edge that overlaps with a swap edge
		if edge in graph_edges_swaps or (edge[1], edge[0]) in graph_edges_swaps:
			g.add_edge(*edge, color=overlap_edge_colour, width=overlap_edge_width)
		else:
			g.add_edge(*edge, color=interaction_edge_colour, width=interaction_edge_width)


all_data = getData()
mapData(all_data["G_swaps"], all_data["G_interactions"])
