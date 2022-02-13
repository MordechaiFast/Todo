"""Stores app settings in a config file"""
from pathlib import Path
from configparser import ConfigParser

config_path = Path('config.ini')

def create_config() -> None:
    try:
        config_path.touch(exist_ok=True)
    except OSError as err:
        raise OSError('Error creating config file\n' + str(err))

def get_default_path() -> Path:
    return Path.cwd() / "to-do.json"

def save_db_path(db_path) -> None:
    if not config_path.exists():
        create_config()
    # record db location
    config_parser = ConfigParser()
    try:
        config_parser.read(config_path)
        config_parser["Open file"] = {"database": db_path}
        with open(config_path, 'w') as file:
            config_parser.write(file)
    except OSError as err:
        raise OSError('Error writing to config file\n' + str(err))

def get_db_path() -> Path:
    if not config_path.exists():
        raise IOError('Config file does not exist.'
        ' Open a to-do list to begin.')

    config_parser = ConfigParser()
    try:
        config_parser.read(config_path)
    except OSError as err:
        raise OSError('Error reading config file\n' + str(err))

    return Path(config_parser["Open file"]["database"])

def get_auto_display() -> bool:
    config_parser = ConfigParser()
    try:
        config_parser.read(config_path)
    except OSError as err:
        raise OSError('Error reading config file\n' + str(err))

    try:
        if   (config_parser["Settings"]["auto display"]) == 'True':
            return True
        elif (config_parser["Settings"]["auto display"]) == 'False':
            return False
    except KeyError:
        config_parser["Settings"] = {"auto display": False}
        return False

def set_auto_display() -> None:
    config_parser = ConfigParser()
    try:
        config_parser.read(config_path)
        config_parser["Settings"] = {"auto display": True}
        with open(config_path, 'w') as file:
            config_parser.write(file)
    except OSError as err:
        raise OSError('Error writing to config file\n' + str(err))

def set_dont_display() -> None:
    config_parser = ConfigParser()
    try:
        config_parser.read(config_path)
        config_parser["Settings"] = {"auto display": False}
        with open(config_path, 'w') as file:
            config_parser.write(file)
    except OSError as err:
        raise OSError('Error writing to config file\n' + str(err))

