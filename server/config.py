import os
import random
script_dir = os.path.dirname(__file__)
edgelist_dir = os.path.join(script_dir, "edgelist.txt")

# We will use a randomly generated graph, but we want to be able to receive input from a JSON later on, for example

# seed = 8  # For being able to reproduce results later on
# random.seed(seed)

numberOfNodes = 30  # Number of nodes we want in our G_swaps and G_interactions

# Determine the range for the number of interactions
nInteractions = (3, 5)

# Number of times to run random inputs
rounds = 1

edgeCreationProbabilitySwaps = 0.05
edgeCreationProbabilityInteractions = 0.01  # Not in effect at the moment

randomInteractionGraph = True
directedRandomInteractionGraph = True

interactionsOnSeparateWindow = True

showOriginalG_swap = False
showG_interactions = False
show_only_edges_G_interactions = False
if interactionsOnSeparateWindow:
    show_only_edges_G_interactions = False
showSteps = False
showNewG_swap = False

node_color_original_swaps = "#f5b505"
node_color_new_swaps = "#66d160"
node_color_step_swaps = "#03f0fc"
edge_color_swaps = "#00bfe0"
edge_width_swaps = 1

node_color_interactions = "#ff00dd"
edge_color_interactions = "#ed02c6"
edge_width_interactions = 1

