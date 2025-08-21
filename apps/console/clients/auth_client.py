from src.services.auth_service import AuthService

from ..utils.console_helpers import clear_console, get_user_choice


class AuthClient:
    def __init__(self):
        self.auth_service = AuthService()
        self._authenticated: bool = False
        self._user_id: int = 0
        self._username: str = ""
        self._user_created_at: str = ""

    def _process_authentication(self) -> None:
        self._user_id = self.auth_service.user_id
        self._username = self.auth_service.username
        self._user_created_at = self.auth_service.user_created_at
        self._authenticated = self.auth_service.is_authenticated()
        return

    # -- Public API -- #

    def is_authenticated(self):
        return self._authenticated

    def get_user_id(self):
        return self._user_id

    def get_username(self):
        return self._username

    def get_user_created_at(self):
        return self._user_created_at

    def login(self, username: str, password: str) -> None:
        if not self.auth_service.login(username, password):
            input("Login failed.\nPress Enter")
            return
        self._process_authentication()
        return

    def register(self, username: str, pw1: str, pw2: str) -> None:
        if not self.auth_service.register(username, pw1, pw2):
            input("Registration failed.\nPress Enter")
            return
        self._process_authentication()
        return

    def __repr__(self):
        return f"Authenticated: {self.is_authenticated()} | User-ID: {self._user_id} | Username: {self._username} | User created at: {self._user_created_at}"


auth_client = AuthClient()
