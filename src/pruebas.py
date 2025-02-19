import numpy as np
import json
import pandas as pd

# Load CSV file and handle potential encoding issues
file_path = "data/mapaTFG.csv"  # Replace with your actual file path
data = pd.read_csv(file_path, delimiter=",", dtype=int, encoding="utf-8-sig", header=None).to_numpy()


# Iterate over the matrix to find product locations (value = 2)
for y, row in enumerate(data):  # y is the row index
    print(y, row, len(row))