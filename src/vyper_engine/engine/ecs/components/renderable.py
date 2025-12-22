from dataclasses import dataclass
from typing import Tuple

@dataclass
class Renderable:
    """
        Marks an entity as renderable.

        For now this is a simple rectangle.
        Later this can evolve into sprites, meshes, etc.
        """
    size: Tuple[int, int] = (32, 32)
    color: Tuple[int, int, int] = (200, 200, 255)