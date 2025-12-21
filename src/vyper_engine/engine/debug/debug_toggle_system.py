from vyper_engine.engine.ecs.system_base import UpdateSystem
from vyper_engine.engine.ports.input_state import InputState
from vyper_engine.engine.debug.debug_config import DebugConfig


class DebugToggleSystem(UpdateSystem):
    def update(self, world, dt: float) -> None:
        input_state: InputState = world.get_resource(InputState)
        debug: DebugConfig = world.get_resource(DebugConfig)

        if not input_state or not debug:
            return

        if "f3" in input_state.keys_pressed:
            debug.enabled = not debug.enabled