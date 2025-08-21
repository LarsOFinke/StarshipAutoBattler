# import os, sys
from os import system, name
from sys import stdout


def clear_console() -> None:
    """Clear the terminal screen if we're attached to a TTY; otherwise just add space."""
    if stdout.isatty():
        system("cls" if name == "nt" else "clear")
    else:
        # When output is piped/redirected (not a TTY), avoid control codes.
        print("\n" * 50)


def get_user_choice() -> str:
    return input("")
