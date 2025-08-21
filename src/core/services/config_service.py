from configparser import ConfigParser

from ...config import CONFIG_PATH
from .logger_service import log, log_duration


class ConfigService:
    def __init__(self):
        self.path: str = CONFIG_PATH
        self.cfg = self._setup_config()
        log(self, "dev-info")

    def _setup_config(self):
        cfg = ConfigParser()
        cfg.optionxform = str  # keep key case as-is
        cfg.read(self.path)
        return cfg

    # -- Public API -- #

    @log_duration
    def change_key(self, section, key, value):
        """Example:
        section = "ui"
        key, value = "theme", "dark"
        """
        log("Attempting to change config-key.", "dev-info")
        if not self.cfg.has_section(section):
            log(f"Section ({section}) not found.", "dev-info")
            self.cfg.add_section(section)
            log(f"Section ({section}) added.", "dev-info")
        self.cfg.set(section, key, value)
        log(f"Key ({key}) with Value ({value}) set.", "dev-info")

        with open(self.path, "w") as f:
            log("Attempting to overwrite config.", "dev-info")
            self.cfg.write(f)
            log("Config successfully overwritten.", "dev-info")

    def __repr__(self):
        return f"Path: {self.path} | Config: {self.cfg}"
