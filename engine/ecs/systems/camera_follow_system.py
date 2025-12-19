from engine.ecs.system_base import FixedSystem
from engine.ecs.components.transform import Transform
from engine.ecs.components.camera_target import CameraTarget
from engine.core.camera import Camera

class CameraFollowSystem(FixedSystem):
    """
    Selects a camera target and updates the camera's desired position.
    Does NOT move the camera directly.
    """

    def update(self, world, dt: float) -> None:
        camera: Camera = world.get_resource(Camera)
        if camera is None:
            return

        for entity in world.entities_with(Transform, CameraTarget):
            transform = world.get_component(entity, Transform)
            camera.target_x = transform.x
            camera.target_y = transform.y

            # Follow only one entity (for now)
            break