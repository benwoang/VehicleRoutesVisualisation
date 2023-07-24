from abc import ABC, abstractmethod
from typing import Sequence
from matplotlib.patches import RegularPolygon
from solution_visualiser import COLORS
from cmath import pi


class TaskShape(ABC, RegularPolygon):
    # Task Properties
    RADIUS = 0.35
    NUM_VERTICES = 3
    EDGE_COLOUR = "black"
    BORDER_WIDTH = 0.3
    ALPHA = 1.0

    # Task Text Properties
    TEXT_FONTSIZE = 1.6
    HORIZONTAL_TEXT_ALIGNMENT, VERTICAL_TEXT_ALIGNMENT = "center"
    FONT_FAMILY = "Helvetica Neue"


class PickupShape(TaskShape):
    # Pickup
    __X_OFFSET = 0.5
    __Y_OFFSET = 0.56
    __ORIENTATION = pi
    TEXT_X_OFFSET = 0.49
    TEXT_Y_OFFSET = 0.56

    def __init__(self, xy: Sequence[float], numVertices: int) -> None:
        super().__init__(xy, numVertices, radius, orientation, **kwargs)


class DeliveryShape(TaskShape):
    # Delivery
    __X_OFFSET = 0.5
    __Y_OFFSET = 0.43
    __ORIENTATION = 0
    TEXT_X_OFFSET = 0.49
    TEXT_Y_OFFSET = 0.45

    def __init__(self, xy: Sequence[float]) -> None:
        super().__init__(xy, numVertices, radius, orientation, **kwargs)
