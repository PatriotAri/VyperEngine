# clock.py
import time
#optimizes for ECS
class Clock:
    __slots__ = (
        "delta",          # fixed timestep (user-set)
        "dt",             # variable delta
        "accumulator",    # stores leftover time for fixed updates
        "fps",            # current frames per second
        "_last",       # last frame timestamp
        "_fps_counter",
        "_fps_timer",
    )

    def __init__(self, fixed_dt: float = 1/60):
        self.delta = fixed_dt
        self.dt = 0.0
        self.accumulator = 0.0

        self.fps = 0
        self._last = time.perf_counter()
        self._fps_counter = 0
        self._fps_timer = 0.0

    def tick(self):
        #Update dt, accumulator, fps.
        now = time.perf_counter()
        self.dt = now - self._last
        self._last = now

        self.accumulator += self.dt
        #prevents spiral of death (recursive lag spike and crash)
        if self.accumulator > self.delta * 5:
            self.accumulator = self.delta * 5
        # FPS logic
        self._fps_counter += 1
        self._fps_timer += self.dt

        if self._fps_timer >= 1.0:
            self.fps = self._fps_counter
            self._fps_counter = 0
            self._fps_timer = 0.0
    #returns true if time for a fixed update
    def should_step(self):
        return self.accumulator > self.delta
    #removes used accumulated time preventing overflow in delta time
    def consume_step(self):
        self.accumulator -= self.delta
    #Interpolation factor for rendering (0.0 -> 1.0)
    def alpha(self):
        return self.accumulator / self.delta