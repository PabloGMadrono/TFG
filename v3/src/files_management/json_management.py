import json
import os


def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

def save_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {path}")


def add_to_file(path, new_data):
    # Ensure the file exists before reading
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump([], file)  # Initialize with an empty list

    # Read the existing data
    with open(path, "r", encoding="utf-8") as file:
        try:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                existing_data = [existing_data]  # Convert to list if not already
        except json.JSONDecodeError:
            existing_data = []  # If file is empty or invalid JSON, start fresh

    # Append new data
    if isinstance(new_data, list):
        existing_data.extend(new_data)
    else:
        existing_data.append(new_data)

    # Write back to the file
    with open(path, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4)

    print(f"Data saved to {path}")


import json


def empty_json_file(filename, empty_type='dict'):
    """
    Empties a JSON file by writing an empty JSON structure to it.

    Parameters:
        filename (str): The path to the JSON file.
        empty_type (str): The type of empty structure to write.
                          Use 'dict' for {} (default) or 'list' for [].
    """
    if empty_type == 'dict':
        content = {}
    elif empty_type == 'list':
        content = []
    else:
        raise ValueError("empty_type must be 'dict' or 'list'")

    with open(filename, 'w') as f:
        json.dump(content, f, indent=4)
