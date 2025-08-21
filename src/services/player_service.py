from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .logger_service import log, log_duration
from .database_service import database_service

from .service import Service
from ..models.player_character import PlayerCharacter


class PlayerService(Service):
    @log_duration
    def __init__(self) -> None:
        self.title: str = "Player-Service"
        self.player: PlayerCharacter | None = None
        self.database_service = database_service
        log(f"Player-Service initialised - {self}", "dev-info")

    @log_duration
    def _get_player_character_by_name(self, name: str) -> PlayerCharacter | None:
        return self.player

    # -- Public API -- #

    @log_duration
    def create_player_character(self) -> None:
        pass

    @log_duration
    def select_player_character(self, name: str) -> None:
        player_character = self._get_player_character_by_name(name)
        return

    def __repr__(self):
        return (
            super().__repr__()
            + f"Player: {self.player} | Database-Service: {self.database_service}"
        )
