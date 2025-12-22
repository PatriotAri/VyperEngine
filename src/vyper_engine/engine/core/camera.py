from dataclasses import dataclass

@dataclass
class Camera:
    """
    World-space camera.

    - (x, y)        : current camera position
    - (target_x, target_y): desired camera position
    - smoothing     : how fast the camera approaches its target (0..1)
    - zoom          : render scale (future use)
    """
    x: float = 0.0
    y: float = 0.0

    target_x: float = 0.0
    target_y: float = 0.0

    smoothing: float = 0.15
    zoom: float = 1.0
