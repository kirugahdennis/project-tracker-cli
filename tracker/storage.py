import json 
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tracker_data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return{"users": [], "projects": [], "tasks": [] }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)