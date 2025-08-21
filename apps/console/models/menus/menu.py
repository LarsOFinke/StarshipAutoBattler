from __future__ import annotations

from abc import ABC
from typing import Callable, TypedDict

from ...utils.constants import PRINT_SEPARATOR_LENGTH
from ...utils.console_helpers import clear_console, get_user_choice


class Action(TypedDict):
    hotkey: str
    name: str
    action: Callable[[], None]


class Menu(ABC):
    """
    Abstract base class for an authentication menu.

    Subclasses must provide:
      - `action_list` (list of {hotkey, name, action})
    """

    def __init__(self) -> None:
        self.running: bool = True
        self.title: str
        self.action_list: list[Action]

    # ----- Helpers (concrete) -----

    def _clear_console(self) -> None:
        clear_console()

    def _print_separator(self) -> None:
        print("=" * PRINT_SEPARATOR_LENGTH)

    def _print_header(self) -> None:
        self._print_separator()
        print(self.title)
        self._print_separator()

    def _get_user_choice(self) -> str:
        return get_user_choice()

    def _match_choice(self, choice: str, action_list: list[Action]) -> None:
        for action in action_list:
            if action["hotkey"] == choice:
                action["action"]()
                break  # stop at first match

    def _print_actions(self) -> None:
        for action in self.action_list:
            print(f'{action["hotkey"]} - {action["name"].capitalize()}')

    # ----- Public API -----

    def run(self) -> None:
        """
        Basic loop: show header/actions, accept choice, execute, and
        re-check authentication until authenticated or stopped.
        Subclasses can override for custom flow.
        """
        while self.running:
            self._clear_console()
            self._print_header()
            self._print_actions()
            choice = self._get_user_choice().strip()
            self._match_choice(choice, self.action_list)

    def __repr__(self) -> str:
        actions_string = " - ".join(
            f'{a["hotkey"]} {a["name"]}' for a in self.action_list
        )
        return f"Running: {self.running} | " f"Action-List: {actions_string}"
