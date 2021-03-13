import networkx as nx


def relabelGraphs(newG_swaps, newG_interactions, mapping):
    newG_swaps = nx.relabel_nodes(newG_swaps, mapping, copy=True)
    newG_interactions = nx.relabel_nodes(newG_interactions, mapping, copy=True)
    return newG_swaps, newG_interactions
