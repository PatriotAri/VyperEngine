from dataclasses import dataclass


@dataclass
class Collider:
    """
    Axis-aligned bounding box (AABB) collider.

    The collider is centered on the entity's Transform position.
    half_width / half_height define the extents.
    """
    half_width: float
    half_height: float