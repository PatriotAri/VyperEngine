from engine.ecs.system_base import UpdateSystem
from engine.ecs.components.intent import MoveIntent
from engine.ports.input_state import InputState
from engine.ecs.components.transform import Transform
from engine.ecs.components.player_controlled import PlayerControlled
class InputSystem(UpdateSystem):
    """
    Converts raw InputState into intent components.
    """

    def update(self, world, dt: float) -> None:
        input_state: InputState = world.get_resource(InputState)
        if input_state is None:
            return

        # Example: WASD movement
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

        if dx == 0.0 and dy == 0.0:
            return

        # For now: apply intent to all entities (we'll filter later)
        for entity in world.entities_with(Transform, PlayerControlled):
            world.add_component(entity, MoveIntent(dx, dy))