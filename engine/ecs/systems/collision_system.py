from engine.ecs.system_base import FixedSystem
from engine.ecs.components.transform import Transform
from engine.ecs.components.collider import Collider
from engine.ecs.components.velocity import Velocity
from engine.ecs.components.rigidbody import RigidBody, BodyType

_EPS = 1e-6  # helps avoid tiny jitter / re-penetration due to float noise


class CollisionSystem(FixedSystem):
    """
    Phase 4: Axis-separated AABB resolution.

    Collisions are resolved along the axis with the minimum penetration
    (minimum translation vector).
    """

    def update(self, world, dt: float) -> None:
        entities = list(world.entities_with(Transform, Collider, RigidBody))

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

                # Skip static-static collisions
                if ra.body_type == BodyType.STATIC and rb.body_type == BodyType.STATIC:
                    continue

                dx = tb.x - ta.x
                dy = tb.y - ta.y

                overlap_x = (ca.half_width + cb.half_width) - abs(dx)
                if overlap_x <= 0:
                    continue

                overlap_y = (ca.half_height + cb.half_height) - abs(dy)
                if overlap_y <= 0:
                    continue

                # Resolve along minimum penetration axis
                if overlap_x < overlap_y:
                    self._resolve_x(world, a, b, dx, overlap_x)
                else:
                    self._resolve_y(world, a, b, dy, overlap_y)

    def _resolve_x(self, world, a, b, dx: float, overlap: float) -> None:
        ta = world.get_component(a, Transform)
        tb = world.get_component(b, Transform)
        ra = world.get_component(a, RigidBody)
        rb = world.get_component(b, RigidBody)

        sep = overlap + _EPS
        if dx > 0:
            sep = -sep

        if ra.body_type == BodyType.DYNAMIC:
            ta.x += sep
            va = world.get_component(a, Velocity)
            va.vx = 0.0

        if rb.body_type == BodyType.DYNAMIC:
            tb.x -= sep
            vb = world.get_component(b, Velocity)
            if vb is not None:
                vb.vx = 0.0

    def _resolve_y(self, world, a, b, dy: float, overlap: float) -> None:
        ta = world.get_component(a, Transform)
        tb = world.get_component(b, Transform)
        ra = world.get_component(a, RigidBody)
        rb = world.get_component(b, RigidBody)

        sep = overlap + _EPS
        if dy > 0:
            sep = -sep

        if ra.body_type == BodyType.DYNAMIC:
            ta.y += sep
            va = world.get_component(a, Velocity)
            va.vy = 0.0

        if rb.body_type == BodyType.DYNAMIC:
            tb.y -= sep
            vb = world.get_component(b, Velocity)
            if vb is not None:
                vb.vy = 0.0