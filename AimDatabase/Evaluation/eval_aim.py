# description: This script uses result data to evaluate the AIM approach
# usage (from root): evalAim Results/Joomla/joomla_results.json -b Results/Joomla/joomla_baselines.json -a Results/Joomla/joomla_analysis.json -d Results/Joomla/joomla_duels.json -v

from argparse import ArgumentParser
from typing import List, Dict, Optional
from .Auxiliary.json import read_json, write_json
from .Auxiliary.analysis import analyze_results
from .Auxiliary.metrics import get_duels

# not executed if the module is imported
if __name__ == '__main__':
    main()

def main():
    # get arguments
    args = get_args()
    resultFile = args.resultFile
    baselineFile = args.baselineFile
    analysisFile = args.analysisFile
    duelsFile = args.duelsFile
    verbose = args.verbose
    # extract data
    data = read_json(resultFile, verbose = verbose)
    vulnerabilities = data['vulnerabilities']
    inputCosts = data['costs']
    runs = data['runs']
    exeTime = data['aimExecutionTime']
    # check runs and (if any) add baselines
    runIDs = check_runs(runs)
    if baselineFile is not None:
        baselines = read_json(baselineFile, verbose = verbose)
        for baseline, baselineRuns in baselines.items():
            if baseline in runs:
                raise ValueError("A baseline name should not be a configuration name.")
            runs[baseline] = baselineRuns
            # baselines are inexpensive to compute
            if baseline in exeTime:
                raise ValueError("A baseline name should not be a configuration name.")
            exeTime[baseline] = {}
            for run in runIDs:
                exeTime[baseline][run] = 0
    # total number of vulnerabilities to trigger
    totalVulns = len(vulnerabilities)*len(runIDs)
    # analysis
    analysis = analyze_results(vulnerabilities, inputCosts, runs, exeTime, totalVulns, verbose = verbose)
    write_json(analysis, analysisFile)
    # duels for configuration with full coverage
    configurations = filter_configurations(analysis, totalVulns, verbose = verbose)
    if len(configurations) > 0:
        duels = get_duels(analysis, configurations, verbose = verbose)
        write_json(duels, duelsFile)

# parse arguments from command line interface
def get_args():
    parser = ArgumentParser(
        prog = 'EvalAim',
        description = 'Evaluate AIM')
    # mandatory arguments
    parser.add_argument('resultFile',
        metavar = 'RESULT_FILEPATH',
        help = 'path to result file')
    # optional arguments
    parser.add_argument('-b', '--baselineFile',
        type = str,
        default = None,
        help = 'path to the baseline file')
    parser.add_argument('-a', '--analysisFile',
        type = str,
        default = "eval_aim_analysis",
        help = 'path to the analysis file')
    parser.add_argument('-d', '--duelsFile',
        type = str,
        default = "eval_aim_duels",
        help = 'path to the duels file')
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        help = 'display execution information in the console')
    return parser.parse_args()

# check there the run file conbtains at least one configuration
# and that for each configuration the number of runs is the same
# then return that number
def check_runs(runs: Dict[str, Dict[str, List[int]]]) -> List[str]:
    if len(runs) == 0:
        raise ValueError("There should be at least one configuration in the run file.")
    runIDs_previous = None
    for config in runs:
        runIDs = list(runs[config].keys())
        if 'total' in runIDs:
            raise ValueError("'total' is a reserved key.")
        if runIDs_previous is not None and runIDs != runIDs_previous:
            raise ValueError("Each configuration should have the same run IDs.")
        runIDs_previous = runIDs
    return runIDs

# determine the list of the configurations with full vulnerability coverage
def filter_configurations(analysis: Dict[str, Dict[str, Dict[str, int]]], totalVulns: int, verbose: Optional[bool] = False) -> List[str]:
    configurations = [config for config in analysis if analysis[config]['vulns']['total'] == totalVulns]
    if verbose:
        print(f"configurations with full coverage:")
        if len(configurations) == 0:
            print("none")
        for config in configurations:
            print(config)
    return configurations
