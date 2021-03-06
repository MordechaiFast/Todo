import pytest
import json
from todo.model import DatabaseModel

@pytest.fixture
def mock_json_file(tmp_path):
    todo = [{"Description": "Write tests", "Priority": 1, "Done": False}]
    test_file = tmp_path / "todo.json"
    with test_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return test_file

test_data1 = {"description": "Go to bed", "priority": 3,
 "todo": {"Description": "Go to bed", "Priority": 3, "Done": False}}
test_data2 = {"description": "Do housework", "priority": 2,
 "todo": {"Description": "Do housework", "Priority": 2, "Done": False}}

@pytest.mark.parametrize("description, priority, expected",
 [pytest.param(test_data1["description"], test_data1["priority"], test_data1["todo"]),
  pytest.param(test_data2["description"], test_data2["priority"], test_data2["todo"])])
def test_add(mock_json_file, description, priority, expected):
    with DatabaseModel(mock_json_file) as test_db:
        test_db.add(description, priority)
    with DatabaseModel(mock_json_file) as test_db:
        # Use second 'with' to force a write to the db and a new read
        todo_list = test_db.get_todo_list()
    assert expected in todo_list
    assert len(todo_list) == 2