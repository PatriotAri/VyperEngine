from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

RunModeName = Literal["windowed", "headless"]

@dataclass(frozen=True)
class RunMode:
    name: RunModeName
    requires_display: bool

WINDOWED = RunMode(name="windowed", requires_display=True)
HEADLESS = RunMode(name="headless", requires_display=False)

def parse_mode(value: str | None) -> RunMode:
    if value is None:
        return WINDOWED
    value = value.strip().lower()
    if value in ("windowed", "win", "gui"):
        return WINDOWED
    if value in ("headless", "hl", "ci", "server"):
        return HEADLESS
    raise ValueError(f"Unknown mode: {value!r}. Use 'windowed' or 'headless'.")