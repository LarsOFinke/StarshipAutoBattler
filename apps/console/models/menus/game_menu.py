from ...clients.game_client import GameClient

from .menu import Menu, Action


class GameMenu(Menu):
    def __init__(self):
        super().__init__()
        self.title = "Game-Menu"
        self.game_client = GameClient()
        self.action_list: list[Action] = [
            {
                "hotkey": "1",
                "name": "Select character",
                "action": self._select_character,
            },
            {
                "hotkey": "0",
                "name": "Return to Main-Menu",
                "action": self._stop,
            },
        ]

    def _select_character(self):
        pass

    def __repr__(self):
        return super().__repr__() + f" | Game-Client - {self.game_client}"
