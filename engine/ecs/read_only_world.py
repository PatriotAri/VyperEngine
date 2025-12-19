from typing import Type, Iterable
from engine.ecs.entity import Entity


class ReadOnlyWorld:
    """
    Read-only view of the ECS World.
    Used by RenderSystems to prevent mutation.
    """

    def __init__(self, world):
        self._world = world

    # ----- Safe read operations -----
    def get_component(self, entity: Entity, component_type: Type):
        return self._world.get_component(entity, component_type)

    def get_resource(self, resource_type: Type):
        return self._world.get_resource(resource_type)

    def entities_with(self, *component_types: Type) -> Iterable[Entity]:
        return self._world.entities_with(*component_types)
