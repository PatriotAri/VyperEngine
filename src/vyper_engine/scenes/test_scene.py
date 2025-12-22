from __future__ import annotations

from vyper_engine.scenes.base import Scene
from vyper_engine.engine.core.engine import Engine
from vyper_engine.engine.ecs.world import World

# Resources
from vyper_engine.engine.core.camera import Camera
from vyper_engine.engine.debug.debug_config import DebugConfig

# Systems
from vyper_engine.engine.ecs.systems.input_system import InputSystem
from vyper_engine.engine.debug.debug_toggle_system import DebugToggleSystem
from vyper_engine.engine.debug.debug_render_system import DebugRenderSystem
from vyper_engine.engine.ecs.systems.basic_render_system import BasicRenderSystem
from vyper_engine.engine.ecs.systems.scene_switch_system import SceneSwitchSystem

# Components
from vyper_engine.engine.ecs.components.transform import Transform
from vyper_engine.engine.ecs.components.renderable import Renderable
from vyper_engine.engine.ecs.components.sprite import Sprite


class TestScene(Scene):
    """
    Minimal bring-up scene:
    - debug toggle + debug overlay
    - a single red square in the center of the world
    """

    def on_enter(self, engine: Engine, world: World) -> None:
        # Resources
        world.add_resource(DebugConfig())
        world.add_resource(Camera(x=0, y=0))

        # Systems
        engine.add_update_system(InputSystem())
        engine.add_update_system(DebugToggleSystem())

        # Render systems (note differing constructors)
        engine.add_render_system(BasicRenderSystem(engine.renderer, engine.window))
        engine.add_render_system(DebugRenderSystem(engine.renderer))

        # Entity: red square at world origin
        e = world.create_entity()
        world.add_component(e, Transform(x=0, y=0))
        world.add_component(e, Renderable())
        world.add_component(e, Sprite(size=(50, 50), color=(255, 0, 0)))
