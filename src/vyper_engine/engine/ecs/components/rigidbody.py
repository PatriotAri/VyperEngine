from dataclasses import dataclass
from enum import Enum, auto


class BodyType(Enum):
    STATIC = auto()
    DYNAMIC = auto()


@dataclass
class RigidBody:
    """
    Defines how an entity participates in physics.
    """
    body_type: BodyType = BodyType.DYNAMIC