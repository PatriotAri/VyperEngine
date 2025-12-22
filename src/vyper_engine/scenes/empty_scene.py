from __future__ import annotations

from vyper_engine.scenes.base import Scene
from vyper_engine.engine.core.engine import Engine
from vyper_engine.engine.ecs.world import World


class EmptyScene(Scene):
    """
    Empty scene used to validate scene switching.
    """

    def on_enter(self, engine: Engine, world: World) -> None:
        print("Entered EmptyScene")