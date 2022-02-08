"""Module for doing the actual reading and writing to the database"""

def init_db(db_path) -> None:
    """Create the to-do database"""
    try:
        with open(db_path, 'w') as db:
            db.write("[]")   # Empty to-do list
    except OSError as err:
        raise OSError('Error writing to to-do list\n' + str(err))

from pathlib import Path
import json
class DatabaseHandler:
    def __init__(self, db_path) -> None:
        if Path(db_path).exists():
            self._db_path = db_path
        else:
            raise IOError(f'To-do list "{db_path}" not found.')

    def read_db(self) -> list:
        try:
            with open(self._db_path) as db:
                return json.load(db)
        except json.JSONDecodeError as err:
            raise IOError("Error interpreting to-do file\n" + str(err))
        except OSError as err:
            raise OSError("Error reading to-do file\n" + str(err))

    def write_db(self, todo_list: list) -> None:
        try:
            with open(self._db_path, 'w') as db:
                json.dump(todo_list, db, indent=4)
        except OSError as err:
            raise OSError("Error writing to to-do list\n" + str(err))