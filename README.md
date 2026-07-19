
# Project Tracker CLI

A command-line project management tool for tracking users, projects, and tasks. Built with Python, using object-oriented design (inheritance, properties, class methods) and JSON file persistence.

## Features

- Create and list users
- Create and list projects, linked to their owning user (one-to-many)
- Create, list, complete, and update tasks, linked to their project (one-to-many) and assignee
- Data persists locally between runs via JSON
- Input validation via Python properties (e.g. task status must be one of `todo`, `in_progress`, `done`)

## Project Structure
project-tracker-cli/
├── main.py # CLI entry point (argparse)
├── models/
│ ├── person.py # Base class: name, email
│ ├── user.py # User(Person) — owns projects
│ ├── project.py # Project — belongs to a user, has tasks
│ └── task.py # Task — belongs to a project, assigned to a user
├── utils/
│ └── storage.py # JSON load/save, object<->dict conversion
├── data/
│ └── tracker_data.json # Local data store (auto-created)
├── tests/
│ └── ... # Unit tests
└── requirements.txt

## AUTHOR

Denis Kiarie.
