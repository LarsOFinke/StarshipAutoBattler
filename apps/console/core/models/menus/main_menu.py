from src.core.services.config_service import ConfigService

from ...services.auth_service import auth_service
from .menu import Menu
from .game_menu import GameMenu


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.running = True
        self.title = "Main-Menu"
        self.auth_service = auth_service
        self.action_list: list[dict[str:callable]] = [
            {"hotkey": "1", "name": "play", "action": self._play},
            {"hotkey": "2", "name": "test", "action": self._test},
            {"hotkey": "7", "name": "profile", "action": self._profile},
            {"hotkey": "8", "name": "settings", "action": self._settings},
            {"hotkey": "0", "name": "logout", "action": self._logout},
        ]

    # -- HELPERS -- #

    def _print_user_info(self) -> None:
        print(
            f"User-ID: {self.auth_service.get_user_id()} \n"
            f"Username: {self.auth_service.get_username()} \n"
            f"Created at: {self.auth_service.get_user_created_at()}"
        )

    # -- ACTIONS -- #

    def _play(self):
        game_menu = GameMenu()
        game_menu.run()

    def _test(self):
        print(self.auth_service)
        input()

    def _profile(self):
        self._clear_console()
        self._print_separator()
        print("Profile")
        self._print_separator()
        self._print_user_info()
        input()

    def _settings(self):
        cfg_service = ConfigService()
        cfg_service.change_key("Logging", "DEV_MODE", "0")
        input()

    def _logout(self):
        self.running = False

    def __repr__(self):
        return super().__repr__()
