import base64, hashlib, hmac, secrets

from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..utils.constants import SALT_BYTES, ITERATIONS, ALG

from .logger_service import log, log_duration
from .database_service import database_service

from .service import Service
from ..models.user import User


class AuthService(Service):
    @log_duration
    def __init__(self):
        self.title: str = "Auth-Service"
        self.database_service = database_service
        self._user = None
        self._authenticated: bool = False
        self.user_id: int = 0
        self.username: str = ""
        self.user_created_at: str = ""
        log(f"Auth-Service initialised - {self}", "dev-info")

    # -- Helpers -- #

    @log_duration
    def _password_checks(self, pw1, pw2) -> bool:
        log("Checking passwords.", "dev-info")
        if pw1 == pw2:
            log("Passwords match.", "dev-info")
            return True
        log("Password check failed.", "warning")
        return False

    @log_duration
    def _hash_password(self, password: str) -> str:
        log("Hashing password.", "dev-info")
        salt = secrets.token_bytes(SALT_BYTES)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
        log("Password hashed.", "dev-info")
        return (
            f"{ALG}${ITERATIONS}$"
            f"{base64.b64encode(salt).decode()}$"
            f"{base64.b64encode(dk).decode()}"
        )

    @log_duration
    def _verify_password(self, password: str, stored: str) -> bool:
        log("Starting verify-password.", "dev-info")
        try:
            alg, iter_str, b64_salt, b64_hash = stored.split("$", 3)
            if alg != ALG:
                return False
            iterations = int(iter_str)
            salt = base64.b64decode(b64_salt)
            expected = base64.b64decode(b64_hash)
            candidate = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt, iterations
            )
            return hmac.compare_digest(expected, candidate)
        except Exception as e:
            log(f"Verify-password failed. {e}", "error")
            return False

    @log_duration
    def _get_user_by_name(self, session, name: str) -> Optional[User]:
        log("Getting user by name.", "dev-info")
        query = select(User).where(User.name == name)
        log("User found", "dev-info")
        return session.scalar(query)

    @log_duration
    def _process_authentication(self, user) -> None:
        log("Starting processing authentication.", "dev-info")
        self.user_id = user.id
        self.username = user.name
        self.user_created_at = user.created_at
        self._authenticated = True
        log(f"Authenticaton processed. {self}", "dev-info")
        return

    # -- Public API -- #

    @log_duration
    def is_authenticated(self):
        return self._authenticated

    @log_duration
    def get_user(self):
        return self._user

    @log_duration
    def register(self, name, pw1, pw2) -> bool:
        log("Starting registration.")
        with self.database_service.db_session() as s:
            if not self._password_checks(pw1, pw2):
                log("Registration failed. Passwords don't match requirements.")
                raise ValueError("Passwörter erfüllen nicht die Voraussetzungen.")

            user = User(name=name, password_hash=self._hash_password(pw1))
            s.add(user)
            try:
                s.flush()
                self._user = user
                log("User successfully registered.")
            except IntegrityError as e:
                s.rollback()
                log(f"Registration failed. {e}", "error")
                return False
            # self._process_authentication(user)
            log("User successfully authenticated.")
            self._authenticated = True
            return True

    @log_duration
    def login(self, name, password) -> bool:
        log("Starting login.")
        with self.database_service.db_session() as s:
            user = self._get_user_by_name(s, name)
            if (
                user
                and self._verify_password(password, user.password_hash)
                and user.is_active
            ):
                # self._process_authentication(user)
                self._user = user
                self._authenticated = True
                log("Login successful")
                return True
            log("Login failed.")
            return False

    def __repr__(self):
        return (
            super().__repr__()
            + f"Database-Service: {self.database_service} | Authenticated: {self.is_authenticated()} | User-ID: {self.user_id} | Username: {self.username} | User created at: {self.user_created_at}"
        )
