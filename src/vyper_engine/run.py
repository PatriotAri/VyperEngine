from __future__ import annotations

import argparse
import os
import sys

from vyper_engine.runtime.mode import parse_mode, WINDOWED, HEADLESS
# Adjust these imports to match your actual class names/locations:
from vyper_engine.engine import Engine
from vyper_engine.backends.pygame.window import PygameWindow
from vyper_engine.backends.pygame.renderer import PygameRenderer
from vyper_engine.backends.headless.window import HeadlessWindow
from vyper_engine.backends.headless.renderer import NullRenderer


def _env_constraints_summary() -> str:
    parts = []
    sdl = os.environ.get("SDL_VIDEODRIVER")
    if sdl:
        parts.append(f"SDL_VIDEODRIVER={sdl}")
    disp = os.environ.get("DISPLAY")
    if disp:
        parts.append(f"DISPLAY={disp}")
    return ", ".join(parts) if parts else "(none)"


def _validate_windowed_is_possible() -> None:
    # SDL_VIDEODRIVER=dummy means "no window surface possible"
    if os.environ.get("SDL_VIDEODRIVER") == "dummy":
        raise RuntimeError(
            "Windowed mode requested, but SDL_VIDEODRIVER=dummy.\n"
            "Unset SDL_VIDEODRIVER (or set it to a real backend like x11/windows/cocoa),\n"
            "or run with --mode headless.\n"
            f"Env constraints: {_env_constraints_summary()}"
        )


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vyper", description="Vyper Engine runner")
    p.add_argument(
        "--mode",
        default="windowed",
        help="Run mode: windowed | headless (default: windowed)",
    )
    # Optional: allow overriding a frame cap for headless runs
    p.add_argument("--frames", type=int, default=None, help="Optional frame cap")
    # Optional: allow configuring window
    p.add_argument("--width", type=int, default=1280)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--title", type=str, default="Vyper Engine")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    mode = parse_mode(args.mode)

    print("Vyper Engine")
    print(f"Mode: {mode.name}")
    print(f"Env constraints: {_env_constraints_summary()}")

    if mode is WINDOWED:
        _validate_windowed_is_possible()
        window = PygameWindow(width=args.width, height=args.height, title=args.title)
        renderer = PygameRenderer(window)
    else:
        window = HeadlessWindow()
        renderer = NullRenderer()

    engine = Engine(window=window, renderer=renderer)

    # If your Engine supports it, apply frame cap here:
    if args.frames is not None:
        engine.set_frame_cap(args.frames)  # only if you have this; otherwise remove

    engine.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())