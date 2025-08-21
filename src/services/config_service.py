from configparser import ConfigParser

from ..config import CONFIG_PATH

from .logger_service import log, log_duration

from .service import Service


class ConfigService(Service):
    @log_duration
    def __init__(self):
        self.title: str = "Config-Service"
        self.path: str = CONFIG_PATH
        self.cfg = self._setup_config()
        log(f"Config-Service initialised - {self}", "dev-info")

    @log_duration
    def _setup_config(self):
        log("Setting up config for the Config-Service.", "dev-info")
        cfg = ConfigParser()
        cfg.optionxform = str  # keep key case as-is
        cfg.read(self.path)
        log("Config for the Config-Service is set up.", "dev-info")
        return cfg

    # -- Public API -- #

    @log_duration
    def change_key(self, section, key, value):
        """Example:
        section = "ui"
        key, value = "theme", "dark"
        """
        log("Attempting to change config-key.")
        if not self.cfg.has_section(section):
            log(f"Section ({section}) not found.")
            self.cfg.add_section(section)
            log(f"Section ({section}) added.")
        self.cfg.set(section, key, value)
        log(f"Key ({key}) with Value ({value}) set.")

        with open(self.path, "w") as f:
            log("Attempting to overwrite config.")
            self.cfg.write(f)
            log("Config successfully overwritten.")

    def __repr__(self):
        return super().__repr__() + f"Path: {self.path} | Config: {self.cfg}"
