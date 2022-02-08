#!/usr/bin/env python
"""Router module for 'todo'.
CLI with argparse.
Logging with logger.
Configuration handling with configparser.
Database storage with json library."""

from config import get_default_path
default_db_path = get_default_path()

from argparse import ArgumentParser
parser = ArgumentParser(description="To-do app. Loosly based upon rptodo.",
 allow_abbrev=True, usage="%(prog)s [options]")
parser.add_argument('-v', action='version', version='Command line to-do 1.2')
file_group = parser.add_mutually_exclusive_group(required=False)
file_group.add_argument('--new', nargs='?', const=default_db_path,
 metavar='PATH',
 help=f"Creates a new to-do list at PATH. By default {default_db_path}")
file_group.add_argument('--open', nargs='+', metavar='PATH',
 help="Open an existing to-do list at PATH")
add_move_revome = parser.add_mutually_exclusive_group(required=False)
add_move_revome.add_argument('--add', nargs='+',
 metavar='DESCRIPTION', dest='description',
 help="Add a new to-do with a DESCRIPTION (multiple words)")
parser.add_argument('-priority', type=int, default=2, choices=[1, 2, 3],
 help="of to-do being added")
add_move_revome.add_argument('--move-up', nargs=2, type=int,
 metavar=('ID', 'PLACES'),
 help="Moves item ID up by a number of PLACES")
add_move_revome.add_argument('--move-down', nargs=2, type=int,
 metavar=('ID', 'PLACES'),
 help="Moves item ID down by a number of PLACES")
parser.add_argument('--check', type=int, metavar='ID',
 help="Marks item ID as done. If 0 is entered, marks ALL as done")
parser.add_argument('--uncheck', type=int, metavar='ID',
 help="Marks item ID as not done. If 0 is entered, marks ALL as not done")
parser.add_argument('--change', nargs = 2, type=int,
 metavar=('ID', 'PRIORITY'),
 help="Changes the priority of ID to PRIORITY")
add_move_revome.add_argument('--remove', type=int, metavar='ID',
 help="Remove a to-do using its ID number")
parser.add_argument('-confirm', action='store_true',
 help="Confirm removal on command-line")
parser.add_argument('--list', action='store_true',
 help="List all to-do's")
parser.add_argument('-auto', action='store_true',
 help="Toggles if the list is automatically displayed")
args = parser.parse_args()

import logging
log = logging.Logger('todo')
terminal_logging = logging.StreamHandler()
terminal_logging.setLevel(logging.INFO)
terminal_logging.setFormatter(logging.Formatter('{message}', style='{'))
log.addHandler(terminal_logging)

from config import (save_db_path, get_db_path,
 get_auto_display, set_auto_display, set_dont_display)
from database import init_db
from controler import Controler
from view import display
try:    # All file reads and writes could create errors, so be ready to record them
    if args.new:
        db_path = args.new
        save_db_path(db_path)
        log.info(f"Current to-do file set to: {db_path}")
        init_db(db_path)
        log.info("New to-do list initilized")

    if args.open:
        db_path = " ".join(args.open)
        save_db_path(db_path)
        log.info(f"Current to-do file set to: {db_path}")

    with Controler(get_db_path) as controler:
    # Contains the work functions and connects them to the to-do file

        if args.description:    # add to-do item
            # Capitalize first word
            args.description[0] = args.description[0].capitalize()
            # String the words of the description together
            description = " ".join(args.description)
            controler.add(description, args.priority)
            log.info(f'to-do: "{description}" was added'
            f" with priority: {args.priority}")

        if args.move_up:
            start = args.move_up[0] - 1
            places = args.move_up[1]
            todo = controler.get_todo(start)
            for index in range(start, start - places, -1):
                controler.move_up(index)
            log.info(f"""to-do #{args.move_up[0]}: "{todo['Description']}" """
            f"moved up {places} places")

        if args.move_down:
            start = args.move_down[0] - 1
            places = args.move_down[1]
            todo = controler.get_todo(start)
            for index in range(start, start + places):
                controler.move_down(index)
            log.info(f"""to-do #{args.move_down[0]}: "{todo['Description']}" """
            f"moved down {places} places")

        if args.check is not None:    # complete to-do item, or all of them
            if args.check == 0:
                for index in range(len(controler.get_todo_list())):
                    controler.set_done(index)
                log.info("All to-do items marked as done!")
            else:
                id = args.check - 1
                todo = controler.get_todo(id)
                controler.set_done(id)
                log.info(f"""to-do #{args.check}: "{todo['Description']}" """
                    "marked as done!")

        if args.uncheck is not None:  # un-complete to-do item, or all of them
            if args.uncheck == 0:
                for index in range(len(controler.get_todo_list())):
                    controler.set_not_done(index)
                log.info("All to-do items marked as not done!")
            else:
                id = args.uncheck - 1
                todo = controler.get_todo(id)
                controler.set_not_done(id)
                log.info(f"""to-do #{args.uncheck}: "{todo['Description']}" """
                    "marked as not done!")

        if args.change:     # change priority
            id = args.change[0]-1
            priority = args.change[1]
            todo = controler.get_todo(id)
            controler.change_priority(id, priority)
            log.info(f"""to-do #{args.change[0]} "{todo['Description']}" """
            f"set to priority {priority}")


        if args.remove:
            id = args.remove - 1
            todo = controler.get_todo(id)
            if args.confirm == False:
                confirimation = input("Really remove to-do"
                f""" "{todo['Description']}"? [y/N]""")
                
            if args.confirm == True or confirimation.upper() == 'Y':
                controler.remove_todo(id)
                log.info(f"""to-do #{args.remove}: "{todo['Description']}" """
                    "removed from the list!")
            else:
                print("Removal canceled")

        if args.auto:
            if get_auto_display():
                set_dont_display()
            else:
                set_auto_display()
            log.info(f"Automatic listing set to {get_auto_display()}")

        if args.list or get_auto_display():
            todo_list = controler.get_todo_list()
            display(todo_list)

except IndexError:
    log.error("No such to-do item")
except OSError as err:
    log.error(err)