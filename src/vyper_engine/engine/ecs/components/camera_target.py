from dataclasses import dataclass

@dataclass
class CameraTarget:
    """
        Marks an entity as a camera follow target.
        Optional per-entity camera offset.
        """
    offset_x: float = 0.0
    offset_y: float = 0.0