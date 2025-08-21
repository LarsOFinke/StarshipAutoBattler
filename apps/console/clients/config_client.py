from functools import partial

from src.services.config_service import ConfigService


class ConfigClient:
    def __init__(self):
        self.cfg_service = ConfigService()
        self.dev_mode_actions: list[dict[str:callable]] = [
            {
                "hotkey": "1",
                "name": "Enable Dev-Mode",
                "action": partial(self._toggle_dev_mode, activate=True),
            },
            {
                "hotkey": "2",
                "name": "Disable Dev-Mode",
                "action": partial(self._toggle_dev_mode, activate=False),
            },
            {
                "hotkey": "0",
                "name": "Cancel",
                "action": lambda: None,
            },
        ]
        self.log_level_actions: list[dict[str:callable]] = [
            {
                "hotkey": "1",
                "name": "Set to Info-Level",
                "action": partial(self._set_log_level, level="INFO"),
            },
            {
                "hotkey": "2",
                "name": "Set to Warning-Level",
                "action": partial(self._set_log_level, level="WARNING"),
            },
            {
                "hotkey": "3",
                "name": "Set to Error-Level",
                "action": partial(self._set_log_level, level="ERROR"),
            },
            {
                "hotkey": "0",
                "name": "Cancel",
                "action": lambda: None,
            },
        ]

    def _toggle_dev_mode(self, activate: bool) -> bool:
        self.cfg_service.change_key("Logging", "DEV_MODE", "1" if activate else "0")

    def _set_log_level(self, level: str):
        self.cfg_service.change_key("Logging", "LOG_LEVEL", level)

    def __repr__(self):
        return f"Config-Service - {self.cfg_service}"
