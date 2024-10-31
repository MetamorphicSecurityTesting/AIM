    

# write data in a text file
def write_txt(data: str, filePath: str):
    with open(filePath, 'w') as file:
        file.write(data)
    print(f"data written in {filePath}")
