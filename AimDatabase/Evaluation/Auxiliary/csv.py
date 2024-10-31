from csv import DictReader
from typing import Optional

# read data from a CSV file
# the first column contains keys
def read_csv(filePath: str, verbose: Optional[bool] = False):
    if verbose:
        print(f"read data from file {filePath}")
    data = {}
    with open(filePath, encoding='utf-8-sig') as csvFile:
        csvReader = DictReader(csvFile)
        for row in csvReader:
            first = True
            for key, value in row.items():
                if first:
                    config = value
                    data[config] = {}
                    first = False
                else:
                    data[config][key] = int(value)
    return data
