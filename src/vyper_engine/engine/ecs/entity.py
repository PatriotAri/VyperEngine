from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Entity:
    """
    Opaque entity identifier.

    Entities contain no logic and no data.
    They are used solely as stable IDs
    for indexing components in the World.
    """
    id: int
