# description: This script uses duel values to generate LaTeX tables
# usage (from root): genVulnTable Results/Jenkins/jenkins_analysis.json jenkins Results/Joomla/joomla_analysis.json joomla -o Results/Both/vulnerability_coverage.tex -c Results/Both/colors.json -v

from argparse import ArgumentParser
from .Auxiliary.json import read_json, write_json
from .Auxiliary.tables import get_table_vulns
from .Auxiliary.txt import write_txt

# not executed if the module is imported
if __name__ == '__main__':
    main()

def main():
    # get arguments
    args = get_args()
    analysisFile1 = args.firstAnalysisFile
    analysisFile2 = args.secondAnalysisFile
    system1 = args.firstSystem
    system2 = args.secondSystem
    outputPath = args.outputPath
    colorPath = args.colorPath
    verbose = args.verbose
    # gather data
    analysis1 = read_json(analysisFile1, verbose = verbose)
    analysis2 = read_json(analysisFile2, verbose = verbose)
    # generate and write table for vulnerability coverage
    table, colors = get_table_vulns(analysis1, analysis2, system1, system2, verbose = verbose)
    write_txt(table, outputPath)
    write_json(colors, colorPath)

# parse arguments from command line interface
def get_args():
    parser = ArgumentParser(
        prog = 'GenVulnTable',
        description = 'Generate LaTeX table for vulnerability coverage')
    # mandatory arguments
    parser.add_argument('firstAnalysisFile',
        metavar = 'FIRST_ANALYSIS_FILEPATH',
        help = 'path to the first analysis file')
    parser.add_argument('firstSystem',
        metavar = 'FIRST_SYSTEM',
        help = 'comment identifying the first system')
    parser.add_argument('secondAnalysisFile',
        metavar = 'SECOND_ANALYSIS_FILEPATH',
        help = 'path to the second analysis file')
    parser.add_argument('secondSystem',
        metavar = 'SECOND_SYSTEM',
        help = 'comment identifying the second system')
    # optional arguments
    parser.add_argument('-o', '--outputPath',
        type = str,
        default = "gen_vuln_table_output",
        help = 'path to the output file')
    parser.add_argument('-c', '--colorPath',
        type = str,
        default = "gen_vuln_table_colors",
        help = 'path to the colors file')
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        help = 'display execution information in the console')
    return parser.parse_args()
