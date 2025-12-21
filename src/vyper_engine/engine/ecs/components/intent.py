from dataclasses import dataclass

@dataclass
class MoveIntent:
    """
    High-level movement intent.
    Values are normalized (-1.0 to 1.0).
    """
    x: float = 0.0
    y: float = 0.0