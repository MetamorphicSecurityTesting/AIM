# description: This script uses gathered data to generate results for the random testing (RT) baseline and merge the result with the data gathered for the adaptive random testing (ART) baseline
# usage (from root):
# gatherBaselines Results/Jenkins/jenkins_results.json Results/Jenkins/jenkins_baseline_art.json -o Results/Jenkins/jenkins_baselines.json -v
# gatherBaselines Results/Joomla/joomla_results.json Results/Joomla/joomla_baseline_art.json -o Results/Joomla/joomla_baselines.json -v

from argparse import ArgumentParser
from random import sample
from typing import List, Dict, Optional
from .Auxiliary.json import read_json, write_json

# not executed if the module is imported
if __name__ == '__main__':
    main()

def main():
    # get arguments
    args = get_args()
    resultFile = args.resultFile
    artFile = args.artFile
    output = args.output
    verbose = args.verbose
    # gather data
    results = read_json(resultFile, verbose = verbose)
    runs = results['runs']
    initial_inputset = [int(input) for input in results['costs']]
    artBaselines = read_json(artFile, verbose = verbose)
    # generate random testing (RT) results
    baselines = {}
    baselines['RT'] = get_random_testing(runs, initial_inputset, verbose = verbose)
    # gather adaptive random testing (ART) results (with sorted run and input IDs)
    runIDs = list(baselines['RT'].keys())
    for baseline in ['ART_Kmeans', 'ART_DBSCAN', 'ART_HDBSCAN']:
        baselines[baseline] = {}
        for run in runIDs:
            inputset = artBaselines[baseline][run]
            inputset.sort()
            baselines[baseline][run] = inputset
    # write baseline results
    write_json(baselines, output)
    
# parse arguments from command line interface
def get_args():
    parser = ArgumentParser(
        prog = 'GatherBaselines',
        description = 'Generate RT baselien results and gather ART baseline results')
    # mandatory arguments
    parser.add_argument('resultFile',
        metavar = 'RESULT_FILEPATH',
        help = 'path to the result file')
    parser.add_argument('artFile',
        metavar = 'ART_BASELINE_FILEPATH',
        help = 'path to the ART baseline file')
    # optional arguments
    parser.add_argument('-o', '--output',
        type = str,
        default = "baselines",
        help = 'path to the output file')
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        help = 'display execution information in the console')
    return parser.parse_args()

# For each run, the maximum number of inputs in all the minimized input sets is determined, then used to randomly select that many inputs from the initial input set.
def get_random_testing(runs: Dict[str, Dict[str, List[int]]], initial_inputset: List[int], verbose: Optional[bool] = False) -> Dict[str, List[int]]:
    # gather sizes of the obtained minimized input sets
    sizes = {}
    for config, configRuns in runs.items():
        for run, inputset in configRuns.items():
            if run not in sizes:
                sizes[run] = []
            sizes[run].append(len(inputset))
    # randomly sample the minimal input set based on sizes
    baseline = {}
    for run in sizes:
        size = max(sizes[run])
        inputset = sample(initial_inputset, size)
        inputset.sort()
        baseline[run] = inputset
    return baseline
