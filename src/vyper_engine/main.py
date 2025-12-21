"""
Vyper Engine main entrypoint.

This file is responsible ONLY for:
- parsing runtime intent (windowed vs headless)
- validating environment constraints
- constructing the correct Window + Renderer
- starting the Engine

It does NOT:
- auto-detect CI
- silently change behavior
- exit early without explanation
"""

from __future__ import annotations

import argparse
import os
import sys

from vyper_engine.engine.engine import Engine

# Window / Renderer backends
from vyper_engine.backends.pygame.window import PygameWindow
from vyper_engine.backends.pygame.renderer import PygameRenderer
from vyper_engine.backends.headless.window import HeadlessWindow
from vyper_engine.backends.headless.renderer import NullRenderer


# ----------------------------
# Argument parsing
# ----------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vyper",
        description="Vyper Engine runtime"
    )

    parser.add_argument(
        "--mode",
        choices=("windowed", "headless"),
        default="windowed",
        help="Run mode (default: windowed)"
    )

    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--title", type=str, default="Vyper Engine")

    parser.add_argument(
        "--frames",
        type=int,
        default=None,
        help="Optional frame limit (useful for headless runs)"
    )

    return parser


# ----------------------------
# Environment validation
# ----------------------------

def validate_windowed_environment() -> None:
    """
    Ensure a windowed run is actually possible.
    """
    sdl_driver = os.environ.get("SDL_VIDEODRIVER")

    if sdl_driver == "dummy":
        raise RuntimeError(
            "\nWindowed mode requested, but SDL_VIDEODRIVER=dummy.\n\n"
            "This environment cannot create a window.\n\n"
            "Fix one of the following:\n"
            "  • Unset SDL_VIDEODRIVER\n"
            "  • Run with: --mode headless\n\n"
            "Example:\n"
            "  unset SDL_VIDEODRIVER\n"
            "  python -m vyper_engine.main\n"
        )


# ----------------------------
# Main bootstrap
# ----------------------------

def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    print("Vyper Engine")
    print(f"Mode: {args.mode}")

    # ------------------------
    # Windowed mode
    # ------------------------
    if args.mode == "windowed":
        validate_windowed_environment()

        window = PygameWindow(
            width=args.width,
            height=args.height,
            title=args.title,
        )
        renderer = PygameRenderer(window)

    # ------------------------
    # Headless mode
    # ------------------------
    else:
        window = HeadlessWindow()
        renderer = NullRenderer()

    engine = Engine(
        window=window,
        renderer=renderer,
    )

    # Optional frame cap (especially useful in CI)
    if args.frames is not None:
        engine.set_frame_cap(args.frames)

    engine.run()
    return 0


# ----------------------------
# Script entry
# ----------------------------

if __name__ == "__main__":
    raise SystemExit(main())
