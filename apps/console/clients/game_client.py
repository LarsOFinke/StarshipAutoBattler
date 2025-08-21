from src.services.game_service import GameService


class GameClient:
    def __init__(self):
        self.game_service = GameService()
