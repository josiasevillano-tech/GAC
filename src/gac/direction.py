from enum import Enum


class Direction(Enum):
    """
    Representa las direcciones permitidas para colocar una palabra.
    """

    HORIZONTAL = (0, 1)
    VERTICAL = (1, 0)