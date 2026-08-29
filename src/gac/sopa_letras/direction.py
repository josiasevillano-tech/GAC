from enum import Enum


class Direction(Enum):
    """
    Representa las 8 direcciones permitidas para colocar
    una palabra en una sopa de letras.

    Cada valor es una tupla (delta_fila, delta_columna).
    """

    HORIZONTAL = (0, 1)
    HORIZONTAL_INVERSA = (0, -1)
    VERTICAL = (1, 0)
    VERTICAL_INVERSA = (-1, 0)
    DIAGONAL_ABAJO_DERECHA = (1, 1)
    DIAGONAL_ABAJO_IZQUIERDA = (1, -1)
    DIAGONAL_ARRIBA_DERECHA = (-1, 1)
    DIAGONAL_ARRIBA_IZQUIERDA = (-1, -1)
