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
    for u in data["user"]:
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


if __name__ == "__main__":
    cli()