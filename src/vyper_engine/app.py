from __future__ import annotations

from vyper_engine.engine.core.engine import Engine
from vyper_engine.scenes.base import Scene


class Application:
    """
    Composition root for runtime content.

    Owns:
    - loading a scene
    - registering systems/resources/entities for that scene

    Does NOT own:
    - CLI args
    - window/renderer creation
    - engine loop
    """

    def __init__(self, engine: Engine):
        self.engine = engine
        self._scene: Scene | None = None

    def load_scene(self, scene: Scene) -> None:
        if self._scene is not None:
            self._scene.on_exit(self.engine, self.engine.world)

        self._scene = scene
        self._scene.on_enter(self.engine, self.engine.world)
