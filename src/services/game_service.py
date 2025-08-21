from .logger_service import log, log_duration

from .service import Service


class GameService(Service):
    @log_duration
    def __init__(self):
        self.title: str = "Game-Service"
        log(f"Game-Service initialised - {self}", "dev-info")

    def __repr__(self):
        return super().__repr__() + f""
