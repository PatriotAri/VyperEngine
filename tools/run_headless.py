from engine.core.engine import Engine
from engine.core.clock import Clock
from engine.ports.headless_window import HeadlessWindow
from backends.pygame.renderer import PygameRenderer


def main():
    window = HeadlessWindow()
    renderer = PygameRenderer()
    clock = Clock()

    engine = Engine(
        window=window,
        renderer=renderer,
        clock=clock,
    )

    # Default headless frame cap applies (60 frames)
    engine.run()


if __name__ == "__main__":
    main()