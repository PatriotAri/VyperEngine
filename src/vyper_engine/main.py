"""
Vyper Engine main entrypoint.

Responsibilities:
- parse runtime intent (windowed vs headless)
- validate environment constraints
- construct the correct Window + Renderer
- start the Engine
"""

from __future__ import annotations

import argparse
import os

from vyper_engine.engine.ecs.systems.basic_render_system import BasicRenderSystem
from vyper_engine.engine.debug.debug_render_system import DebugRenderSystem
from vyper_engine.engine.debug.debug_toggle_system import DebugToggleSystem
from vyper_engine.engine.ecs.systems.input_system import InputSystem

from vyper_engine.engine.core.engine import Engine

# Windowed backend (pygame)
from vyper_engine.backends.pygame.window import PygameWindow
from vyper_engine.backends.pygame.renderer import PygameRenderer

# Headless backend (ports)
from vyper_engine.engine.ports.headless_window import HeadlessWindow
from vyper_engine.engine.ports.null_renderer import NullRenderer


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vyper", description="Vyper Engine runtime")

    parser.add_argument(
        "--mode",
        choices=("windowed", "headless"),
        default="windowed",
        help="Run mode (default: windowed)",
    )
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--title", type=str, default="Vyper Engine")

    parser.add_argument(
        "--frames",
        type=int,
        default=None,
        help="Optional frame limit (useful for headless runs). "
             "If omitted in headless mode, Engine defaults to 60 frames.",
    )

    return parser


def validate_windowed_environment() -> None:
    if os.environ.get("SDL_VIDEODRIVER") == "dummy":
        raise RuntimeError(
            "Windowed mode requested, but SDL_VIDEODRIVER=dummy.\n"
            "Unset SDL_VIDEODRIVER (or run with --mode headless).\n"
            "Example:\n"
            "  unset SDL_VIDEODRIVER\n"
            "  vyper\n"
        )


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    print("Vyper Engine")
    print(f"Mode: {args.mode}")

    if args.mode == "windowed":
        validate_windowed_environment()
        window = PygameWindow(size=(args.width, args.height), title=args.title)
        renderer = PygameRenderer()
        engine = Engine(window=window, renderer=renderer)

        # ----------------------------
        # Register systems (fact-based)
        # ----------------------------

        # Input must come first
        engine.add_update_system(InputSystem())

        # Debug toggle listens to input
        engine.add_update_system(DebugToggleSystem())

        # Rendering
        engine.add_render_system(BasicRenderSystem(renderer, window))
        engine.add_render_system(DebugRenderSystem(renderer))

        # Add debug configuration resource (REQUIRED)
        from vyper_engine.engine.debug.debug_config import DebugConfig
        engine.world.add_resource(DebugConfig())

        engine.run()

        return 0

    # headless
    window = HeadlessWindow()
    renderer = NullRenderer()
    engine = Engine(window=window, renderer=renderer)
    engine.run(max_frames=args.frames)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())