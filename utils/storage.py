import json
import os

from models.user import User
from models.project import Project
from models.task import Task

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tracker_data.json")


def load_data():
    """
    Load users, projects, and tasks from the JSON file, reconstructing
    them as proper class instances. Handles a missing or malformed file
    gracefully by returning empty collections instead of crashing.
    """
    if not os.path.exists(DATA_FILE):
        return {"users": [], "projects": [], "tasks": []}

    try:
        with open(DATA_FILE, "r") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: could not read data file ({e}). Starting with empty data.")
        return {"users": [], "projects": [], "tasks": []}

    users = [_dict_to_user(u) for u in raw.get("users", [])]
    projects = [_dict_to_project(p) for p in raw.get("projects", [])]
    tasks = [_dict_to_task(t) for t in raw.get("tasks", [])]


    _sync_id_counter(User, users)
    _sync_id_counter(Project, projects)
    _sync_id_counter(Task, tasks)

    return {"users": users, "projects": projects, "tasks": tasks}


def save_data(data):
    """Save users, projects, and tasks (class instances) back to the JSON file."""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        serializable = {
            "users": [_user_to_dict(u) for u in data["users"]],
            "projects": [_project_to_dict(p) for p in data["projects"]],
            "tasks": [_task_to_dict(t) for t in data["tasks"]],
        }
        with open(DATA_FILE, "w") as f:
            json.dump(serializable, f, indent=2)
    except OSError as e:
        print(f"Error: could not save data ({e}).")


# --- conversion helpers -----------------------------------------------

def _user_to_dict(u):
    return {"id": u.id, "name": u.name, "email": u.email, "project_ids": u.project_ids}

def _dict_to_user(d):
    u = User(d["name"], d["email"])
    u.id = d["id"]
    u.project_ids = d.get("project_ids", [])
    return u

def _project_to_dict(p):
    return {
        "id": p.id, "title": p.title, "description": p.description,
        "due_date": p.due_date, "owner_id": p.owner_id, "task_ids": p.task_ids,
    }

def _dict_to_project(d):
    p = Project(d["title"], d["description"], d["due_date"], d["owner_id"])
    p.id = d["id"]
    p.task_ids = d.get("task_ids", [])
    return p

def _task_to_dict(t):
    return {
        "id": t.id, "title": t.title, "status": t.status,
        "assigned_to": t.assigned_to, "project_id": t.project_id,
    }

def _dict_to_task(d):
    t = Task(d["title"], d["status"], d["assigned_to"], d["project_id"])
    t.id = d["id"]
    return t


def _sync_id_counter(cls, instances):
    """Ensure cls._id_counter is set higher than any existing instance's id."""
    if instances:
        max_id = max(obj.id for obj in instances)
        cls._id_counter = max(cls._id_counter, max_id + 1)