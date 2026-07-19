import click
from rich.console import Console
from rich.table import Table
from .storage import load_data, save_data
from .models import User, Project, Task

console = Console()

@click.group()
def cli():
    """Project Tracker CLI"""
    pass

@cli.command()
@click.argument("username")
def add_user(username):
    data = load_data()
    user = User(username=username)
    data["users"].append(user.to_dict())
    save_data(data)
    console.print(f"[green]Created user:[/green] {username} ({user.id})")


@cli.command()
def list_users():
    data = load_data()
    table = Table(title= "User")
    table.add_column("ID")
    table.add_column("Username")
    for u in data["users"]:
        table.add_row(u["id"], u["username"])
    console.print(table)


@cli.command()
@click.argument("name")
@click.argument("owner_username")
def add_project(name, owner_username):
    data = load_data()

    owner = next((u for u in data["users"] if u["username"] == owner_username), None)
    if not owner:
        console.print(f"[red]No user found with username:[/red] {owner_username}")
        return

    project = Project(name=name, owner_id=owner["id"])
    data["projects"].append(project.to_dict())
    owner["project_ids"].append(project.id)


    save_data(data)
    console.print(f"[green]Created project:[/green] {name} ({project.id}) for user {owner_username}")


@cli.command()
@click.option("--user", default=None, help="Filter projects by username")
def list_projects(user):
    data = load_data()
    table = Table(title="Projects")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Owner")

    users_by_id = {u["id"]: u["username"] for u in data["users"]}

    for p in data["projects"]:
        owner_username = users_by_id.get(p["owner_id"], "unknown")
        if user and owner_username != user:
            continue
        table.add_row(p["id"], p["name"], owner_username)


    console.print(table)

@cli.command()
@click.argument("title")
@click.argument("project_name")
@click.option("--contributors", default="", help="Comma-separated usernames of contributors")
def add_task(title, project_name, contributors):
    data = load_data()

    project = next((p for p in data["projects"] if p["name"] == project_name), None)
    if not project:
        console.print(f"[red]No project found named:[/red] {project_name}")
        return

    contributor_ids = []
    if contributors:
        usernames = [name.strip() for name in contributors.split(",")]
        for uname in usernames:
            user = next((u for u in data["users"] if u["username"] == uname), None)
            if user:
                contributor_ids.append(user["id"])
            else:
                console.print(f"[yellow]Warning: no user found for contributor '{uname}', skipping[/yellow]")

    task = Task(title=title, project_id=project["id"], contributors=contributor_ids)
    data["tasks"].append(task.to_dict())
    project["task_ids"].append(task.id)

    save_data(data)
    console.print(f"[green]Created task:[/green] {title} ({task.id}) in project {project_name}")


@cli.command()
@click.argument("task_id")
def complete_task(task_id):
    data = load_data()
    task = next((t for t in data["tasks"] if t["id"] == task_id), None)
    if not task:
        console.print(f"[red]No task found with ID:[/red] {task_id}")
        return

    task["completed"] = True
    save_data(data)
    console.print(f"[green]Marked complete:[/green] {task['title']}")


@cli.command()
@click.option("--project", default=None, help="Filter tasks by project name")
def list_tasks(project):
    data = load_data()
    table = Table(title="Tasks")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Project")
    table.add_column("Done")
    table.add_column("Contributors")

    projects_by_id = {p["id"]: p["name"] for p in data["projects"]}
    users_by_id = {u["id"]: u["username"] for u in data["users"]}

    for t in data["tasks"]:
        project_name = projects_by_id.get(t["project_id"], "unknown")
        if project and project_name != project:
            continue
        contributor_names = ", ".join(users_by_id.get(uid, "?") for uid in t["contributors"])
        done = "✓" if t["completed"] else "✗"
        table.add_row(t["id"], t["title"], project_name, done, contributor_names)

    console.print(table)


if __name__ == "__main__":
    cli()