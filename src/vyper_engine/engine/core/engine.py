from vyper_engine.engine.core.clock import Clock
from vyper_engine.engine.ports.window import Window
from vyper_engine.engine.ports.renderer import Renderer
from vyper_engine.engine.ports.input_state import InputState

from vyper_engine.engine.ecs.world import World
from vyper_engine.engine.ecs.system_base import FixedSystem, UpdateSystem, RenderSystem
from vyper_engine.engine.ecs.read_only_world import ReadOnlyWorld


DEFAULT_HEADLESS_FRAMES = 60


class Engine:
    """
    Core engine lifecycle controller.
    """

    def __init__(
        self,
        window: Window,
        renderer: Renderer,
        clock: Clock | None = None,
    ):
        self.window = window
        self.renderer = renderer
        self.clock = clock or Clock()

        self.input_state = InputState()
        self.world = World()
        self.world.add_resource(self.input_state)
        self.world.add_resource(self.clock)

        from vyper_engine.engine.core.camera import Camera
        self.camera = Camera()
        self.world.add_resource(self.camera)

        self.fixed_systems: list[FixedSystem] = []
        self.update_systems: list[UpdateSystem] = []
        self.render_systems: list[RenderSystem] = []

        self._running = False

    def run(self, max_frames: int | None = None) -> None:
        """
        Run the main engine loop.

        In headless mode, if no frame cap is provided,
        a default cap is applied to prevent infinite loops.
        """
        frame_count = 0

        # Headless safety
        is_headless = getattr(self.window, "is_headless", False)
        if is_headless and max_frames is None:
            max_frames = DEFAULT_HEADLESS_FRAMES
            print(
                f"[Engine] Headless mode detected, "
                f"defaulting to {DEFAULT_HEADLESS_FRAMES} frames"
            )

        self._running = True
        while self._running:
            self._tick()
            frame_count += 1

            if max_frames is not None and frame_count >= max_frames:
                self.stop()

    def stop(self) -> None:
        self._running = False

    def get_world(self) -> World:
        return self.world

    def add_fixed_system(self, system: FixedSystem):
        self.fixed_systems.append(system)

    def add_update_system(self, system: UpdateSystem):
        self.update_systems.append(system)

    def add_render_system(self, system: RenderSystem):
        self.render_systems.append(system)

    def _fixed_update(self, dt: float):
        """
        Fixed timestep update.
        ECS logic systems will run here later.
        """
        for system in self.fixed_systems:
            system.update(self.world, dt)

    def _update(self, dt: float):
        """
        Per-frame update (input, AI, non-deterministic logic).
        """
        for system in self.update_systems:
            system.update(self.world, dt)

    def _render(self, alpha: float) -> None:
        """
        Render step with interpolation.
        Render systems will run here later.
        """
        ro_world = ReadOnlyWorld(self.world)
        for system in self.render_systems:
            system.render(ro_world, alpha)

    def _tick(self) -> None:
        # 1. Reset per-frame input state
        self.input_state.begin_frame()

        # 2. Poll OS / backend events
        self.window.poll_events(self.input_state)

        # 3. Check for quit request
        if self.window.should_close() or self.input_state.quit_requested:
            self.stop()
            return

        # 4. Update clock (variable timestep)
        self.clock.tick()

        # 5. Variable update phase
        self._update(self.clock.dt)

        # 6. Fixed-step simulation
        while self.clock.should_step():
            self._fixed_update(self.clock.delta)
            self.clock.consume_step()

        # 7. Render
        self.renderer.begin_frame()
        self._render(self.clock.alpha())
        self.renderer.end_frame()
