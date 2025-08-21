import base64, hashlib, hmac, secrets

from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .logger_service import logger
from .database_service import database_service
from ..models.user import User
from ..utils.constants import SALT_BYTES, ITERATIONS, ALG


class AuthService:
    def __init__(self):
        self.database_service = database_service
        self._authenticated: bool = False
        self.user_id: int = 0
        self.username: str = ""
        self.user_created_at: str = ""
        logger.log(self, "dev-info")

    def _password_checks(self, pw1, pw2) -> bool:
        logger.log("Checking passwords.")
        if pw1 == pw2:
            logger.log("Passwords match.")
            return True
        logger.log("Password check failed.", "warning")
        return False

    def _hash_password(self, password: str) -> str:
        logger.log("Hashing password.")
        salt = secrets.token_bytes(SALT_BYTES)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
        logger.log("Password hashed.")
        return (
            f"{ALG}${ITERATIONS}$"
            f"{base64.b64encode(salt).decode()}$"
            f"{base64.b64encode(dk).decode()}"
        )

    def _verify_password(self, password: str, stored: str) -> bool:
        logger.log("Starting verify-password.")
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
            logger.log(f"Verify-password failed. {e}", "error")
            return False

    def _get_user_by_name(self, session, name: str) -> Optional[User]:
        logger.log("Getting user by name.")
        stmt = select(User).where(User.name == name)
        logger.log("User found")
        return session.scalar(stmt)

    def _process_authentication(self, user) -> None:
        self.user_id = user.id
        self.username = user.name
        self.user_created_at = user.created_at
        self._authenticated = True
        logger.log(f"Authenticaton processed. {self}", "dev-info")
        return

    def is_authenticated(self):
        return self._authenticated

    @logger.log_duration
    def register(self, name, pw1, pw2) -> Optional[bool]:
        logger.log("Starting registration.")
        with self.database_service.db_session() as s:
            if not self._password_checks(pw1, pw2):
                logger.log(
                    "Registration failed. Passwords don't match requirements.",
                    "error",
                )
                raise ValueError("Passwörter erfüllen nicht die Voraussetzungen.")

            user = User(name=name, password_hash=self._hash_password(pw1))
            s.add(user)
            try:
                s.flush()
            except IntegrityError as e:
                s.rollback()
                logger.log(f"Registration failed. {e}", "error")
                raise ValueError("Name ist bereits registriert.") from e
            self._process_authentication(user)
            return True

    @logger.log_duration
    def login(self, name, password) -> bool:
        logger.log("Starting login.")
        with self.database_service.db_session() as s:
            user = self._get_user_by_name(s, name)
            if (
                user
                and self._verify_password(password, user.password_hash)
                and user.is_active
            ):
                logger.log("Login successful")
                self._process_authentication(user)
                return True
            logger.log("Login failed.", "warning")
            return False

    def __repr__(self):
        return f"Database-Service: {self.database_service} | Authenticated: {self.is_authenticated()} | User-ID: {self.user_id} | Username: {self.username} | User created at: {self.user_created_at}"
