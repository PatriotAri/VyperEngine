from vyper_engine.engine.ports.window import Window
from vyper_engine.engine.ports.input_state import InputState


class HeadlessWindow(Window):
    """
    Window implementation for headless / CI runs.

    This window never emits events and never requests close.
    The engine is expected to terminate via a frame cap.
    """

    def __init__(self):
        self.is_headless = True

    def poll_events(self, input_state: InputState) -> None:
        # No events in headless mode
        pass

    def should_close(self) -> bool:
        return False

    def get_size(self):
        # No real framebuffer
        return (0, 0)

    def set_title(self, title: str) -> None:
        pass