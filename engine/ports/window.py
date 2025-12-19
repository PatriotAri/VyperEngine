from abc import ABC, abstractmethod
from typing import Tuple

from engine.ports.input_state import InputState


class Window(ABC):
    """
    Backend-agnostic window interface.
    Responsible for OS window management and event polling.
    """

    @abstractmethod
    def poll_events(self, input_state: InputState) -> None:
        """
        Poll OS / backend events and populate InputState.
        Must be called once per frame.
        """
        pass

    @abstractmethod
    def should_close(self) -> bool:
        """Return True if the window has requested to close."""
        pass

    @abstractmethod
    def get_size(self) -> Tuple[int, int]:
        """Return the current window size in pixels."""
        pass

    @abstractmethod
    def set_title(self, title: str) -> None:
        """Set the window title."""
        pass
