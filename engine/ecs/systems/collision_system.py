from engine.ecs.system_base import FixedSystem
from engine.ecs.components.transform import Transform
from engine.ecs.components.collider import Collider
from engine.ecs.components.velocity import Velocity
from engine.ecs.components.rigidbody import RigidBody, BodyType


_EPS = 1e-6  # helps avoid tiny jitter / re-penetration due to float noise


class CollisionSystem(FixedSystem):
    """
    Phase 4: Axis-separated AABB resolution.

    We resolve X penetration first, then Y penetration.
    This improves sliding, reduces corner snagging, and eliminates micro-gaps.
    """

    def update(self, world, dt: float) -> None:
        entities = list(world.entities_with(Transform, Collider))

        for i in range(len(entities)):
            a = entities[i]
            ta = world.get_component(a, Transform)
            ca = world.get_component(a, Collider)
            va = world.get_component(a, Velocity)
            ra = world.get_component(a, RigidBody)

        for j in range(i + 1, len(entities)):
            b = entities[j]
            tb = world.get_component(b, Transform)
            cb = world.get_component(b, Collider)
            vb = world.get_component(b, Velocity)
            rb = world.get_component(b, RigidBody)

            dx = tb.x - ta.x
            dy = tb.y - ta.y

            overlap_x = (ca.half_width + cb.half_width) - abs(dx)
            overlap_y = (ca.half_height + cb.half_height) - abs(dy)

            if overlap_x <= 0 or overlap_y <= 0:
                continue

            # NEW: choose a single axis to resolve
            axis = self._choose_axis(va, vb, overlap_x, overlap_y)

            if axis == "x":
                push = overlap_x if dx > 0 else -overlap_x
            else:
                push = overlap_y if dy > 0 else -overlap_y

            self._resolve_pair(world, a, b, ta, tb, ra, rb, push, axis)

    def _choose_axis(self, va, vb, overlap_x, overlap_y) -> str:
    
   

        vx = (va.vx if va else 0.0) - (vb.vx if vb else 0.0)
        vy = (va.vy if va else 0.0) - (vb.vy if vb else 0.0)

        if abs(vx) > abs(vy):
            return "x"
        if abs(vy) > abs(vx):
            return "y"

        # Fallback: smaller penetration
        return "x" if overlap_x < overlap_y else "y"

    def _resolve_pair(self, world, a, b, ta, tb, ra, rb, push: float, axis: str) -> None:
        # Default missing rigidbody = STATIC
        type_a = ra.body_type if ra else BodyType.STATIC
        type_b = rb.body_type if rb else BodyType.STATIC

        # Clamp into contact by moving bodies exactly by penetration amount (+ tiny eps)
        # eps keeps them from re-penetrating immediately due to float error.
        if type_a == BodyType.DYNAMIC and type_b == BodyType.STATIC:
            self._move(ta, -push - self._signed_eps(push), axis)
            self._zero_velocity(world, a, axis)

        elif type_a == BodyType.STATIC and type_b == BodyType.DYNAMIC:
            self._move(tb, push + self._signed_eps(push), axis)
            self._zero_velocity(world, b, axis)

        elif type_a == BodyType.DYNAMIC and type_b == BodyType.DYNAMIC:
            half = push / 2.0
            self._move(ta, -half - self._signed_eps(half), axis)
            self._move(tb, half + self._signed_eps(half), axis)
            self._zero_velocity(world, a, axis)
            self._zero_velocity(world, b, axis)

        # STATIC vs STATIC: no move

    def _signed_eps(self, value: float) -> float:
        return _EPS if value >= 0 else -_EPS

    def _move(self, t: Transform, amount: float, axis: str) -> None:
        if axis == "x":
            t.x += amount
        else:
            t.y += amount

    def _zero_velocity(self, world, entity, axis: str) -> None:
        vel = world.get_component(entity, Velocity)
        if not vel:
            return
        if axis == "x":
            vel.vx = 0.0
        else:
            vel.vy = 0.0