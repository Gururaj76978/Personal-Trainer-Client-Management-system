import json

file='phone.json'

# Function to load phone data from the JSON file
def load_phone_data():
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save phone data to the JSON file
def save_phone_data(data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)