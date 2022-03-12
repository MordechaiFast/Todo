import pytest
from todo.model import DatabaseModel

@pytest.fixture
def mock_nonexistant_file(tmp_path):
    db_file = tmp_path / "todo.json"
    return db_file

def test_opening_nonexistant_file(mock_nonexistant_file):
    with pytest.raises(IOError) as err:
        with DatabaseModel(mock_nonexistant_file): pass
    assert 'not found' in str(err)

@pytest.fixture
def mock_empty_file(tmp_path):
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as file:
        file.write("")
    return db_file

def test_opening_empty_file(mock_empty_file):
    with pytest.raises(IOError) as err:
        with DatabaseModel(mock_empty_file): pass
    assert 'interpreting' in str(err)