from ...clients.auth_client import auth_client

from .menu import Menu


class AuthMenu(Menu):
    def __init__(self):
        super().__init__()
        self.running: bool = True
        self.title = "Auth-Menu"
        self.auth_client = auth_client
        self.action_list: list[dict[str:callable]] = [
            {"hotkey": "1", "name": "login", "action": self._login},
            {"hotkey": "2", "name": "register", "action": self._register},
            {"hotkey": "0", "name": "exit", "action": self._close},
        ]

    def _login(self):
        self._clear_console()
        username: str = self._get_user_choice("Please enter the username:")
        password: str = self._get_user_choice("Please enter the password:")
        self.auth_client.login(username, password)
        if self.auth_client.is_authenticated():
            self.running = False

    def _register(self):
        self._clear_console()
        username: str = self._get_user_choice("Please enter the username:")
        pw1: str = self._get_user_choice("Please enter the password:")
        pw2: str = self._get_user_choice("Please confirm the password:")
        self.auth_client.register(username, pw1, pw2)
        if self.auth_client.is_authenticated():
            self.running = False

    def _close(self) -> None:
        self.running = False
        return

    def __repr__(self):
        return super().__repr__() + f" | Auth-Client: {self.auth_client}"
