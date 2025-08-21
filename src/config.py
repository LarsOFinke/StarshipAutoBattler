from __future__ import annotations

import os
from dotenv import dotenv_values


# --- Lade-Reihenfolge ---
# Niedrige Priorität → hohe Priorität.
# OS-Umgebungsvariablen haben immer Vorrang (werden nie überschrieben).
def _load_env_chain(app_env: str | None = None) -> None:
    env = (app_env or os.getenv("APP_ENV") or "dev").lower()

    files_in_order = [
        ".config",
        f".config.{env}",
        ".config.local",
        ".env",
        f".env.{env}",
        ".env.local",
    ]

    merged: dict[str, str] = {}
    for path in files_in_order:
        if os.path.exists(path):
            merged.update(dotenv_values(path))  # spätere Dateien überschreiben frühere

    # Nur setzen, wenn noch NICHT in OS-Env vorhanden → OS-Env gewinnt immer.
    for k, v in merged.items():
        if v is None:
            continue
        if k not in os.environ:
            os.environ[k] = v


# Früh laden (vor dem Auslesen unten):
_load_env_chain()

# ---- AB HIER deine bisherigen Auslese-Helper & Werte ----

_TRUE = {"1", "true", "yes", "on", "y"}
_FALSE = {"0", "false", "no", "off", "n"}


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    v = value.strip().lower()
    if v in _TRUE:
        return True
    if v in _FALSE:
        return False
    return default


# -- General -- #
CONFIG_PATH = os.getenv("CONFIG_PATH")

# -- Logging -- #

DEV_MODE = _as_bool(os.getenv("DEV_MODE"))
LOG_LEVEL = os.getenv("LOG_LEVEL").strip().lower()  # Convert to lowercase for checks
LOG_CONSOLE = _as_bool(os.getenv("LOG_CONSOLE"))
LOG_FILE = _as_bool(os.getenv("LOG_FILE"))
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME")
LOG_FILE_TYPE = (
    os.getenv("LOG_FILE_TYPE").strip().lower()
)  # Convert to lowercase for checks

# -- Database -- #
DATABASE_URL = os.getenv("DATABASE_URL")
