import json
import sys


def retrieveJSONFields(inputFileName):
    inputFileData = readJSON(inputFileName)
    try:
        inputG_swaps = [tuple(tup) for tup in inputFileData["G_swaps"]]
        inputG_interactions = [tuple(tup) for tup in inputFileData["G_interactions"]]
        soddi = [tuple(tup) for tup in inputFileData["SODDI"]]
    except KeyError:
        print("Input file must be a JSON file with the fields \"G_swaps\", \"G_interactions\" and \"SODDI\"")
        sys.exit(-1)
    return inputG_swaps, inputG_interactions, soddi


def readJSON(inputFileName):
    try:
        with open(inputFileName, "r") as read_file:
            inputFileData = json.load(read_file)
    except ValueError:
        print("Decoding input file \"%s\" has failed" % inputFileName)
        sys.exit(-1)
    return inputFileData


def isValidList(inputList):
    """
    Checks if inputList is a list of lists of 2 elements that are either ints or strings
    """
    return (isinstance(inputList, list) and all(type(sublist) is tuple for sublist in inputList)
            or all(isinstance(sublist, list) for sublist in inputList) and
            all(len(sublist) == 2 for sublist in inputList) and
            all((type(sublist[0]) is int or type(sublist[0]) is str)
                and (type(sublist[1]) is int or type(sublist[1]) is str)
                for sublist in inputList))


def checkExtractedContents(G_swaps, G_interactions, soddi):
    ok = True
    if not isValidList(G_swaps):
        print("G_swaps must be a list of lists (or tuples) of two ints or strings")
        ok = False
    if not isValidList(G_interactions):
        print("G_interactions must be a list of lists (or tuples) of two ints")
        ok = False
    if not isValidList(soddi):
        print("SODDI must be a list of lists (or tuples) of two ints")
        ok = False
    if not ok:
        sys.exit(-1)

    # Within each dictionary, there must be a key with a list which contains other keys
