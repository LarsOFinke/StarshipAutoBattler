from ...services.game_service import GameService

from .menu import Menu


class GameMenu(Menu):
    def __init__(self):
        super().__init__()
        self.running = True
        self.title = "Game-Menu"
        self.game_service = GameService()
        self.action_list: list[dict[str:callable]] = [
            {
                "hotkey": "1",
                "name": "Select character",
                "action": self._select_character,
            },
            {
                "hotkey": "0",
                "name": "Return to Main-Menu",
                "action": self._return_to_main_menu,
            },
        ]

    def _select_character(self):
        pass

    def _return_to_main_menu(self):
        self.running = False
