from src.services.config_service import ConfigService


class ConfigClient:
    def __init__(self):
        self.cfg_service = ConfigService

    def toggle_dev_mode(self) -> bool:
        try:
            self.cfg_service.change_key("Logging", "DEV_MODE", "0")
            return True
        except:
            return False
