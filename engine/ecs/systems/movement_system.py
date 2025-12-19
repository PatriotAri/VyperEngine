from engine.ecs.system_base import FixedSystem
from engine.ecs.components.transform import Transform
from engine.ecs.components.intent import MoveIntent

class MovementSystem(FixedSystem):
    """
        Applies movement intent to transforms.
        Runs at a fixed timestep for deterministic simulation.
        """
    def __init__(self, speed: float = 100.0):
        #units per second
        self.speed = speed

    def update(self, world, dt: float) -> None:
        for entity in world.entities_with(Transform, MoveIntent):
            transform = world.get_component(entity, Transform)
            intent = world.get_component(entity, MoveIntent)

            #Apply movement
            transform.x += intent.x * self.speed * dt
            transform.y += intent.y * self.speed * dt

            #consume intent (intent is one-frame / one-tick)
            world.remove_component(entity, MoveIntent)