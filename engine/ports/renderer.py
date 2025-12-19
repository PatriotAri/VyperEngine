from abc import ABC, abstractmethod
from typing import Tuple


class Renderer(ABC):
    """
    Backend-agnostic rendering interface.

    ECS systems may call these methods.
    Backends (pygame, OpenGL, etc.) must implement them.
    """

    @abstractmethod
    def begin_frame(self) -> None:
        #Prepare the backend for a new frame.
        pass

    @abstractmethod
    def end_frame(self) -> None:
        #Present the rendered frame.
        pass

    @abstractmethod
    def draw_sprite(
        self,
        sprite_id: str,
        position: Tuple[float, float],
        rotation: float = 0.0,
        scale: Tuple[float, float] = (1.0, 1.0),
        alpha: float = 1.0,
    ) -> None:
        """
        Draw a sprite by logical ID.
        The backend decides how sprite_id is resolved.
        NOTE:
        This API is reserved for future asset-backed rendering.
        Current engine systems use draw_rect() for procedural rendering.
        """
        pass

    @abstractmethod
    def draw_rect(
            self,
            position: Tuple[float, float],
            size: Tuple[int, int],
            color: Tuple[int, int, int],
    ) -> None:
        pass

    @abstractmethod
    def draw_text(
            self,
            text: str,
            position: Tuple[int, int],
            color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        pass