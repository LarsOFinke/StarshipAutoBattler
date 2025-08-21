from src.services.game_service import GameService

from .client import Client


class GameClient(Client):
    def __init__(self):
        super().__init__()
        self.title: str = "Game-Client"
        self.game_service = GameService()

    def __repr__(self):
        return super().__repr__() + f"Game-Service: {self.game_service}"
