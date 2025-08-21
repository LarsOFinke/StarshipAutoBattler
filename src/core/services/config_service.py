from configparser import ConfigParser

from ...config import CONFIG_PATH
from .logger_service import logger


class ConfigService:
    def __init__(self):
        self.path: str = CONFIG_PATH
        self.cfg = self._setup_config()
        logger.log(self, "dev-info")

    def _setup_config(self):
        cfg = ConfigParser()
        cfg.optionxform = str  # keep key case as-is
        cfg.read(self.path)
        return cfg

    # -- Public API -- #

    def change_key(self, section, key, value):
        """Example:
        section = "ui"
        key, value = "theme", "dark"
        """
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
        self.cfg.set(section, key, value)

        with open(self.path, "w") as f:
            self.cfg.write(f)

    def __repr__(self):
        return f"Path: {self.path} | Config: {self.cfg}"
