# description: This script gathers costs from multiple runs of multiples algorithms, then generate the corresponding LaTeX table.
# usage (from root):
# compareAlgos Results/Jenkins/jenkins_algos.json -b 600 -s jenkins -d Results/Jenkins/Tables -v
# compareAlgos Results/Joomla/joomla_algos.json -b 600 -s joomla -d Results/Joomla/Tables -v
# compareAlgos Results/Joomla/joomla_algos.json -b 400 -s joomla -d Results/Joomla/Tables -v

from argparse import ArgumentParser
from .Auxiliary.json import read_json
from .Auxiliary.os import checkDir
from .Auxiliary.metrics import get_algo_duels
from .Auxiliary.tables import get_table_algos
from .Auxiliary.txt import write_txt

def main():
    # get arguments
    args = get_args()
    resultPath = args.resultPath
    timeBudget = str(args.budget)
    system = args.system
    tableDir = args.tableDir
    verbose = args.verbose
    # compare algorithms
    results = read_json(resultPath, verbose = verbose)
    data = {}
    for algo in results:
        data[algo] = results[algo][timeBudget]
    duels = get_algo_duels(data, verbose = verbose)
    # generate table
    checkDir(tableDir)
    table = get_table_algos(duels, timeBudget, system = system, verbose = verbose)
    filePath = tableDir + "/" + system + "_duels_genetic_" + timeBudget + ".tex"
    write_txt(table, filePath)

# parse arguments from command line interface
def get_args():
    parser = ArgumentParser(
        prog = 'CompareAlgorithms',
        description = 'Gather algorithm results and generate corresponding LaTeX table')
    # mandatory arguments
    parser.add_argument('resultPath',
        metavar = 'RESULT_FILEPATH',
        help = 'path to the results file')
    # optional arguments
    parser.add_argument('-b', '--budget',
        # type = int,# can be int or float
        default = 600,
        help = 'considered time budget for the comparison')
    parser.add_argument('-s', '--system',
        type = str,
        default = "",
        help = 'comment to identify the considered system')
    parser.add_argument('-d', '--tableDir',
        type = str,
        default = ".",
        help = 'path to the table directory')
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        help = 'display execution information in the console')
    return parser.parse_args()

# not executed if the module is imported
if __name__ == '__main__':
    main()
