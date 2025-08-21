from functools import partial

from src.services.config_service import ConfigService
from .client import Client


class ConfigClient(Client):
    def __init__(self):
        super().__init__()
        self.title: str = "Config-Client"
        self.cfg_service = ConfigService()
        self.action_list: list[dict[str:callable]] = [
            {"hotkey": "1", "name": "Dev-Mode", "action": self._change_dev_mode},
            {"hotkey": "2", "name": "Log-Level", "action": self._change_log_level},
            {"hotkey": "3", "name": "Console-Log", "action": self._change_console_log},
            {"hotkey": "4", "name": "File-Log", "action": self._change_file_log},
            {"hotkey": "0", "name": "Back", "action": self._stop},
        ]
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
        self.console_log_actions: list[dict[str:callable]] = [
            {
                "hotkey": "1",
                "name": "Enable console-logging",
                "action": partial(
                    self._set_output, output_type="console", activate=True
                ),
            },
            {
                "hotkey": "2",
                "name": "Disable console-logging",
                "action": partial(
                    self._set_output, output_type="console", activate=False
                ),
            },
            {
                "hotkey": "0",
                "name": "Cancel",
                "action": lambda: None,
            },
        ]
        self.file_log_actions: list[dict[str:callable]] = [
            {
                "hotkey": "1",
                "name": "Enable file-logging",
                "action": partial(self._set_output, output_type="file", activate=True),
            },
            {
                "hotkey": "2",
                "name": "Disable file-logging",
                "action": partial(self._set_output, output_type="file", activate=False),
            },
            {
                "hotkey": "3",
                "name": "Change file-name",
                "action": partial(self._set_output, output_type="file", activate=False),
            },
            {
                "hotkey": "3",
                "name": "Change file-type",
                "action": partial(self._set_output, output_type="file", activate=False),
            },
            {
                "hotkey": "0",
                "name": "Cancel",
                "action": lambda: None,
            },
        ]
        self.file_types: list[str] = ["text", "json", "csv"]

    # -- Helpers -- #

    def _list_file_types(self):
        print("")

    # -- Config-Settings -- #

    def _change_dev_mode(self):
        self._print_header("Settings - Config: Dev-Mode")
        self._print_actions(self.dev_mode_actions)
        choice: str = self._get_user_choice()
        self._match_choice(choice, self.dev_mode_actions)

    def _change_log_level(self):
        self._print_header("Settings - Config: Log-Level")
        self._print_actions(self.log_level_actions)
        choice: str = self._get_user_choice()
        self._match_choice(choice, self.log_level_actions)

    def _change_console_log(self):
        self._print_header("Settings - Config: Console-Log")
        self._print_actions(self.console_log_actions)
        choice: str = self._get_user_choice()
        self._match_choice(choice, self.console_log_actions)

    def _change_file_log(self):
        self._print_header("Settings - Config: File-Log")
        self._print_actions(self.file_log_actions)
        choice: str = self._get_user_choice()
        self._match_choice(choice, self.file_log_actions)

    # -- Actions -- #

    def _toggle_dev_mode(self, activate: bool) -> None:
        value: str = "1" if activate else "0"
        self.cfg_service.change_key("Logging", "DEV_MODE", value)

    def _set_log_level(self, level: str) -> None:
        self.cfg_service.change_key("Logging", "LOG_LEVEL", level)

    def _set_output(self, output_type: str, activate: bool) -> None:
        value: str = "1" if activate else "0"
        self.cfg_service.change_key("Logging", f"LOG_{output_type.upper()}", value)

    def _set_file_name(self) -> None:
        name: str = self.get_user_choice("New name:\n'0' to cancel")
        if name == "0":
            return
        self.cfg_service.change_key("Logging", "LOG_FILE_NAME", name)

    def _set_file_type(self) -> None:
        file_type: str = self.get_user_choice("New name:")
        self.cfg_service.change_key("Logging", "LOG_FILE_TYPE", file_type)

    def __repr__(self):
        return super().__repr__() + f"- Config-Service: {self.cfg_service}"
