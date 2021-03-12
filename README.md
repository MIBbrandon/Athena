# Athena
Qubit routing graph visualization

INSERT AN EXAMPLE GRAPH HERE

An important part of NISQ devices is the execution of algorithms as fast as possible before decoherence catches up to our qubits, which then result in undesireable errors. One of the current limitations on the execution speed of algorithms is the hardware.

These quantum algorithms rely on interesting operations like CNOT, which is a two-qubit gate that, put simply, "flips" a target qubit depending on the value of the control qubit. For these CNOTs and other multi-qubit gates to be applied on the hardware (_in the real world_), the physical systems that represent our logical qubits must usually be near one another and have a direct connection that is implemented in said hardware. Otherwise, there is no way to apply these gates, unless we perform what is called a SWAP operation, which swaps the states that two qubits have with one another. These SWAP gate applications are costly in time and even in coherence of a quantum state.

With few qubits, this usually isn't much of a problem, but as the number of qubits grows, the number of swaps required to implement many algorithms increases exponentially since the chance that a qubit has to directly interact with another qubit which is further away topologically increases, as well as the sheer amount of qubits that require direct interactions.

This gives rise to the need to reduce the number of swaps as much as possible, which ends up being a sort of iterative travelling-salesman problem. This obviously becomes a tedious task to manually organize all qubits and the swap paths that they'll take, especially when different quantum hardware have different topologies for the allowed swaps and direct interactions between physical qubits.

There are already great tools to organize these qubits and their paths to a certain degree, such as Cambridge's [tket](https://cqcl.github.io/pytket/build/html/index.html). However, it can be hard to properly appreciate the complexity of the problem a tool like this solves unless it is visualized, and that is what project Athena is for: a way to visualize all the swapping and interactions done.


## How to use
First of all, you'll want to download the repository as a zip file or clone it. Then you must run app.py, which uses the Flask framework so that it can all be interactive in your browser.


Then, once the server is running and you've accessed the page, you should see something like this:

INSERT IMAGE OF LANDING PAGE HERE

On the left side, there is a graph with nodes that spread out in a circumference. If you hover the mouse over the nodes, you'll see that each one has a label (which is the number that you can see without hovering the mouse) and an ID (which identifies each node uniquely, obviously). Each one of these nodes has directed edges leading to other nodes. There are three kinds of edges, whose meanings can be found in the legend.

INSERT IMAGE OF LEGEND

The blue edges represent the swappable qubits, the yellow edges represent available direct interactions, and the pink edges represent interaction edges that overlap with a swap edge, for better visibility. 

These edges mean that whenever two qubits are connected by a blue edge, they can swap states with one another (the label represents the state). Whenever they are connected by a yellow edge, the active node (the one without the head of the arrow aiming at it) can directly interact the the passive node (I'm sure you can guess which node we're talking about), which represents the availability of applying a CNOT gate from the active node to the passive one, for example. And finally, if they are connected by a pink edge, there is an overlap between being able to swap both nodes and establishing an interaction (notice that the pink arrow's head isn't necessarily aiming at both involved nodes).

### Configuration panel
On the right side (or at the bottom on mobile), there is a configuration panel with varios sections.

#### Graph
In the graph configuration section, there are two text fields: "Swap Edges" and "Interaction Edges". They contain lists of tuples, which represent the swap and interaction edges of the graph respectively. If you want, you can add or remove an edge in the "Swap Edges" field at will (the nodes are added as the swap edges require them to exist), but adding an interaction in the "Interaction Edges" must obviously involve existing edges. When you click "Update", the graph will represent your changes, and clicking on "Center" will center the graph in case you dragged around the screen accidentally and got lost.

#### Randomizer
This section randomizes both the graph and the Sequence Of Desired Direct Interactions (SODDI). If you want to create a whole new graph, click on "Randomize graph". This will change the graph and the SODDI (since it must request interactions for nodes that exist). If you want to create a random graph, but want a specific number of nodes, a different length of the SODDI or even alter the probability that an edge will be made between two nodes (swap or interaction), then you can do so by entering the desired values and clicking on "Random graph with constraints".

#### SODDI stepping
In the Sequence Of Desired Direct Interactions (SODDI) section, there is one text field: "Sequence Of Desired Direct Interactions". This is the order in which you want two qubits (well, more specifically two states/labels) to interact. Again, the involved nodes must exist in the graph. In the text field, you can specify the interactions you want to happen, and the order in which they happen. You can click on "Submit/Reset" in order to calculate what the best course of action for swapping and interacting. Once you've received a result, you can click on "Next step" to start going through each step.

You will notice that the graph now has two nodes that are bigger in size, and that there is an edge with a different colour between these two nodes. If you look at the legend, it will tell you that the latest swap that happened is represented by a white edge, and that the latest interaction is represented by a green edge.

If it is a swap, you will see the node with the label we are interested in moving being of a size greater than that of the one that was just displaced. If it is an interaction, both edges will be equally big to show that the desired direct interaction is taking place.

You can continue clicking on "Next Step" until all steps have been completed. You can also see some more information in this section specifying the total number of swaps required for the SODDI to be satisfied, as well as the latest action that has occured, and even a list of values which shows the swaps that will take place (the pairs of numbers are swaps), the interactions taking place after swapping (represented by "#") or without requiring swapping (represented by "Done already").

And that should be all! If you have any problems, I'll respond to any issue raised as soon as possible.

Play around and have fun!
