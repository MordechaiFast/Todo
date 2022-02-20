from argparse import Namespace
import pytest
import json
from todo import __main__ as todo
from todo.model import DatabaseModel

def test_runs():
    args = todo.parse([])
    assert type(args) is Namespace

def test_version(capsys):
    with pytest.raises(SystemExit):
        todo.parse(['-v'])
    captured = capsys.readouterr()
    assert 'to-do' in captured.out

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
        todo_list = test_db.get_todo_list()
        assert expected in todo_list
    with DatabaseModel(mock_json_file) as test_db:
        todo_list = test_db.get_todo_list()
        assert len(todo_list) == 2

@pytest.fixture
def mock_nonexistant_file(tmp_path):
    db_file = tmp_path / "todo.json"
    return db_file

def test_opening_nonexistant_file(mock_nonexistant_file):
    try:
        with DatabaseModel(mock_nonexistant_file): pass
    except IOError: pass

@pytest.fixture
def mock_empty_file(tmp_path):
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as file:
        file.write("")
    return db_file

def test_oppening_empty_file(mock_empty_file):
    try:
        with DatabaseModel(mock_empty_file): pass
    except IOError: pass