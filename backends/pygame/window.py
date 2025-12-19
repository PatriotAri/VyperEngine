import pygame

from engine.ports.window import Window
from engine.ports.input_state import InputState


class PygameWindow(Window):
    def __init__(self, size: tuple[int, int] = (800, 600), title: str = "Vyper Engine"):
        pygame.init()

        self._size = size
        self._surface = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

        self._should_close = False

    def poll_events(self, input_state: InputState) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._should_close = True
                input_state.quit_requested = True

            elif event.type == pygame.WINDOWFOCUSLOST:
                input_state.has_focus = False

            elif event.type == pygame.WINDOWFOCUSGAINED:
                input_state.has_focus = True

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                input_state.keys_down.add(key)
                input_state.keys_pressed.add(key)

            elif event.type == pygame.KEYUP:
                key = pygame.key.name(event.key)
                input_state.keys_down.discard(key)
                input_state.keys_released.add(key)

    def should_close(self) -> bool:
        return self._should_close

    def get_size(self) -> tuple[int, int]:
        return self._size

    def set_title(self, title: str) -> None:
        pygame.display.set_caption(title)