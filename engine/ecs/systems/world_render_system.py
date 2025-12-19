from engine.ecs.system_base import RenderSystem
from engine.ecs.components.transform import Transform
from engine.ecs.components.sprite import Sprite
from engine.ports.renderer import Renderer


class WorldRenderSystem(RenderSystem):
    """
    Renders entities with Transform + Sprite.
    """

    def __init__(self, renderer: Renderer):
        self.renderer = renderer

    def render(self, world, alpha: float) -> None:
        for entity in world.entities_with(Transform, Sprite):
            transform = world.get_component(entity, Transform)
            sprite = world.get_component(entity, Sprite)

            self.renderer.draw_rect(
                position=(transform.x, transform.y),
                size=sprite.size,
                color=sprite.color,
            )