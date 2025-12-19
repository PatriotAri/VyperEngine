# engine/ecs/components/transform.py
from dataclasses import dataclass

@dataclass
class Transform:
    x: float = 0.0
    y: float = 0.0