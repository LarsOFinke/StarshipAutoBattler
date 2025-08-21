from ...clients.auth_client import auth_client
from ...clients.config_client import ConfigClient
from .menu import Menu
from .game_menu import GameMenu


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.running = True
        self.title = "Main-Menu"
        self.auth_client = auth_client
        self.cfg_client = ConfigClient()
        self.action_list: list[dict[str:callable]] = [
            {"hotkey": "1", "name": "play", "action": self._play},
            {"hotkey": "7", "name": "profile", "action": self._profile},
            {"hotkey": "8", "name": "settings", "action": self._settings},
            {"hotkey": "0", "name": "logout", "action": self._logout},
        ]
        self.config_setting_actions: list[dict[str:callable]] = [
            {
                "hotkey": "1",
                "name": "Change Dev-Mode",
                "action": self._change_dev_mode,
            },
            {
                "hotkey": "2",
                "name": "Change Log-Level",
                "action": self._change_log_level,
            },
            {
                "hotkey": "0",
                "name": "Back",
                "action": self._stop_selecting,
            },
        ]

    # -- HELPERS -- #

    def _print_user_info(self) -> None:
        print(
            f"User-ID: {self.auth_client.get_user_id()} \n"
            f"Username: {self.auth_client.get_username()} \n"
            f"Created at: {self.auth_client.get_user_created_at()}"
        )

    # -- Config-Settings -- #

    def _change_dev_mode(self):
        self._clear_console()
        self._print_actions(self.cfg_client.dev_mode_actions)
        choice: str = self._get_user_choice()
        self._match_choice(choice, self.cfg_client.dev_mode_actions)

    def _change_log_level(self):
        pass

    # -- ACTIONS -- #

    def _play(self):
        game_menu = GameMenu()
        game_menu.run()

    def _profile(self):
        self._print_menu_name("Profile")
        self._print_user_info()
        input()

    def _settings(self):
        self.selecting: bool = True
        while self.selecting:
            self._print_menu_name("Settings")
            self._print_actions(self.config_setting_actions)
            choice = self._get_user_choice()
            self._match_choice(choice, self.config_setting_actions)

    def _logout(self):
        self.running = False

    def __repr__(self):
        return (
            super().__repr__()
            + f" | Auth-Client: {self.auth_client} | Config-Client: {self.cfg_client}"
        )
