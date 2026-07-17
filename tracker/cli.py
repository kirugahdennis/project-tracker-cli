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


if __name__ == "__main__":
    cli()