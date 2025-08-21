from __future__ import annotations

from abc import ABC

from ..utils.console_helpers import (
    Action,
    clear_console,
    print_separator,
    print_header,
    print_actions,
    get_user_choice,
    match_choice,
)


class Client(ABC):
    """
    Abstract base class for a client.

    Subclasses must provide:
    - `title` (string)
    - `action_list` (list of {hotkey, name, action})
    """

    def __init__(self) -> None:
        self.running: bool = False
        self.selecting = False
        self.title: str
        self.action_list: list[Action]

    # ----- Helpers (concrete) -----

    def _stop_selecting(self):
        self.selecting = False

    def _clear_console(self) -> None:
        clear_console()

    def _print_separator(self) -> None:
        print_separator()

    def _print_header(self, name: str) -> None:
        print_header(name)

    def _get_user_choice(self, message: str = "") -> str:
        return get_user_choice(message)

    def _match_choice(self, choice: str, action_list: list[Action]) -> None:
        match_choice(choice, action_list)

    def _print_actions(self, action_list: list[Action]) -> None:
        print_actions(action_list)

    # ----- Public API -----

    def _stop(self):
        self.running = False

    def run(self) -> None:
        """
        Basic loop: show header/actions, accept choice, execute, and
        re-check authentication until authenticated or stopped.
        Subclasses can override for custom flow.
        """
        self.running = True
        while self.running:
            self._print_header(self.title)
            self._print_actions(self.action_list)
            choice = self._get_user_choice().strip()
            self._match_choice(choice, self.action_list)

    def __repr__(self) -> str:
        return f"{self.title} "
