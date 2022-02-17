"""Module for reading and writing to a json database"""

def init_db(db_path) -> None:
    """Create the database"""
    try:
        with open(db_path, 'w') as db:
            db.write("[]")   # Empty list
    except OSError as err:
        raise OSError('Error initilizing list\n' + str(err))

from pathlib import Path
import json
class DatabaseHandler:
    """Reads and writes to the json file"""
    def __init__(self, db_path) -> None:
        if Path(db_path).exists():
            self._db_path = db_path
        else:
            raise IOError(f'List "{db_path}" not found.')

    def read_db(self) -> list:
        try:
            with open(self._db_path) as db:
                return json.load(db)
        except json.JSONDecodeError as err:
            raise IOError("Error interpreting list file\n" + str(err))
        except OSError as err:
            raise OSError("Error reading list file\n" + str(err))

    def write_db(self, todo_list: list) -> None:
        try:
            with open(self._db_path, 'w') as db:
                json.dump(todo_list, db, indent=4)
        except OSError as err:
            raise OSError("Error writing to list file\n" + str(err))