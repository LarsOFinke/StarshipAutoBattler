from src.services.auth_service import AuthService

from .client import Client


class AuthClient(Client):
    def __init__(self):
        super().__init__()
        self.title: str = "Auth-Client"
        self.auth_service = AuthService()
        self._authenticated: bool = False
        self.user = None

    # -- Helpers -- #

    # -- Public API -- #

    def is_authenticated(self):
        return self._authenticated

    def get_user_id(self):
        return self._user_id

    def get_username(self):
        return self._username

    def get_user_created_at(self):
        return self._user_created_at

    def login(self) -> None:
        self._print_header("Login")
        username: str = self._get_user_choice("Please enter the username:")
        password: str = self._get_user_choice("Please enter the password:")
        if not self.auth_service.login(username, password):
            input("Login failed.\nPress Enter")
            return
        self.user = self.auth_service.get_user()
        self._authenticated = self.auth_service.is_authenticated()
        return

    def register(self) -> None:
        self._print_header("Registration")
        username: str = self._get_user_choice("Please enter the username:")
        pw1: str = self._get_user_choice("Please enter the password:")
        pw2: str = self._get_user_choice("Please confirm the password:")
        if not self.auth_service.register(username, pw1, pw2):
            input("Registration failed.\nPress Enter")
            return
        self.user = self.auth_service.get_user()
        self._authenticated = self.auth_service.is_authenticated()
        input(self._authenticated)
        return

    def __repr__(self):
        return (
            super().__repr__()
            + f"Authenticated: {self.is_authenticated()} | User-ID: {self._user_id} | Username: {self._username} | User created at: {self._user_created_at}"
        )


auth_client = AuthClient()
