import pygame

from vyper_engine.engine.ports.renderer import Renderer


class PygameRenderer(Renderer):
    def __init__(self, clear_color: tuple[int, int, int] = (30, 30, 30)):
        self.clear_color = clear_color
        self._surface = pygame.display.get_surface()

        if self._surface is None:
            raise RuntimeError(
                "Pygame display surface not initialized. "
                "Create a PygameWindow before the renderer."
            )

        self._font = pygame.font.SysFont("consolas", 16)

    def begin_frame(self) -> None:
        self._surface.fill(self.clear_color)

    def end_frame(self) -> None:
        pygame.display.flip()

    def draw_sprite(
        self,
        sprite_id: str,
        position: tuple[float, float],
        rotation: float = 0.0,
        scale: tuple[float, float] = (1.0, 1.0),
        alpha: float = 1.0,
    ) -> None:
        # Not implemented yet (intentionally)
        pass

    def draw_rect(self, position, size, color) -> None:
        rect = pygame.Rect(
            int(position[0]),
            int(position[1]),
            size[0],
            size[1],
        )
        pygame.draw.rect(self._surface, color, rect)

    def draw_text(
        self,
        text: str,
        position: tuple[int, int],
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        surface = self._font.render(text, True, color)
        self._surface.blit(surface, position)
