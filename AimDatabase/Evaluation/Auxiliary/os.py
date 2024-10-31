import os

# generate directory if it does not already exist
def checkDir(dirPath: str):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
        print(f"generate directory {dirPath}")
