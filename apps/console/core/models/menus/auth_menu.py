from ...services.auth_service import auth_service

from .menu import Menu


class AuthMenu(Menu):
    def __init__(self):
        super().__init__()
        self.running: bool = True
        self.title = "Auth-Menu"
        self.auth_service = auth_service
        self.action_list: list[dict[str:callable]] = [
            {"hotkey": "1", "name": "login", "action": self._login},
            {"hotkey": "2", "name": "register", "action": self._register},
            {"hotkey": "0", "name": "exit", "action": self._close},
        ]

    def _login(self):
        self.auth_service.login()
        if self.auth_service.is_authenticated():
            self.running = False

    def _register(self):
        self.auth_service.register()
        if self.auth_service.is_authenticated():
            self.running = False

    def _close(self) -> None:
        self.running = False
        return

    def __repr__(self):
        return super().__repr__() + f" | Auth-Service: {self.auth_service}"
