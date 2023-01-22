"""Model for 'todo'"""
from .database import DatabaseHandler

class DatabaseModel:
    """Contains the work functions and connects them to the to-do file"""

    def __init__(self, db_path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    
    def __enter__(self):
        """Reads the database upon entry to context"""
        self._todo_list: list[dict] = self._db_handler.read_db()
        return self

    def __exit__(self, *args) -> None:
        """Records the to-do list to the database upon exit"""
        self._db_handler.write_db(self._todo_list)

    def add(self, description: str, priority: int) -> None:
        """Add a new to-do to the database."""
        self._todo_list.append({
            "Description": description,
            "Priority": priority,
            "Done": False,
        })

    def change_priority(self, id: int, priority: int) -> None:
        """Changes the proprity of a to-do to the given value"""
        self._todo_list[id]['Priority'] = priority

    def set_done(self, id: int) -> None:
        """Set a to-do as done"""
        self._todo_list[id]['Done'] = True

    def set_not_done(self, id: int) -> None:
        """Set a to-do as not done"""
        self._todo_list[id]['Done'] = False

    def move_up(self, id: int) -> None:
        """Moves an item up one in the list.
        Call multiple times to move up multiple places"""
        self._todo_list[id], self._todo_list[id - 1] \
        = self._todo_list[id - 1], self._todo_list[id]

    def move_down(self, id: int) -> None:
        """Moves an item down one in the list.
        Call multiple times to move up multiple places"""
        self._todo_list[id], self._todo_list[id + 1] \
        = self._todo_list[id + 1], self._todo_list[id]

    def remove_todo(self, id: int) -> None:
        """Remove a to-do from the list"""
        del self._todo_list[id]

    def get_todo(self, id: int) -> dict:
        """Returns a single to-do with id"""
        return self._todo_list[id]

    def get_todo_list(self) -> list:
        """Return the current to-do list"""
        return self._todo_list