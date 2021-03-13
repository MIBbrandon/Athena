import getopt
import sys


def checkValidArgs(argv):
    inputFileName = ''
    outputFileName = ''
    opts = []  # List of strings to hold options #TODO: create uses for this
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('processingMain.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    if len(opts) == 0:
        print('processingMain.py -i <inputfile> -o <outputfile>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            # TODO: improve the information displayed with -h
            print('processingMain.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFileName = arg
        elif opt in ("-o", "--ofile"):
            outputFileName = arg
    print("Input file: " + inputFileName)
    print("Output file: " + outputFileName)
    if not inputFileName.endswith('.json'):
        print("Input file must be a .json file")
        sys.exit(-1)
    return inputFileName, outputFileName, opts
