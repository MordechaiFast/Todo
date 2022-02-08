"""I/O for to-do app using Typer"""

from typer import *
from typing import List, Optional

app = Typer()

from pathlib import Path
default_db_path = Path.cwd() / "todo.json"
from config import save_db_path, get_db_path
from database import init_db

@app.command()
def new(path: str = Option(
 str(default_db_path),
 prompt="Path of new to-do list?")):
    """Creates a new to-do list at PATH."""
    try:
        save_db_path(path)
        secho(f"Current to-do file set to: {path}", fg=colors.GREEN)
        init_db(path)
        secho(f"New to-do list initilized", fg=colors.GREEN)
    except OSError as err:
        secho(err, fg=colors.RED)
        raise Exit(1)

@app.command()
def open(path: str = Option(
 str(get_db_path()),
 prompt="Path of to-do list to open?")):
    """Open an existing to-do list at PATH"""
    try:
        save_db_path(path)
    except OSError as err:
        secho(err, fg=colors.RED)
        raise Exit(1)
    else:
        secho(f"Current to-do file set to: {path}", fg=colors.GREEN)

from controler import Controler
@app.command()
def add(description: List[str], priority: int = Option(2)):
    """Add a new to-do with a DESCRIPTION."""
    description = " ".join(description)
    try:
        controler = Controler()
        controler.add(description, priority)
    except OSError as err:
        secho(err, fg=colors.RED)
    else:
        secho(f"""to-do: "{description}" was added"""
            f" with priority: {priority}", fg=colors.GREEN)

@app.command(name='list')
def display():
    """Displays the to-do list"""
    try:
        controler = Controler()
        todo_list = controler.get_todo_list()
    except OSError as err:
        secho(err, fg=colors.RED)
    else:
        if len(todo_list) == 0:
            secho("There are no tasks in the to-do list yet", fg=colors.RED)
            raise Exit()
        secho("\nto-do list:\n", fg=colors.BLUE, bold=True)
        columns = (
            "ID.  ",
            "| Priority  ",
            "| Done  ",
            "| Description  ",
        )
        headers = "".join(columns)
        secho(headers, fg=colors.BLUE, bold=True)
        secho("-" * len(headers), fg=colors.BLUE)
        for id, todo in enumerate(todo_list, 1):
            desc, priority, done = todo.values()
            secho(
                f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
                f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
                f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
                f"| {desc}",
                fg=colors.BLUE,
            )
        secho("-" * len(headers) + "\n", fg=colors.BLUE)

app()