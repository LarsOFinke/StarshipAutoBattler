from src.services.game_service import GameService
from src.services.player_service import PlayerService


class GameClient:
    def __init__(self):
        self.game_service = GameService()
        self.player_service = PlayerService()
        
    def select_player_character(self):
        name: str = ""
        self.player_service._get_player_character_by_name(name)

    def __repr__(self):
        return f"Game-Client - Game-Service: {self.game_service}"
