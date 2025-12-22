from dataclasses import dataclass
from typing import Tuple

@dataclass
class Sprite:
    """
    Simple renderable marker component.
    """
    size: Tuple[int, int] = (32, 32)
    color: Tuple[int, int, int] = (200, 200, 200)