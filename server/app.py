import ast
import json
import os

from processingMain import coreExecution, processNodesAndEdgesForJSVisual, obtainRandomValidInputForJS

from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
from flask_jsglue import JSGlue

app = Flask(__name__)
jsglue = JSGlue(app)

@app.route('/', methods=["GET", "POST"])
def indexPage():
    return render_template("index.html")

@app.route('/athena', methods=["GET", "POST"])
def athenaPage():
    return render_template("athena.html")

@app.route('/favicon.ico', methods=["GET"])
def getFavicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route("/coreExecutionMethod", methods=["GET", "POST"])
def coreExecutionMethod():
    if request.method == "POST":
        print("Determining the number of swaps required...")
        jsondata = request.get_json()
        print(jsondata)
        try:
            inputG_swaps = ast.literal_eval(jsondata['gSwapsInputted'])
            inputG_interactions = ast.literal_eval(jsondata['gInteractionsInputted'])
            soddi = ast.literal_eval(jsondata['SODDIInputted'])
        except:
            print("Invalid input received from client")
            return {"ERROR": "INVALID INPUT"}

        totalSwaps, swapSteps, ids = coreExecution(inputG_swaps, inputG_interactions, soddi)
        solution = {
            "totalSwaps": totalSwaps,
            "swapSteps": swapSteps,
            "ids": ids,
            "edge_attributes": {
                "edge_colour_std": "#ffffff",
                "edge_width_std": 10,
                "edge_colour_done": "#1df505",
                "edge_width_done": 10,
            },
            "node_attributes": {
                "node_colour_from_std": "#ffa600",
                "node_colour_to_std": "#f5c07a",
                "node_size_from_std": 30,
                "node_size_to_std": 30,
                "node_colour_from_done": "#43f707",
                "node_colour_to_done": "#43f707"
            }
        }
        jsonSolution = json.dumps(solution)
        print(jsonSolution)
        return jsonSolution

@app.route("/obtainRandomValidInputMethod", methods=["POST"])
def obtainRandomValidInputMethod():
    if request.method == "POST":
        print("Obtaining a random valid input...")
        jsondata = request.get_json()
        print(jsondata)
        try:
            numNodes = int(jsondata['numNodes'])
            print(numNodes)
            soddiLength = int(jsondata['soddiLength'])
            print(soddiLength)
            swapEdgeCreationChance = float(jsondata['swapEdgeCreationChance'])
            print(swapEdgeCreationChance)
            interactionEdgeCreationChance = float(jsondata['interactionEdgeCreationChance'])
            print(interactionEdgeCreationChance)
        except:
            print("Invalid input received from client")
            return {"ERROR": "INVALID INPUT"}
        return obtainRandomValidInputForJS(numNodes, soddiLength, swapEdgeCreationChance, interactionEdgeCreationChance)
    return {"ERROR": "INVALID METHOD"}

@app.route("/processNodesAndEdgesForJSVisualMethod", methods=["POST"])
def processNodesAndEdgesForJSVisualMethod():
    if request.method == "POST":
        print("Preparing data for visualization...")
        jsondata = request.get_json()
        print(jsondata)
        try:
            inputG_swaps = ast.literal_eval(jsondata['gSwapsInputted'])
            inputG_interactions = ast.literal_eval(jsondata['gInteractionsInputted'])
            soddi = ast.literal_eval(jsondata['SODDIInputted'])
        except SyntaxError:
            return "INVALID INPUT"

        return processNodesAndEdgesForJSVisual(inputG_swaps, inputG_interactions, soddi)
    return "INVALID METHOD"


if __name__ == "__main__":
    app.run(debug=True)
