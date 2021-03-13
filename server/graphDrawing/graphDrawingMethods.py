import networkx as nx
from matplotlib import pyplot as plt

from config import *


def drawOriginalGSwap(G_preSwaps):
	# Draw graph showing which nodes can directly swap with the other
	if showOriginalG_swap:
		plt.figure()
		plt.draw()
		nx.draw_circular(G_preSwaps, with_labels=True, node_color=node_color_original_swaps,
						 edge_color=edge_color_swaps, width=edge_width_swaps)
		plt.pause(0.5)
		plt.show(block=False)


def drawGInteractions(G_interactions):
	# Draw graph showing nodes that can directly interact with one another
	if showG_interactions:
		if interactionsOnSeparateWindow:
			plt.figure()
		plt.draw()
		plt.pause(0.5)
		if show_only_edges_G_interactions:
			nx.draw_circular(G_interactions, with_labels=True,
							 node_color=node_color_interactions, edge_color=edge_color_interactions,
							 width=edge_width_interactions, node_size=0)
		else:
			nx.draw_circular(G_interactions, with_labels=True,
							 node_color=node_color_interactions, edge_color=edge_color_interactions,
							 width=edge_width_interactions)
		plt.show(block=False)


def drawStepsInGraph(G_swaps):
	if showSteps:
		plt.figure()
		nx.draw_circular(G_swaps, with_labels=True, node_color=node_color_step_swaps,
						 edge_color=edge_color_swaps)
		plt.show(block=False)


def drawNewGSwaps(G_swaps):
	if showNewG_swap:
		plt.figure()
		plt.draw()
		plt.pause(0.5)
		nx.draw_circular(G_swaps, with_labels=True, node_color=node_color_new_swaps, edge_color=edge_color_swaps,
						 width=edge_width_swaps)
		plt.show(block=True)
