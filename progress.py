import json

file='client_progress.json'

def load_progress_data():
    with open(file, 'r') as f:
        return json.load(f)

def save_progress_data(data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)