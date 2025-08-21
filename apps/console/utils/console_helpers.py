# import os, sys
from os import system, name
from sys import stdout
from typing import Callable, TypedDict
from math import floor

from .constants import PRINT_SEPARATOR_LENGTH


class Action(TypedDict):
    hotkey: str
    name: str
    action: Callable[[], None]


def clear_console() -> None:
    """Clear the terminal screen if we're attached to a TTY.
    Otherwise just add space."""
    if stdout.isatty():
        system("cls" if name == "nt" else "clear")
    else:
        # When output is piped/redirected (not a TTY), avoid control codes.
        print("\n" * 50)


def print_separator() -> None:
    print("=" * PRINT_SEPARATOR_LENGTH)


def calculate_separator_lengths(name: str):
    name_length: int = len(name)
    side_length: int = (
        floor((PRINT_SEPARATOR_LENGTH - name_length) / 2)
        - 1  # -1 for spaceing left and right of the name
    )
    left_length: int = side_length
    right_length: int = side_length if name_length % 2 == 0 else side_length + 1
    return (left_length, right_length)


def get_side_separators(name: str) -> tuple[str, str]:
    left_length, right_length = calculate_separator_lengths(name)
    left_separator: str = "=" * left_length
    right_separator: str = "=" * right_length
    return (left_separator, right_separator)


def print_header(name: str) -> None:
    left_separator, right_separator = get_side_separators(name)
    clear_console()
    print_separator()
    print(f"{left_separator} {name} {right_separator}")
    print_separator()


def print_actions(action_list: list[Action]) -> None:
    for action in action_list:
        print(f'{action["hotkey"]} - {action["name"].capitalize()}')


def get_user_choice(message: str) -> str:
    return input(f"{message}\n")


def match_choice(choice: str, action_list: list[Action]) -> None:
    for action in action_list:
        if action["hotkey"] == choice:
            action["action"]()
            break  # stop at first match
