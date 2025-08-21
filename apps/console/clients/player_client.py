from src.services.player_service import PlayerService

from .client import Client


class PlayerClient(Client):
    def __init__(self):
        super().__init__()
        self.title: str = "Player-Client"
        self.player_service = PlayerService()

    def __repr__(self):
        return super().__repr__() + f"Player-Service: {self.player_service}"
