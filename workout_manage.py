import json
import os

workout_file = "workout_plans.json"

# Load Workout Data
def load_workouts():
    if not os.path.exists(workout_file):
        with open(workout_file, "w") as f:
            json.dump({}, f)
    with open(workout_file, "r") as f:
        return json.load(f)

# Save Workout Data
def save_workouts(data):
    with open(workout_file, "w") as f:
        json.dump(data, f, indent=4)

# Add or Update Workout
def add_or_update_workout(client_id, workout):
    data = load_workouts()
    data[str(client_id)] = {"workout": workout}
    save_workouts(data)

# View Workout
def view_workout(client_id):
    data = load_workouts()
    return data.get(str(client_id), {}).get("workout", "No Workout Plan Found")
