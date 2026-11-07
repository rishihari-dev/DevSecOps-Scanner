import csv
import json
from pathlib import Path

"""
Generic file parser 
"""

def parse_file(file_path):

    path = Path(file_path)

    # Throws error file file does not exist
    if not path.is_file():
        raise FileNotFoundError(f"No file found at {file_path}")

    lines = {}

    with open(path, 'r', encoding='utf-8') as file: #Opens file at path, reads it, python interpets, and names the file "file"
        for lineNum, text in enumerate(file, start = 1):
            lines[lineNum] = text.rstrip("\r\n")
                  #Dictionary key  = Value
                  
    return lines


print(parse_file("sample1.java"))
    