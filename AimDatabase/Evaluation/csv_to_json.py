# description: convert a CSV file into a JSON file
# usage: csvToJson Results/Jenkins/aim_execution_time.csv -v
# or: csvToJson Results/Jenkins/aim_execution_time.csv -o Results/Jenkins/aim_execution_time.json -v

from argparse import ArgumentParser
from .Auxiliary.csv import read_csv
from .Auxiliary.json import write_json

# not executed if the module is imported
if __name__ == '__main__':
    main()

def main():
    # get arguments
    args = get_args()
    csvFile = args.csvFile
    jsonFile = args.jsonFile
    verbose = args.verbose
    # extract data
    data = read_csv(csvFile, verbose = verbose)
    if jsonFile is None:
        jsonFile = csvFile.split(".csv")[0] + ".json"
    write_json(data, jsonFile)

# parse arguments from command line interface
def get_args():
    parser = ArgumentParser(
        prog = 'csvToJson',
        description = 'convert CSV file to JSON file')
    # mandatory arguments
    parser.add_argument('csvFile',
        metavar = 'CSV_FILEPATH',
        help = 'path to CSV file')
    # optional arguments
    parser.add_argument('-o', '--jsonFile',
        type = str,
        default = None,
        help = 'path to the output file')
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        help = 'display execution information in the console')
    return parser.parse_args()
