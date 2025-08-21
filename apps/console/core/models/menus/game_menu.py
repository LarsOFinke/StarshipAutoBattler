from .menu import Menu


class GameMenu(Menu):
    def __init__(self):
        super().__init__()
        self.running = True
        self.title = "Game-Menu"
        self.action_list: list[dict[str:callable]] = [
            {
                "hotkey": "0",
                "name": "Return to Main-Menu",
                "action": self._return_to_main_menu,
            },
        ]

    def _return_to_main_menu(self):
        self.running = False
