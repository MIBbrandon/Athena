function obtainConstrainedRandomGraph() {
    //Obtains a random graph given the constraints
    var inputStructure = {
        'numNodes': $("#numNodes").val(),
        'soddiLength': $("#soddiLength").val(),
        'edgeCreationChance': $("#edgeCreationChance").val(),
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
            document.getElementById("target1").innerHTML = "";
            document.getElementById("target2").innerHTML = "";
        }
    };
}

function obtainRandomGraph() {
    //Create initial inputs
    document.getElementById("numNodes").value = Math.floor((Math.random()*30) + 2); // Number of nodes (minimum 2 nodes)
    document.getElementById("soddiLength").value = Math.floor((Math.random()*30) + 1); //Number of desired interactions
    document.getElementById("edgeCreationChance").value = Math.max(Math.random(), 0.25); //Probability of edges existing
    obtainConstrainedRandomGraph()
}
