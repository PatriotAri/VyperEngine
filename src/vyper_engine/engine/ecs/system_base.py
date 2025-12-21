from abc import ABC, abstractmethod
from vyper_engine.engine.ecs.world_view import WorldView

class FixedSystem(ABC):
    """
    Runs at a fixed timestep.
    Used for deterministic simulation.
    """

    @abstractmethod
    def update(self, world: WorldView, dt: float) -> None:
        pass


class UpdateSystem(ABC):
    """
    Runs once per frame.
    Used for input, AI, and non-deterministic logic.
    """

    @abstractmethod
    def update(self, world: WorldView, dt: float) -> None:
        pass


class RenderSystem(ABC):
    """
    Runs once per frame after simulation.
    Must not mutate world state.
    """

    @abstractmethod
    def render(self, world: WorldView, alpha: float) -> None:
        pass
