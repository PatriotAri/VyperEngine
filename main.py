import os
import sys

# main.py is interactive-only and requires a visible display
if os.environ.get("SDL_VIDEODRIVER") == "dummy":
    print(
        "Error: main.py is intended for interactive, windowed runs only.\n"
        "Detected SDL_VIDEODRIVER=dummy (headless environment).\n\n"
        "For CI, automation, or Codex runs, use:\n"
        "  python tools/run_headless.py"
    )
    sys.exit(1)

from engine.core.engine import Engine
from engine.core.clock import Clock

from backends.pygame.window import PygameWindow
from backends.pygame.renderer import PygameRenderer

from engine.ecs.components.transform import Transform
from engine.ecs.components.sprite import Sprite
from engine.ecs.components.renderable import Renderable
from engine.ecs.components.camera_target import CameraTarget
from engine.ecs.components.player_controlled import PlayerControlled
from engine.ecs.components.velocity import Velocity

from engine.ecs.systems.input_system import InputSystem
from engine.ecs.systems.movement_system import MovementSystem
from engine.ecs.systems.basic_render_system import BasicRenderSystem
from engine.ecs.systems.camera_follow_system import CameraFollowSystem
from engine.ecs.systems.camera_update_system import CameraUpdateSystem
from engine.ecs.systems.physics_integrate_system import PhysicsIntegrateSystem

from engine.debug.debug_config import DebugConfig
from engine.debug.debug_toggle_system import DebugToggleSystem
from engine.debug.debug_render_system import DebugRenderSystem

def main():
    window = PygameWindow(size = (960, 540), title = "Vyper Engine")
    renderer = PygameRenderer()
    clock = Clock(fixed_dt = 1 / 60)
    engine = Engine(window = window, renderer = renderer, clock = clock)

    # --- Bootstrap test entity ---
    world = engine.get_world()
    test_entity = world.create_entity()
    world.add_component(test_entity, Transform(x=100.0, y=100.0))
    world.add_components(test_entity, Velocity())
    world.add_component(test_entity, Renderable())
    world.add_component(test_entity, CameraTarget())
    world.add_component(test_entity, Sprite(size=(32, 32), color=(200, 200, 200)))
    world.add_component(test_entity, PlayerControlled())
    #-----------------------------

    #order is input ->movement ->cameraFollow ->render

    #update systems(input, AI)
    engine.add_update_system(InputSystem())
    #fixed systems(movement, camera follow)
    engine.add_fixed_system(MovementSystem(speed = 100.0))
    engine.add_fixed_system(PhysicsIntegrateSystem())
    engine.add_fixed_system(CameraFollowSystem())
    engine.add_fixed_system(CameraUpdateSystem())
    #render systems (world -> screen)
    engine.add_render_system(BasicRenderSystem(renderer, window))

    world.add_resource(DebugConfig())

    engine.add_update_system(DebugToggleSystem())
    engine.add_render_system(DebugRenderSystem(renderer))

    engine.run()

if __name__ == "__main__":
    main()