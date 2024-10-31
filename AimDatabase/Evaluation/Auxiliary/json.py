from json import load, dump
from typing import Optional

# read data from a JSON file
def read_json(filePath: str, verbose: Optional[bool] = False):
    if verbose:
        print(f"read data from file {filePath}")
    with open(filePath, 'r') as file:
        data = load(file)
    return data

# write data in a JSON file
def write_json(data: dict, filePath: str):
    with open(filePath, 'w') as file:
        dump(data, file, indent = 4)
    print(f"data written in {filePath}")
