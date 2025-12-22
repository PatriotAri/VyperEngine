# src/vyper_engine/game.py

from vyper_engine.engine.core.engine import Engine
#movement and physics
from vyper_engine.engine.ecs.systems.movement_system import MovementSystem
from vyper_engine.engine.ecs.systems.physics_integrate_system import PhysicsIntegrateSystem

# Components/camera
from vyper_engine.engine.ecs.components.transform import Transform
from vyper_engine.engine.ecs.components.renderable import Renderable
from vyper_engine.engine.ecs.components.sprite import Sprite
from vyper_engine.engine.core.camera import Camera
from vyper_engine.engine.ecs.entity import Entity

# Systems
from vyper_engine.engine.ecs.systems.input_system import InputSystem
from vyper_engine.engine.debug.debug_toggle_system import DebugToggleSystem
from vyper_engine.engine.ecs.systems.basic_render_system import BasicRenderSystem
from vyper_engine.engine.debug.debug_render_system import DebugRenderSystem

# Resources
from vyper_engine.engine.debug.debug_config import DebugConfig


class Game:
    """
    Game bootstrap.

    Responsible for:
    - registering systems
    - registering world resources
    - defining the initial runtime composition

    Not responsible for:
    - window creation
    - renderer creation
    - engine loop
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    def setup(self) -> None:
        world = self.engine.world

        # ----------------------------
        # Resources
        # ----------------------------
        world.add_resource(DebugConfig())

        # ----------------------------
        # Update systems
        # ----------------------------
        self.engine.add_update_system(InputSystem())
        self.engine.add_update_system(DebugToggleSystem())

        # ----------------------------
        # Movement and Physics systems
        # ----------------------------
        self.engine.add_fixed_system(MovementSystem())
        self.engine.add_fixed_system(PhysicsIntegrateSystem())

        # ----------------------------
        # Render systems
        # ----------------------------
        renderer = self.engine.renderer
        window = self.engine.window

        self.engine.add_render_system(
            BasicRenderSystem(renderer, window)
        )
        self.engine.add_render_system(
            DebugRenderSystem(renderer)
        )

        #entity spawn test
        self.spawn_test_entity()
    
    def spawn_test_entity(self) -> None:
        world = self.engine.world

        # Camera resource (REQUIRED for rendering)
        world.add_resource(Camera(x=0, y=0))

        # Create entity
        entity = world.create_entity()

        # Components required by BasicRenderSystem
        world.add_component(entity, Transform(x=0, y=0))
        world.add_component(entity, Renderable())
        world.add_component(entity, Sprite(size=(50, 50), color=(255, 0, 0)))