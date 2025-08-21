from __future__ import annotations

from abc import ABC


class Service(ABC):
    """
    Abstract base class for a service.
    """

    def __init__(self) -> None:
        self.title: str

    def __repr__(self) -> str:
        return f"{self.title} - "
