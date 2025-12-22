from vyper_engine.engine.ecs.system_base import UpdateSystem
from vyper_engine.engine.ports.input_state import InputState

from vyper_engine.app import Application
from vyper_engine.scenes.empty_scene import EmptyScene


class SceneSwitchSystem(UpdateSystem):
    """
    Temporary system to validate scene switching.
    """

    def __init__(self, app: Application):
        self.app = app

    def update(self, world, dt: float) -> None:
        input_state: InputState = world.get_resource(InputState)
        if not input_state:
            return

        # Press F1 to switch scenes
        if "f1" in input_state.keys_pressed:
            self.app.load_scene(EmptyScene())
