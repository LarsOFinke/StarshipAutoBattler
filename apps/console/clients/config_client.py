from functools import partial

from src.services.config_service import ConfigService


class ConfigClient:
    def __init__(self):
        self.cfg_service = ConfigService()
        self.dev_mode_actions: list[dict[str:callable]] = [
            {
                "hotkey": "1",
                "name": "Enable Dev-Mode",
                "action": partial(self.toggle_dev_mode, activate=True),
            },
            {
                "hotkey": "2",
                "name": "Disable Dev-Mode",
                "action": partial(self.toggle_dev_mode, activate=False),
            },
        ]

    def toggle_dev_mode(self, activate: bool) -> bool:
        try:
            self.cfg_service.change_key("Logging", "DEV_MODE", "1" if activate else "0")
            return True
        except:
            return False

    def __repr__(self):
        return f"Config-Service - {self.cfg_service}"
