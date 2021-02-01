function obtainConstrainedRandomGraph() {
    //Obtains a random graph given the constraints
    var inputStructure = {
        'numNodes': $("#numNodes").val(),
        'soddiLength': $("#soddiLength").val(),
        'swapEdgeCreationChance': $("#swapEdgeCreationChance").val(),
        'interactionEdgeCreationChance': $("#interactionEdgeCreationChance").val(),
    };
    var jsonString = JSON.stringify(inputStructure);
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "obtainRandomValidInputMethod");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.responseType = 'json';
    xhr.send(jsonString);

    xhr.onload = function () {
        if (xhr.status != 200) { // analyze HTTP status of the response
            alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
        }
        else { // show the result
            let solution = xhr.response;
            document.getElementById("submissionGSwaps").value = solution["gSwaps"];
            document.getElementById("submissionGInteractions").value = solution["gInteractions"];
            document.getElementById("submissionSODDI").value = solution["soddi"];
            updateGraphToInputs();

            //Reset stepFunctions variables
            window.currentIndex = undefined;
            window.stepsSolution = undefined;
            clearSODDItext()  //submit.js function to clear text of that section
        }
    };
}

function obtainRandomGraph() {
    //Create initial inputs
    // These are somewhat arbitrary, but they generally produce interesting situations

    // Number of nodes (minimum 2 nodes)
    document.getElementById("numNodes").value = Math.floor((Math.random()*30) + 2);

    //Number of desired interactions
    document.getElementById("soddiLength").value = Math.floor((Math.random()*30) + 1);

    //Probability of swap edges existing
    document.getElementById("swapEdgeCreationChance").value = Math.round(Math.max(Math.random(), 0.25)*1000)/1000;

    //Probability of interaction edges existing
    document.getElementById("interactionEdgeCreationChance").value = Math.round(Math.random()*(0.7 - 0.1)*1000)/1000;
    obtainConstrainedRandomGraph()
}
