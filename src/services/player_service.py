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

    # -- Public API -- #

    @log_duration
    def create_player_character(self) -> None:
        pass

    @log_duration
    def get_player_character(self) -> PlayerCharacter | None:
        return self.player

    @log_duration
    def list_player_characters(self) -> list:
        player_character_list: list[PlayerCharacter] = []
        return player_character_list

    def __repr__(self):
        return f"Player: {self.player} | Database-Service: {self.database_service}"
