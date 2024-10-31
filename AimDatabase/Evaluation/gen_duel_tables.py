# description: This script uses duel values to generate LaTeX tables
# usage (from root):
# genDuelTables Results/Jenkins/jenkins_duels.json -s jenkins -c Results/Both/colors.json -d Results/Jenkins/Tables -v
# genDuelTables Results/Joomla/joomla_duels.json -s joomla -c Results/Both/colors.json -d Results/Joomla/Tables -v

from argparse import ArgumentParser
from .Auxiliary.json import read_json
from .Auxiliary.os import checkDir
from .Auxiliary.tables import get_table_duels
from .Auxiliary.txt import write_txt

# not executed if the module is imported
if __name__ == '__main__':
    main()

def main():
    # get arguments
    args = get_args()
    duelFile = args.duelFile
    system = args.system
    colorPath = args.colorPath
    tableDir = args.tableDir
    verbose = args.verbose
    # gather data
    duels = read_json(duelFile, verbose = verbose)
    if colorPath is None:
        colors = None
    else:
        colors = read_json(colorPath, verbose = verbose)
    # generate and write duel tables
    checkDir(tableDir)
    for aspect in duels:
        data = duels[aspect]
        table = get_table_duels(data, aspect, system = system, colors = colors, verbose = verbose)
        filePath = tableDir + "/" + system + "_duels_" + aspect + ".tex"
        write_txt(table, filePath)

# parse arguments from command line interface
def get_args():
    parser = ArgumentParser(
        prog = 'GenDuelTables',
        description = 'Generate LaTeX duel tables')
    # mandatory arguments
    parser.add_argument('duelFile',
        metavar = 'DUEL_FILEPATH',
        help = 'path to the duel file')
    # optional arguments
    parser.add_argument('-s', '--system',
        type = str,
        default = "",
        help = 'comment to identify the considered system')
    parser.add_argument('-c', '--colorPath',
        type = str,
        default = None,
        help = 'path to the colors file')
    parser.add_argument('-d', '--tableDir',
        type = str,
        default = ".",
        help = 'path to the table directory')
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        help = 'display execution information in the console')
    return parser.parse_args()
