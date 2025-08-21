from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .logger_service import log, log_duration
from .database_service import database_service

from ..models.player_character import PlayerCharacter


class PlayerService:
    def __init__(self) -> None:
        self.player: PlayerCharacter | None = None
        self.database_service = database_service

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
        return f"Player: {self.player} | Database-Service: {self.database_service}"
