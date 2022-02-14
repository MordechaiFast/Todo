"""Model for 'todo'"""
from database import DatabaseHandler

class DatabaseModel:
    def __init__(self, db_path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    
    def __enter__(self):
        self._todo_list = self._db_handler.read_db()
        return self

    def __exit__(self, *args):
        self._db_handler.write_db(self._todo_list)

    def add(self, description: list, priority: int) -> None:
        """Add a new to-do to the database."""
        todo = {
            "Description": description,
            "Priority": priority,
            "Done": False,
        }
        self._todo_list.append(todo)

    def change_priority(self, id: int, priority: int) -> None:
        """Changes the proprity of a to-do to the given value"""
        todo = self._todo_list[id]
        todo['Priority'] = priority
        # Pass-by-reference, so no need to put back into the list

    def set_done(self, id: int) -> None:
        """Set a to-do as done"""
        todo = self._todo_list[id]
        todo['Done'] = True

    def set_not_done(self, id: int) -> None:
        """Set a to-do as not done"""
        todo = self._todo_list[id]
        todo['Done'] = False

    def move_up(self, id: int) -> None:
        """Moves an item up one in the list.
        Call multiple times to move up multiple places"""
        this_todo = self._todo_list[id]
        self._todo_list[id] = self._todo_list[id - 1]
        self._todo_list[id - 1] = this_todo

    def move_down(self, id: int) -> None:
        """Moves an item down one in the list.
        Call multiple times to move up multiple places"""
        this_todo = self._todo_list[id]
        self._todo_list[id] = self._todo_list[id + 1]
        self._todo_list[id + 1] = this_todo

    def remove_todo(self, id: int) -> None:
        """Remove a to-do from the list"""
        self._todo_list.pop(id)

    def get_todo(self, id: int) -> dict:
        """Returns a single to-do with id"""
        return self._todo_list[id]

    def get_todo_list(self) -> list:
        """Return the current to-do list"""
        return self._todo_list