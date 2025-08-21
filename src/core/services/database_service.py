from __future__ import annotations
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .logger_service import logger
from ...config import DATABASE_URL
from ..models.orm_base import Base


class DatabaseService:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=False, future=True)
        self.session = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, future=True
        )

    # ---------- Session Helper ----------
    @logger.log_duration
    @contextmanager
    def db_session(self):
        with self.session.begin() as session:
            logger.log("Starting DB-session.")
            try:
                yield session
                session.commit()
                logger.log("DB-session successfully committed.")
            except:
                session.rollback()
                logger.log("DB-session rolled back.", "error")
                raise
            finally:
                session.close()
                logger.log("DB-sessions closed.")

    @logger.log_duration
    def init_db(self):
        logger.log("Initiatlizing the Database.")
        from ..models import user

        Base.metadata.create_all(self.engine)
        logger.log("Database initialized.")

    def __repr__(self):
        return f"Engine: {self.engine} | Session: {self.session}"


database_service = DatabaseService()
database_service.init_db()

"""
with db_session() as s:
    # Registrierung
    try:
        u = create_user(s, "test", "sicheresPasswort123!")
        print("Registriert:", u.id, u.name)
    except ValueError as e:
        print("Registrierung fehlgeschlagen:", e)

    # Login
    ok = authenticate(s, "test", "sicheresPasswort123!")
    print("Login OK:", bool(ok))

    bad = authenticate(s, "test", "falsch")
    print("Login mit falschem Passwort:", bool(bad))
"""
