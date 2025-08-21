from __future__ import annotations

from abc import ABC
from typing import Callable, TypedDict
from math import floor

from ...utils.constants import PRINT_SEPARATOR_LENGTH
from ...utils.console_helpers import clear_console, get_user_choice


class Action(TypedDict):
    hotkey: str
    name: str
    action: Callable[[], None]


class Menu(ABC):
    """
    Abstract base class for a menu.

    Subclasses must provide:
    - `title` (string)
    - `action_list` (list of {hotkey, name, action})
    """

    def __init__(self) -> None:
        self.running: bool = False
        self.title: str
        self.action_list: list[Action]

    # ----- Helpers (concrete) -----

    def _clear_console(self) -> None:
        clear_console()

    def _stop_selecting(self):
        self.selecting = False

    def _calculate_separator_lengths(self, name: str):
        name_length: int = len(name)
        side_length: int = (
            floor((PRINT_SEPARATOR_LENGTH - name_length) / 2)
            - 1  # -1 for spaceing left and right of the name
        )
        left_length: int = side_length
        right_length: int = side_length + 1 if name_length % 2 != 0 else side_length
        return (left_length, right_length)

    def _get_side_separators(self, name: str) -> tuple[str, str]:
        left_length, right_length = self._calculate_separator_lengths(name)
        left_separator: str = "=" * left_length
        right_separator: str = "=" * right_length
        return (left_separator, right_separator)

    def _print_separator(self) -> None:
        print("=" * PRINT_SEPARATOR_LENGTH)

    def _print_menu_name(self, name: str) -> None:
        left_separator, right_separator = self._get_side_separators(name)
        self._clear_console()
        self._print_separator()
        print(f"{left_separator} {name} {right_separator}")
        self._print_separator()

    def _get_user_choice(self, message: str = "") -> str:
        return get_user_choice(message)

    def _match_choice(self, choice: str, action_list: list[Action]) -> None:
        for action in action_list:
            if action["hotkey"] == choice:
                action["action"]()
                break  # stop at first match

    def _print_actions(self, action_list: list[Action]) -> None:
        for action in action_list:
            print(f'{action["hotkey"]} - {action["name"].capitalize()}')

    # ----- Public API -----

    def run(self) -> None:
        """
        Basic loop: show header/actions, accept choice, execute, and
        re-check authentication until authenticated or stopped.
        Subclasses can override for custom flow.
        """
        self.running = True
        while self.running:
            self._print_menu_name(self.title)
            self._print_actions(self.action_list)
            choice = self._get_user_choice().strip()
            self._match_choice(choice, self.action_list)

    def __repr__(self) -> str:
        actions_string = " - ".join(
            f'{a["hotkey"]} {a["name"]}' for a in self.action_list
        )
        return f"Running: {self.running} | " f"Action-List: {actions_string}"
