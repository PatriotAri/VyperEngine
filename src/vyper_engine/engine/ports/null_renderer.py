from vyper_engine.engine.ports.renderer import Renderer


class NullRenderer(Renderer):
    """
    Renderer for headless / CI runs.
    Performs no rendering.
    """

    def begin_frame(self) -> None:
        pass

    def end_frame(self) -> None:
        pass

    def draw_sprite(self, *args, **kwargs) -> None:
        pass

    def draw_rect(self, *args, **kwargs) -> None:
        pass

    def draw_text(self, *args, **kwargs) -> None:
        pass