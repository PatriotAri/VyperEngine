from __future__ import annotations
from abc import ABC, abstractmethod

from vyper_engine.engine.ecs.world import World
from vyper_engine.engine.core.engine import Engine


class Scene(ABC):
    """
    A Scene owns content lifecycle:
    - create entities/resources/systems needed for this scene
    - optionally tear them down

    Scenes do NOT create windows/renderers or run the engine loop.
    """

    @abstractmethod
    def on_enter(self, app, engine: Engine, world: World) -> None:
        ...

    def on_exit(self, app, engine: Engine, world: World) -> None:
        # Optional: cleanup if/when you add scene switching
        pass
