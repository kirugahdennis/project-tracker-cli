import argparse

from utils.storage import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task


def cmd_add_user(args, data):
    user = User.create(args.name, args.email)
    data["users"].append(user)
    save_data(data)
    print(f"Created: {user}")


def cmd_list_users(args, data):
    if not data["users"]:
        print("No users found.")
    for u in data["users"]:
        print(u)


def cmd_add_project(args, data):
    owner = User.find_by_name(data["users"], args.user)
    if not owner:
        print(f"No user found with name: {args.user}")
        return
    project = Project.create(args.title, args.description, args.due_date, owner.id)
    data["projects"].append(project)
    owner.project_ids.append(project.id)
    save_data(data)
    print(f"Created: {project}")


def cmd_list_projects(args, data):
    projects = data["projects"]
    if args.user:
        owner = User.find_by_name(data["users"], args.user)
        if not owner:
            print(f"No user found with name: {args.user}")
            return
        projects = Project.find_by_owner(projects, owner.id)
    if not projects:
        print("No projects found.")
    for p in projects:
        print(p)


def cmd_add_task(args, data):
    project = Project.find_by_title(data["projects"], args.project)
    if not project:
        print(f"No project found with title: {args.project}")
        return

    assigned_id = None
    if args.assigned_to:
        assignee = User.find_by_name(data["users"], args.assigned_to)
        if not assignee:
            print(f"No user found with name: {args.assigned_to}")
            return
        assigned_id = assignee.id

    task = Task.create(args.title, args.status, assigned_id, project.id)
    data["tasks"].append(task)
    project.task_ids.append(task.id)
    save_data(data)
    print(f"Created: {task}")


def cmd_list_tasks(args, data):
    tasks = data["tasks"]
    if args.project:
        project = Project.find_by_title(data["projects"], args.project)
        if not project:
            print(f"No project found with title: {args.project}")
            return
        tasks = Task.find_by_project(tasks, project.id)
    if not tasks:
        print("No tasks found.")
    for t in tasks:
        print(t)


def cmd_complete_task(args, data):
    task = Task.find_by_id(data["tasks"], args.id)
    if not task:
        print(f"No task found with id: {args.id}")
        return
    task.status = "done"
    save_data(data)
    print(f"Marked complete: {task}")


def cmd_update_task(args, data):
    task = Task.find_by_id(data["tasks"], args.id)
    if not task:
        print(f"No task found with id: {args.id}")
        return
    if args.title:
        task.title = args.title
    if args.status:
        task.status = args.status
    save_data(data)
    print(f"Updated: {task}")


def build_parser():
    parser = argparse.ArgumentParser(prog="tracker", description="Project Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = subparsers.add_parser("add-user", help="Create a new user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", required=True)
    p.set_defaults(func=cmd_add_user)

    p = subparsers.add_parser("list-users", help="List all users")
    p.set_defaults(func=cmd_list_users)

    p = subparsers.add_parser("add-project", help="Create a new project for a user")
    p.add_argument("--user", required=True, help="Owner's name")
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--due-date", dest="due_date", default="")
    p.set_defaults(func=cmd_add_project)

    p = subparsers.add_parser("list-projects", help="List projects, optionally filtered by user")
    p.add_argument("--user", default=None)
    p.set_defaults(func=cmd_list_projects)

    p = subparsers.add_parser("add-task", help="Create a new task under a project")
    p.add_argument("--project", required=True, help="Project title")
    p.add_argument("--title", required=True)
    p.add_argument("--status", default="todo", choices=Task.VALID_STATUSES)
    p.add_argument("--assigned-to", dest="assigned_to", default=None, help="Assignee's name")
    p.set_defaults(func=cmd_add_task)

    p = subparsers.add_parser("list-tasks", help="List tasks, optionally filtered by project")
    p.add_argument("--project", default=None)
    p.set_defaults(func=cmd_list_tasks)

    p = subparsers.add_parser("complete-task", help="Mark a task as done")
    p.add_argument("--id", required=True, type=int)
    p.set_defaults(func=cmd_complete_task)

    p = subparsers.add_parser("update-task", help="Update a task's title or status")
    p.add_argument("--id", required=True, type=int)
    p.add_argument("--title", default=None)
    p.add_argument("--status", default=None, choices=Task.VALID_STATUSES)
    p.set_defaults(func=cmd_update_task)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    data = load_data()
    args.func(args, data)