from src.services.game_service import GameService as GameSrvc


class GameService:
    def __init__(self):
        self.game_srvc = GameSrvc()
