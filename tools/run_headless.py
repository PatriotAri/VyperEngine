from engine.core.engine import Engine
from engine.core.clock import Clock
from engine.ports.headless_window import HeadlessWindow
from engine.ports.null_renderer import NullRenderer


def main():
    window = HeadlessWindow()
    renderer = NullRenderer()
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