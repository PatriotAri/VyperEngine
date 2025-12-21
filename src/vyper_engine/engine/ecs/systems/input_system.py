import math

from vyper_engine.engine.ecs.system_base import UpdateSystem
from vyper_engine.engine.ecs.components.intent import MoveIntent
from vyper_engine.engine.ports.input_state import InputState
from vyper_engine.engine.ecs.components.transform import Transform
from vyper_engine.engine.ecs.components.player_controlled import PlayerControlled

class InputSystem(UpdateSystem):
    """
    Converts raw InputState into intent components.
    Intent is persistent state (updated every frame).
    """

    def update(self, world, dt: float) -> None:
        input_state: InputState = world.get_resource(InputState)
        if input_state is None:
            return

        dx = 0.0
        dy = 0.0

        if "w" in input_state.keys_down:
            dy -= 1.0
        if "s" in input_state.keys_down:
            dy += 1.0
        if "a" in input_state.keys_down:
            dx -= 1.0
        if "d" in input_state.keys_down:
            dx += 1.0

        #normalize diagonal intent so movement speed is consistent in all directions
        mag = math.hypot(dx, dy)
        if mag > 0.0:
            dx /= mag
            dy /= mag

        # Apply intent to player-controlled entities (always, even if zero)
        for entity in world.entities_with(Transform, PlayerControlled):
            existing = world.get_component(entity, MoveIntent)
            if existing is None:
                world.add_component(entity, MoveIntent(dx, dy))
            else:
                existing.x = dx
                existing.y = dy