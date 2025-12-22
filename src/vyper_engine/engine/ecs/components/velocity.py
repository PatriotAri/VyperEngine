from dataclasses import dataclass


@dataclass
class Velocity:
    """
    Linear velocity in world units per second.
    """
    vx: float = 0.0
    vy: float = 0.0