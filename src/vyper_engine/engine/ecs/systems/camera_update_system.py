from vyper_engine.engine.ecs.system_base import FixedSystem
from vyper_engine.engine.core.camera import Camera


class CameraUpdateSystem(FixedSystem):
    """
    Smoothly moves the camera toward its target position.
    """

    def update(self, world, dt: float) -> None:
        camera: Camera = world.get_resource(Camera)
        if camera is None:
            return

        # Smoothly interpolate camera position toward target
        factor = 1.0 - pow(1.0 - camera.smoothing, dt * 60.0)

        camera.x += (camera.target_x - camera.x) * factor
        camera.y += (camera.target_y - camera.y) * factor
