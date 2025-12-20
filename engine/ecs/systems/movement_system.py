from engine.ecs.system_base import FixedSystem
from engine.ecs.components.velocity import Velocity
from engine.ecs.components.intent import MoveIntent


class MovementSystem(FixedSystem):
    """
    Converts MoveIntent into Velocity.

    Runs at a fixed timestep.
    Does NOT integrate position.
    """

    def __init__(self, speed: float = 100.0):
        self.speed = speed

    def update(self, world, dt: float) -> None:
        for entity in world.entities_with(Velocity, MoveIntent):
            vel = world.get_component(entity, Velocity)
            intent = world.get_component(entity, MoveIntent)

            # Velocity is derived directly from intent
            vel.vx = intent.x * self.speed
            vel.vy = intent.y * self.speed