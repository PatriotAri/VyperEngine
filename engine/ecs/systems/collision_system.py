from engine.ecs.system_base import FixedSystem
from engine.ecs.components.transform import Transform
from engine.ecs.components.collider import Collider
from engine.ecs.components.velocity import Velocity
from engine.ecs.components.rigidbody import RigidBody, BodyType


class CollisionSystem(FixedSystem):
    """
    Resolves AABB collisions with static vs dynamic body handling.
    """

    def update(self, world, dt: float) -> None:
        entities = list(world.entities_with(Transform, Collider))

        for i in range(len(entities)):
            a = entities[i]
            ta = world.get_component(a, Transform)
            ca = world.get_component(a, Collider)
            ra = world.get_component(a, RigidBody)

            for j in range(i + 1, len(entities)):
                b = entities[j]
                tb = world.get_component(b, Transform)
                cb = world.get_component(b, Collider)
                rb = world.get_component(b, RigidBody)

                dx = tb.x - ta.x
                dy = tb.y - ta.y

                overlap_x = (ca.half_width + cb.half_width) - abs(dx)
                overlap_y = (ca.half_height + cb.half_height) - abs(dy)

                if overlap_x <= 0 or overlap_y <= 0:
                    continue

                # Determine resolution axis
                if overlap_x < overlap_y:
                    axis = "x"
                    push = overlap_x if dx > 0 else -overlap_x
                else:
                    axis = "y"
                    push = overlap_y if dy > 0 else -overlap_y

                self._resolve(world, a, b, ta, tb, ra, rb, push, axis)

    def _resolve(self, world, a, b, ta, tb, ra, rb, push, axis):
        # Default missing rigidbody = static
        type_a = ra.body_type if ra else BodyType.STATIC
        type_b = rb.body_type if rb else BodyType.STATIC

        if type_a == BodyType.DYNAMIC and type_b == BodyType.STATIC:
            self._move(ta, -push, axis)
            self._zero_velocity(world, a, axis)

        elif type_a == BodyType.STATIC and type_b == BodyType.DYNAMIC:
            self._move(tb, push, axis)
            self._zero_velocity(world, b, axis)

        elif type_a == BodyType.DYNAMIC and type_b == BodyType.DYNAMIC:
            self._move(ta, -push / 2, axis)
            self._move(tb, push / 2, axis)
            self._zero_velocity(world, a, axis)
            self._zero_velocity(world, b, axis)

        # static vs static → do nothing

    def _move(self, transform, amount, axis):
        if axis == "x":
            transform.x += amount
        else:
            transform.y += amount

    def _zero_velocity(self, world, entity, axis):
        vel = world.get_component(entity, Velocity)
        if vel:
            if axis == "x":
                vel.vx = 0.0
            else:
                vel.vy = 0.0
