from collections import defaultdict
from typing import Type, TypeVar, Dict, Iterable
from .entity import Entity

T = TypeVar("T")


class World:
    """
    ECS World.

    Owns all entities and their components.
    Provides methods to create entities and
    attach/query component data.
    """

    def __init__(self):
        self._next_entity_id: int = 0
        self._components: Dict[Type, Dict[Entity, object]] = defaultdict(dict)
        # Singleton ECS resources (input, time, config, etc.)
        self._resources: dict[type, object] = {}

    # ---------- Entity management ----------

    def create_entity(self) -> Entity:
        entity = Entity(self._next_entity_id)
        self._next_entity_id += 1
        return entity

    def destroy_entity(self, entity: Entity) -> None:
        """
        Remove an entity and all of its components from the world.
        """
        for component_map in self._components.values():
            component_map.pop(entity, None)

    # ---------- Component management ----------

    def add_component(self, entity: Entity, component: object) -> None:
        self._components[type(component)][entity] = component

    def remove_component(self, entity: Entity, component_type: Type[T]) -> None:
        self._components[component_type].pop(entity, None)

    def get_component(self, entity: Entity, component_type: Type[T]) -> T | None:
        return self._components[component_type].get(entity)

    def has_component(self, entity: Entity, component_type: Type) -> bool:
        return entity in self._components[component_type]

    # ---------- Resource management ----------

    def add_resource(self, resource: object) -> None:
        # Add or replace a singleton resource.
        self._resources[type(resource)] = resource

    def get_resource(self, resource_type: type):
        # Retrieve a singleton resource by type.
        return self._resources.get(resource_type)

    # ---------- Queries ----------

    def entities_with(self, *component_types: Type) -> Iterable[Entity]:
        if not component_types:
            # All entities = union of all component owners
            all_entities = set()
            for entity_map in self._components.values():
                all_entities.update(entity_map.keys())
            return all_entities

        component_maps = [self._components[ctype] for ctype in component_types]
        smallest = min(component_maps, key=len)


        return [
            entity
            for entity in smallest
            if all(entity in comp for comp in component_maps)
        ]
