//Setting up the important data for making the steps animation
var currentSoddiIndex;
var soddi;
var currentIndex;  //Records on what swap step we are on to know whether we can step back or step forward
var stepsSolution;  //Holds list with steps
var stepNodesAttributes;
var stepEdgesAtrributes;
var ids;

//TODO: complete these functions to draw the new arrows and nodes to represent the swaps step by step
function stepForwards() {
    if (currentIndex == undefined) {
        document.getElementById("target2").innerHTML = "Please submit soddi first!";
    }
    else if(!(Array.isArray(soddi) && soddi.length)) {
        document.getElementById("target2").innerHTML = "No swap steps are required";
    }
    else if (currentIndex == (stepsSolution.length - 1)) {
        document.getElementById("target2").innerHTML = "All steps have been completed";
    }
    else {
        //Remove whatever extra nodes and edges that have been added previously for visual effects
        try {
            window.edges.remove([99999]);
            window.edges.remove([99998]);
        }
        catch(err) {}

        //Make last nodes return to normal size
        window.nodes.update([{id: lastN1, font: {size: 50}}, {id: lastN2, font: {size: 50}}]);


        //Clear some text
        document.getElementById("target2").innerHTML = "";
        //Before moving to the next step, if this step marks the end of a desired interaction, move onto the next one
        try {  //In a try-catch so that when index is out of bounds (like when submitting, for example), it just skips this section
            if(!("#").localeCompare(stepsSolution[currentIndex]) || !("Done already").localeCompare(stepsSolution[currentIndex])) {
                currentSoddiIndex++;
            }
        }catch(err){}; 
        currentIndex++;  //Move onto the next step
        if(currentIndex == (stepsSolution.length - 1)) {
            document.getElementById("target2").innerHTML = "All steps have been completed";
            document.getElementById("next_step_button").classList.add("w3-disabled");
        }

        //Nodes of interest
        let n1 = ids.indexOf(soddi[currentSoddiIndex][0]);
        let n2 = ids.indexOf(soddi[currentSoddiIndex][1]);

        if(!("#").localeCompare(stepsSolution[currentIndex])) {
            //End of desired interaction reached, so show that this interaction has been completed
            edge1ToAdd = {"id":99999, "arrows": "to", "color": stepEdgesAtrributes["edge_colour_done"], 
            "from": n1, "to": n2, 
            "width": stepEdgesAtrributes["edge_width_done"], arrowStrikethrough: false};

            //Make nodes bigger for visibility
            window.lastN1 = n1;
            window.lastN2 = n2;
            window.nodes.update([{id: n1, font: {size: 100}}, {id: n2, font: {size: 100}}]);

            window.edges.update([edge1ToAdd]);
            window.network.redraw();
            window.network.selectNodes([n1, n2]);
            document.getElementById("just_swapped").innerHTML = "Latest action: allowed interaction " + soddi[currentSoddiIndex][0] + "->" + soddi[currentSoddiIndex][1];
        }
        else if (!("Done already").localeCompare(stepsSolution[currentIndex])) {
            //Interaction is already established, so show it
            edge1ToAdd = {"id":99999, "arrows": "to", "color": stepEdgesAtrributes["edge_colour_done"], 
            "from": n1, "to": n2, 
            "width": stepEdgesAtrributes["edge_width_done"], arrowStrikethrough: false};

            //Make nodes bigger for visibility
            window.lastN1 = n1;
            window.lastN2 = n2;
            window.nodes.update([{id: n1, font: {size: 100}}, {id: n2, font: {size: 100}}]);

            window.edges.update([edge1ToAdd]);
            window.network.redraw();
            window.network.selectNodes([n1, n2]);
            document.getElementById("just_swapped").innerHTML = "Latest action: allowed interaction " + soddi[currentSoddiIndex][0] + "->" + soddi[currentSoddiIndex][1];
        }
        else {
            //Start the process of showing the next elements
            //First draw arrow between the two nodes being swapped
            firstNodeLabel = stepsSolution[currentIndex][0];
            secondNodeLabel = stepsSolution[currentIndex][1];
            firstNode = ids.indexOf(firstNodeLabel);
            secondNode = ids.indexOf(secondNodeLabel);

            //Make nodes bigger for visibility
            window.lastN1 = firstNode;
            window.lastN2 = secondNode;
            window.nodes.update([{id: firstNode, font: {size: 100}}, {id: secondNode, font: {size: 100}}]);

            edge1ToAdd = {"id":99999, "arrows": "to", "color": stepEdgesAtrributes["edge_colour_std"], 
            "from": firstNode, "to": secondNode, 
            "width": stepEdgesAtrributes["edge_width_std"], arrowStrikethrough: false};
            edge2ToAdd = {"id":99998, "arrows": "to", "color": stepEdgesAtrributes["edge_colour_std"], 
            "from": secondNode, "to": firstNode, 
            "width": stepEdgesAtrributes["edge_width_std"], arrowStrikethrough: false};
            
            window.edges.update([edge1ToAdd, edge2ToAdd]);

            //Then switch the nodes (remembering to update ids as well)
            nodesUpdate = [{id:firstNode, label:secondNodeLabel.toString()}, {id:secondNode, label:firstNodeLabel.toString()}]
            window.nodes.update(nodesUpdate);
            window.network.redraw();
            window.network.selectNodes([firstNode, secondNode]);

            //Updating ids accordingly
            ids[firstNode] = secondNodeLabel;
            ids[secondNode] = firstNodeLabel;

            //Display what was just swapped
            document.getElementById("just_swapped").innerHTML = "Latest action: swapped (" + firstNodeLabel + ", " + secondNodeLabel + ")"; 
        }
    }
    
}

// TODO: make this actually work
function stepBackwards() {
    
    if (currentIndex == undefined) {
        document.getElementById("target2").innerHTML = "Please submit soddi first!";
    } 
    else if(!(Array.isArray(soddi) && soddi.length)) {
        document.getElementById("target2").innerHTML = "No swap steps are required";
    }
    else if (currentIndex == 0) {
        document.getElementById("target2").innerHTML = "There is no step before this one";
    }
    else {
        // Remove whatever extra nodes and edges that have been added previously for visual effects
        try {
            window.edges.remove([99999]);
            window.edges.remove([99998]);
        }
        catch(err) {}
        document.getElementById("target2").innerHTML = "";
        //We need to revert whatever effect has happened in the current step
        //First, we remove whatever was just placed
        //This is already taken care of previously
        //Then we need to revert whatever swap just took place (if any did)
        //Since the action of switching undoes itself, we can just do that
        if(("#").localeCompare(stepsSolution[currentIndex]) && ("Done already").localeCompare(stepsSolution[currentIndex])) {
            //Start the process of showing the next elements
            //First draw arrow between the two nodes being swapped
            firstNodeLabel = stepsSolution[currentIndex][0];
            secondNodeLabel = stepsSolution[currentIndex][1];
            firstNode = ids.indexOf(firstNodeLabel);
            secondNode = ids.indexOf(secondNodeLabel);

            //We do not draw the edges. We don't care to show this swap

            //edge1ToAdd = {"id":99999, "arrows": "to", "color": stepEdgesAtrributes["edge_colour_std"], 
            //"from": firstNode, "to": secondNode, 
            //"width": stepEdgesAtrributes["edge_width_std"], arrowStrikethrough: false};
            //edge2ToAdd = {"id":99998, "arrows": "to", "color": stepEdgesAtrributes["edge_colour_std"], 
            //"from": secondNode, "to": firstNode, 
            //"width": stepEdgesAtrributes["edge_width_std"], arrowStrikethrough: false};
            //window.edges.update([edge1ToAdd, edge2ToAdd]);

            //Then switch the nodes (remembering to update ids as well)
            nodesUpdate = [{id:firstNode, label:secondNodeLabel.toString()}, {id:secondNode, label:firstNodeLabel.toString()}]
            window.nodes.update(nodesUpdate);
            window.network.redraw();
            window.network.selectNodes([firstNode, secondNode]);

            //Updating ids accordingly
            ids[firstNode] = secondNodeLabel;
            ids[secondNode] = firstNodeLabel;
        }
        //We repeat for the step before
        if(("#").localeCompare(stepsSolution[currentIndex-1]) && ("Done already").localeCompare(stepsSolution[currentIndex-1])) {
            //Start the process of showing the next elements
            //First draw arrow between the two nodes being swapped
            firstNodeLabel = stepsSolution[currentIndex-1][0];
            secondNodeLabel = stepsSolution[currentIndex-1][1];
            firstNode = ids.indexOf(firstNodeLabel);
            secondNode = ids.indexOf(secondNodeLabel);

            //We do not draw the edges. We don't care to show this swap

            //edge1ToAdd = {"id":99999, "arrows": "to", "color": stepEdgesAtrributes["edge_colour_std"], 
            //"from": firstNode, "to": secondNode, 
            //"width": stepEdgesAtrributes["edge_width_std"], arrowStrikethrough: false};
            //edge2ToAdd = {"id":99998, "arrows": "to", "color": stepEdgesAtrributes["edge_colour_std"], 
            //"from": secondNode, "to": firstNode, 
            //"width": stepEdgesAtrributes["edge_width_std"], arrowStrikethrough: false};
            //window.edges.update([edge1ToAdd, edge2ToAdd]);

            //Then switch the nodes (remembering to update ids as well)
            nodesUpdate = [{id:firstNode, label:secondNodeLabel.toString()}, {id:secondNode, label:firstNodeLabel.toString()}]
            window.nodes.update(nodesUpdate);
            window.network.redraw();
            window.network.selectNodes([firstNode, secondNode]);

            //Updating ids accordingly
            ids[firstNode] = secondNodeLabel;
            ids[secondNode] = firstNodeLabel;
        }

        //All we need to do now is recreate what happened in the previous step
        //To do so, we can go back two steps with the indexes and then use stepForwards()
        //To go back two steps, we need to reduce currentIndex by 2, and then analyze how we should reduce currentSoddiIndex

        if(!("#").localeCompare(stepsSolution[currentIndex]) || !("Done already").localeCompare(stepsSolution[currentIndex])) {
            currentSoddiIndex--;
        }
        if(!("#").localeCompare(stepsSolution[currentIndex-1]) || !("Done already").localeCompare(stepsSolution[currentIndex-1])) {
            currentSoddiIndex--;
        }
        currentIndex -= 2;

        //Now we can go forward again
        stepForwards();

    }
}