from typing import Protocol, Type, Iterable
from engine.ecs.entity import Entity

class WorldView(Protocol):
    """
    Read-only ECS world interface.
    """

    def get_component(self, entity: Entity, component_type: Type): ...
    def get_resource(self, resource_type: Type): ...
    def entities_with(self, *component_types: Type) -> Iterable[Entity]: ...
