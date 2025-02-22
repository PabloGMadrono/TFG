import json



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
