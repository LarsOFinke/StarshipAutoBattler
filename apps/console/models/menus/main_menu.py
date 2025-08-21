from ...clients.auth_client import auth_client
from ...clients.config_client import ConfigClient
from .menu import Menu
from .game_menu import GameMenu


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.title = "Main-Menu"
        self.auth_client = auth_client
        self.cfg_client = ConfigClient()
        self.action_list: list[dict[str:callable]] = [
            {"hotkey": "1", "name": "play", "action": self._play},
            {"hotkey": "7", "name": "profile", "action": self._profile},
            {"hotkey": "8", "name": "settings", "action": self._settings},
            {"hotkey": "0", "name": "logout", "action": self._stop},
        ]
        self.setting_actions: list[dict[str:callable]] = [
            {
                "hotkey": "1",
                "name": "Config settings",
                "action": self.cfg_client.run,
            },
            {"hotkey": "0", "name": "Back", "action": self._stop_selecting},
        ]

    # -- HELPERS -- #

    def _print_user_info(self) -> None:
        print(
            f"User-ID: {self.auth_client.get_user_id()} \n"
            f"Username: {self.auth_client.get_username()} \n"
            f"Created at: {self.auth_client.get_user_created_at()}"
        )

    def _stop_selecting_settings(self) -> None:
        self.selecting_settings = False

    # -- ACTIONS -- #

    def _play(self):
        game_menu = GameMenu()
        game_menu.run()

    def _profile(self):
        self._print_header("Profile")
        self._print_user_info()
        self._get_user_choice()

    def _settings(self):
        self.selecting: bool = True
        while self.selecting:
            self._print_header("Settings")
            self._print_actions(self.setting_actions)
            choice = self._get_user_choice()
            self._match_choice(choice, self.setting_actions)

    def __repr__(self):
        return (
            super().__repr__()
            + f"Auth-Client: {self.auth_client} | Config-Client: {self.cfg_client}"
        )
