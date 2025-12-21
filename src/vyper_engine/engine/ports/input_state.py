#input_state.py
from typing import Set, Tuple
#Backend-agnostic event and input state container.
#This class holds all per-frame input and window state
#that systems may query during an update step.
class InputState:
    __slots__ = (
        "quit_requested",
        "has_focus",
        "keys_down",
        "keys_pressed",
        "keys_released",
        "mouse_buttons_down",
        "mouse_buttons_pressed",
        "mouse_buttons_released",
        "mouse_pos",
        "mouse_delta",
        "mouse_wheel_delta",
        "text_input",
    )
    def __init__(self):
        # Window state
        self.quit_requested: bool = False
        # Prevents stuck keys while alt-tabbing, allows safe input pause
        self.has_focus: bool = True
        # Keyboard state
        self.keys_down: Set[str] = set()
        self.keys_pressed: Set[str] = set()
        self.keys_released: Set[str] = set()
        # Mouse buttons
        self.mouse_buttons_down: Set[int] = set()
        self.mouse_buttons_pressed: Set[int] = set()
        self.mouse_buttons_released: Set[int] = set()
        # Mouse motion
        self.mouse_pos: Tuple[int, int] = (0, 0)
        self.mouse_delta: Tuple[int, int] = (0, 0)
        # Mouse wheel
        self.mouse_wheel_delta: int = 0
        # Text input
        self.text_input: str = ""

    def begin_frame(self):
        """
        Reset all one-frame event state.

        Must be called exactly once per frame,
        before any backend fills input data.
        """
        self.quit_requested = False
        self.text_input = ""

        self.keys_pressed.clear()
        self.keys_released.clear()
        self.mouse_buttons_pressed.clear()
        self.mouse_buttons_released.clear()

        self.mouse_delta = (0, 0)
        self.mouse_wheel_delta = 0