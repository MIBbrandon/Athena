function updateGraphToInputs() {
    var inputStructure = {
        'gSwapsInputted': $("#submissionGSwaps").val(),
        'gInteractionsInputted': $("#submissionGInteractions").val(),
        'SODDIInputted': $("#submissionSODDI").val(),
    };
    var jsonString = JSON.stringify(inputStructure);
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "processNodesAndEdgesForJSVisualMethod");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.responseType = 'json';
    xhr.send(jsonString);

    xhr.onload = function () {
        if (xhr.status != 200) { // analyze HTTP status of the response
            alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
        }
        else { // show the result
            let solution = xhr.response;
            // Update nodes and edges to be the values obtained through the response
            nodes = new vis.DataSet(solution['nodes']);
            edges = new vis.DataSet(solution['edges']);
            drawGraph();

            //Reset stepFunctions variables
            currentSoddiIndex = undefined;
            soddi = undefined;
            currentIndex = undefined;  //Records on what swap step we are on to know whether we can step back or step forward
            stepsSolution = undefined;  //Holds list with steps
            stepNodesAttributes = undefined;
            stepEdgesAtrributes = undefined;
            ids = undefined;
            clearSODDItext();
        }
    };
}

function centerGraph() {
    network.fit();
}
