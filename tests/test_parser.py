import pytest
from argparse import Namespace
from todo import __main__ as todo

def test_runs():
    args = todo.parse([])
    assert type(args) is Namespace

def test_version(capsys):
    with pytest.raises(SystemExit):
        todo.parse(['-v'])
    captured = capsys.readouterr()
    assert 'to-do' in captured.out