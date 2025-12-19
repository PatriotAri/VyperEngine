from engine.ecs.system_base import RenderSystem

from engine.ecs.components.transform import Transform
from engine.ecs.components.renderable import Renderable
from engine.ecs.components.sprite import Sprite

from engine.core.camera import Camera

class BasicRenderSystem(RenderSystem):
    """
    Renders sprites with camera offset.
    """

    def __init__(self, renderer, window):
        self.renderer = renderer
        self.window = window

    def render(self, world, alpha: float) -> None:
        camera: Camera = world.get_resource(Camera)
        if camera is None:
            return

        screen_w, screen_h = self.window.get_size()
        cx = screen_w // 2
        cy = screen_h // 2

        for entity in world.entities_with(Transform, Renderable, Sprite):
            transform = world.get_component(entity, Transform)
            sprite = world.get_component(entity, Sprite)

            # World → screen
            screen_x = (transform.x - camera.x) + cx
            screen_y = (transform.y - camera.y) + cy

            half_w = sprite.size[0] // 2
            half_h = sprite.size[1] // 2

            self.renderer.draw_rect(
                position=(screen_x - half_w, screen_y - half_h),
                size=sprite.size,
                color=sprite.color,
            )