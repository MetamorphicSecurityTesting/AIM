# description: This script gathers input IDs from run results and write them in a JSON file.
# usage (from root): gatherData Results/Jenkins/vulnerabilities.json Results/Jenkins/costs.json ../../Research/Testing/Runs Results/Jenkins/aim_execution_time.json -o Results/Jenkins/jenkins_results.json -v

from argparse import ArgumentParser
from typing import List, Dict, Optional
from .Auxiliary.json import read_json, write_json

# not executed if the module is imported
if __name__ == '__main__':
    main()

def main():
    # get arguments
    args = get_args()
    vulnFile = args.vulnFile
    costFile = args.costFile
    runsDir = args.runsDir
    timeFile = args.timeFile
    output = args.output
    verbose = args.verbose
    # parameters
    distances = ['Lev', 'Bag']
    algorithms = ['Kmeans', 'DBSCAN', 'HDBSCAN']
    runIds = [str(i) for i in range(1, 51)]# runs 1 to 50
    # extract data
    dataVuln = read_json(vulnFile, verbose = verbose)
    dataCost = read_json(costFile, verbose = verbose)
    dataRuns = get_dataRuns(runsDir, runIds, distances, algorithms, verbose = verbose)
    dataTime = read_json(timeFile, verbose = verbose)
    # write data
    data = {
        'vulnerabilities': dataVuln,
        'costs': dataCost,
        'runs': dataRuns,
        'aimExecutionTime': dataTime
    }
    write_json(data, output)

# parse arguments from command line interface
def get_args():
    parser = ArgumentParser(
        prog = 'GatherResults',
        description = 'Gather AIM runs and input data')
    # mandatory arguments
    parser.add_argument('vulnFile',
        metavar = 'COST_FILEPATH',
        help = 'path to costs file')
    parser.add_argument('costFile',
        metavar = 'COST_FILEPATH',
        help = 'path to costs file')
    parser.add_argument('runsDir',
        metavar = 'RUN_DIRPATH',
        help = 'path to Runs directory')
    parser.add_argument('timeFile',
        metavar = 'TIME_FILEPATH',
        help = 'path to execution time file')
    # optional arguments
    parser.add_argument('-o', '--output',
        type = str,
        default = "gather_data_results",
        help = 'path to the output file')
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        help = 'display execution information in the console')
    return parser.parse_args()

# gather input IDs from all configurations and runs
def get_dataRuns(runsDir: str, runIds: List[str], distances: List[str], algorithms: List[str], verbose: Optional[bool] = False) -> Dict[str, Dict[str, List[int]]]:
    data = {}
    if verbose:
        print(f"read data from directory {runsDir} for configurations:")
    for dist in distances:
        for outputAlgo in algorithms:
            for actionAlgo in algorithms:
                configuration = dist + '_' + outputAlgo + '_' + actionAlgo
                if verbose:
                    print(f"   - {configuration}")
                data[configuration] = {}
                for run in runIds:
                    filePath = runsDir + "/Run" + run + "/" + dist + "_" + outputAlgo + "/" + actionAlgo + "/inputset_minimized_IDs.txt"
                    inputIDs = get_inputIDs(filePath)
                    data[configuration][run] = inputIDs
    return data

# read inputset_minimized_IDs.txt and extract input IDs as a list of integers
def get_inputIDs(filePath: str) -> List[int]:
    try:
        with open(filePath, 'r') as file:
            content = file.read()
            # split the content string to get individual values
            values = content.split(',')
        # remove empty strings and convert the rest to integers
        inputIDs = [int(val) for val in values if val]
        return inputIDs
    except FileNotFoundError:
        print(f"The file {filePath} was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
