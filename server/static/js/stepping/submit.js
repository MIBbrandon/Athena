function submit() {
    //First we update the graph to the inputs, in case it is different
    updateGraphToInputs();
    //Then we remove whatever message we had before asking to first submit a soddi
    clearSODDItext();
    //Submit the SODDI inputted to obtain the solution of swap steps
    var inputStructure = {
        'gSwapsInputted': $("#submissionGSwaps").val(),
        'gInteractionsInputted': $("#submissionGInteractions").val(),
        'SODDIInputted': $("#submissionSODDI").val(),
    };
    
    var jsonString = JSON.stringify(inputStructure);
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "coreExecutionMethod");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.responseType = 'json';
    xhr.send(jsonString);

    xhr.onload = function () {
        if (xhr.status != 200) { // analyze HTTP status of the response
            alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
        }
        else { // show the result
            let solution = xhr.response;
            document.getElementById("target1").innerHTML = "Total number of swaps: " + solution["totalSwaps"];
            //document.getElementById("target1").innerHTML = JSON.stringify(solution);
            window.currentSoddiIndex = 0;
            //Turn string into array
            var preppedSODDI = $("#submissionSODDI").val().replace(/\(/g, "[").replace(/\)/g, "]"); //Write it as a string of list of lists, not tuples
            window.soddi = JSON.parse(preppedSODDI);  //Turn it from string to array
            window.currentIndex =-1;
            window.stepsSolution = solution["swapSteps"];
            //Show all the steps at the start
            document.getElementById("all_steps").innerHTML = "All steps: " + JSON.stringify(window.stepsSolution);

            window.stepNodesAttributes = solution["node_attributes"];
            window.stepEdgesAtrributes = solution["edge_attributes"];
            window.ids = solution["ids"];
        }
    };
}

function clearSODDItext() {
    document.getElementById("target1").innerHTML = "";
    document.getElementById("target2").innerHTML = "";
    document.getElementById("just_swapped").innerHTML = "";
    document.getElementById("all_steps").innerHTML = "";
    document.getElementById("next_step_button").classList.remove("w3-disabled");
}
