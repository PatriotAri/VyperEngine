from engine.ecs.system_base import RenderSystem
from engine.debug.debug_config import DebugConfig
from engine.ecs.components.transform import Transform
from engine.core.clock import Clock
from engine.ports.input_state import InputState
from engine.core.camera import Camera

class DebugRenderSystem(RenderSystem):
    def __init__(self, renderer):
        self.renderer = renderer

    def render(self, world, alpha: float) -> None:
        debug: DebugConfig = world.get_resource(DebugConfig)
        if not debug or not debug.enabled:
            return

        clock: Clock = world.get_resource(Clock)
        #title
        y = 10
        self.renderer.draw_text("DEBUG MODE (F3)", (10, y))
        y += 20

        # FPS counter
        if clock:
            self.renderer.draw_text(f"FPS: {clock.fps}", (10, y))
            y += 20

        # current pressed key(s)
        input_state: InputState = world.get_resource(InputState)
        if input_state:
            self.renderer.draw_text(
                f"Keys pressed: {sorted(input_state.keys_down)}",
                (10, y),
            )
            y += 20

        #entity counter
        entities = list(world.entities_with())
        self.renderer.draw_text(f"Entity counter: [{len(entities)}]", (10, y))
        y += 20

        # camera position
        camera: Camera = world.get_resource(Camera)
        if camera:
            self.renderer.draw_text(
                f"Camera Position: x[{camera.x:.1f}], y[{camera.y:.1f}]",
                (10, y),
            )
            y += 20



        self.renderer.draw_text("Entity ID/Position:", (10, y))
        y += 20

        #lists entity locations
        for entity in entities:
            t = world.get_component(entity, Transform)
            if t:
                self.renderer.draw_text(
                    f"ID#: [{entity.id}] Coordinates: x[{t.x:.1f}], y[{t.y:.1f}]",
                    (10, y),
                )
                y += 20