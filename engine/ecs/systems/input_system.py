from engine.ecs.system_base import UpdateSystem
from engine.ecs.components.intent import MoveIntent
from engine.ports.input_state import InputState
from engine.ecs.components.transform import Transform
from engine.ecs.components.player_controlled import PlayerControlled


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

        # Apply intent to player-controlled entities (always, even if zero)
        for entity in world.entities_with(Transform, PlayerControlled):
            existing = world.get_component(entity, MoveIntent)
            if existing is None:
                world.add_component(entity, MoveIntent(dx, dy))
            else:
                existing.x = dx
                existing.y = dy