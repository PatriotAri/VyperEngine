from vyper_engine.engine.ecs.system_base import FixedSystem
from vyper_engine.engine.ecs.components.transform import Transform
from vyper_engine.engine.ecs.components.velocity import Velocity


class PhysicsIntegrateSystem(FixedSystem):
    """
    Integrates Velocity into Transform at a fixed timestep.
    """

    def update(self, world, dt: float) -> None:
        for entity in world.entities_with(Transform, Velocity):
            t = world.get_component(entity, Transform)
            v = world.get_component(entity, Velocity)

            t.x += v.vx * dt
            t.y += v.vy * dt