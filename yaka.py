#! /usr/bin/env python3
# coding: utf-8
import argparse

from classes.db_connect import Connection
from classes.program_loop import ProgramLoop


def parse_arguments():
    """Retrieve arguments passed in program launch."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-k",
        "--keep",
        help="""Keep database and skip database import.""",
        action="store_true"
    )
    group.add_argument(
        "-i",
        "--initdb",
        help="""Just do the database initialization.
Do not execute the program""",
        action="store_true"
    )

    return parser.parse_args()


def main():
    """Program loop"""

    # Retrieve arguments
    args = parse_arguments()

    # On init : set the connection settings + connection test
    connect = Connection(args.keep)

    # If arg -i : Not execute the program loop
    if args.initdb:
        # Stop the program
        exit()

    else:
        # Execute the program loop
        while True:
            ProgramLoop(connect)


if __name__ == "__main__":
    main()
