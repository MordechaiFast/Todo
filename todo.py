#!/usr/bin/env python
"""Controler module for 'todo'.
CLI with argparse.
Logging with logger.
Configuration handling with configparser.
Database storage with json library."""

from config import get_default_path
default_db_path = get_default_path()

from argparse import ArgumentParser
parser = ArgumentParser(description="To-do app. Loosly based upon rptodo.",
 usage="%(prog)s [options]")
parser.add_argument('-v', action='version', version='Command line to-do 1.2')

file_group_parent = parser.add_argument_group('File operations')
file_group= file_group_parent.add_mutually_exclusive_group(required=False)
file_group.add_argument('-n', '--new', nargs='?', const=default_db_path,
 metavar='PATH',
 help=f"Creates a new to-do list at PATH. By default {default_db_path}")
file_group.add_argument('-o', '--open', nargs='+', metavar='PATH',
 help="Open an existing to-do list at PATH")

new_item = parser.add_argument_group('Add to-do')
new_item.add_argument('-a', '--add', nargs='+', action='append',
 metavar='DESCRIPTION', dest='description',
 help="Add a new to-do with a DESCRIPTION (multiple words)")
""" new_item.add_argument('-i', '-priority', dest='priority',
 type=int, default=2, choices=[1, 2, 3],
 help="of to-do being added") """

edit_item = parser.add_argument_group('Edit item position or status')
edit_item.add_argument('-u', '--move-up', nargs=2, type=int,
 metavar=('ID', 'PLACES'),
 help="Moves item ID up by a number of PLACES")
edit_item.add_argument('-d', '--move-down', nargs=2, type=int,
 metavar=('ID', 'PLACES'),
 help="Moves item ID down by a number of PLACES")
edit_item.add_argument('-c', '--check', type=int, metavar='ID',
 help="Marks item ID as done. If 0 is entered, marks ALL as done")
edit_item.add_argument('-k', '--uncheck', type=int, metavar='ID',
 help="Marks item ID as not done. If 0 is entered, marks ALL as not done")
edit_item.add_argument('-p', '--change', nargs = 2, type=int,
 metavar=('ID', 'PRIORITY'),
 help="Changes the priority of ID to PRIORITY")

remove_item = parser.add_argument_group('Remove a to-do')
remove_item.add_argument('-r', '--remove', type=int, metavar='ID',
 help="Remove a to-do using its ID number")
remove_item.add_argument('-confirm', action='store_true',
 help="Confirm removal on command-line")

display_list = parser.add_argument_group('Display the to-do list')
display_list.add_argument('-l', '--list', action='store_true',
 help="List all to-do's")
display_list.add_argument('-t', '--auto', action='store_true',
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
from model import Model
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

    with Model(get_db_path) as db:
    # Contains the work functions and connects them to the to-do file

        if args.description:    # add to-do item
            for item in args.description:
                # Capitalize first word
                item[0] = item[0].capitalize()
                # String the words of the description together
                description = " ".join(item)
                db.add(description, priority=0)
                log.info(f'to-do: "{description}" was added with priority: 0')

        if args.move_up:
            start = args.move_up[0] - 1
            places = args.move_up[1]
            todo = db.get_todo(start)
            for index in range(start, start - places, -1):
                db.move_up(index)
            log.info(f"""to-do #{args.move_up[0]}: "{todo['Description']}" """
            f"moved up {places} places")

        if args.move_down:
            start = args.move_down[0] - 1
            places = args.move_down[1]
            todo = db.get_todo(start)
            for index in range(start, start + places):
                db.move_down(index)
            log.info(f"""to-do #{args.move_down[0]}: "{todo['Description']}" """
            f"moved down {places} places")

        if args.check is not None:    # complete to-do item, or all of them
            if args.check == 0:
                for index in range(len(db.get_todo_list())):
                    db.set_done(index)
                log.info("All to-do items marked as done!")
            else:
                id = args.check - 1
                todo = db.get_todo(id)
                db.set_done(id)
                log.info(f"""to-do #{args.check}: "{todo['Description']}" """
                    "marked as done!")

        if args.uncheck is not None:  # un-complete to-do item, or all of them
            if args.uncheck == 0:
                for index in range(len(db.get_todo_list())):
                    db.set_not_done(index)
                log.info("All to-do items marked as not done!")
            else:
                id = args.uncheck - 1
                todo = db.get_todo(id)
                db.set_not_done(id)
                log.info(f"""to-do #{args.uncheck}: "{todo['Description']}" """
                    "marked as not done!")

        if args.change:     # change priority
            id = args.change[0]-1
            priority = args.change[1]
            todo = db.get_todo(id)
            db.change_priority(id, priority)
            log.info(f"""to-do #{args.change[0]} "{todo['Description']}" """
            f"set to priority {priority}")


        if args.remove:
            id = args.remove - 1
            todo = db.get_todo(id)
            if args.confirm == False:
                confirimation = input("Really remove to-do"
                f""" "{todo['Description']}"? [y/N]""")
                
            if args.confirm == True or confirimation.upper() == 'Y':
                db.remove_todo(id)
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
            todo_list = db.get_todo_list()
            display(todo_list)

except IndexError:
    log.error("No such to-do item")
except OSError as err:
    log.error(err)