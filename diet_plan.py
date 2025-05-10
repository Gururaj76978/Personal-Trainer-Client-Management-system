import json
import os

# JSON File Path
diet_file = 'client_diet.json'

# Create JSON file if not exists
if not os.path.exists(diet_file):
    with open(diet_file, 'w') as f:
        json.dump({}, f)

def load_diet_data():
    with open(diet_file, 'r') as f:
        return json.load(f)

def save_diet_data(data):
    with open(diet_file, 'w') as f:
        json.dump(data, f, indent=4)

def add_or_update_diet(client_name, meal_time, food_items):
    data = load_diet_data()
    if client_name not in data:
        data[client_name] = {}
    data[client_name][meal_time] = food_items
    save_diet_data(data)

def view_diet_for_client(client_name):
    data = load_diet_data()
    return data.get(client_name, {})
