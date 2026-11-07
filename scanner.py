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

    extension = path.suffix.lower() # Stores the lower extension (ex. .json)

    if extension == '.json':
        with open(path, 'r', encoding = 'utf-8') as f:
            return json.load(f) # Returns the list/dictionary

    elif extension == '.csv':
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [row for row in reader] # Returns the dictionary

    else:
        # Generic parser if not .csv or .json file
        with open(path, 'r', encoding='utf-8') as f:
            # Returns a list of stripped lines
            return [line.strip() for line in f if line.strip()]

print(parse_file("sample1.java"))
    