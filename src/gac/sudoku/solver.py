def es_valido(grid, row, col, num):
    """
    Verifica si colocar 'num' en (row, col) respeta las reglas
    del sudoku: no puede repetirse en la misma fila, columna,
    ni en el bloque de 3x3 al que pertenece la celda.
    """

    for c in range(9):
        if grid[row][c] == num:
            return False

    for r in range(9):
        if grid[r][col] == num:
            return False

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == num:
                return False

    return True


def encontrar_celda_vacia(grid):
    """
    Devuelve la primera celda vacia (fila, columna) encontrada,
    o None si el tablero ya esta completo.
    """

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col

    return None


def resolver(grid):
    """
    Resuelve el sudoku IN-PLACE usando backtracking.

    Devuelve True si encontro una solucion (el grid queda
    modificado con la solucion), False si no tiene solucion.
    """

    celda = encontrar_celda_vacia(grid)

    if celda is None:
        return True

    row, col = celda

    for num in range(1, 10):

        if es_valido(grid, row, col, num):

            grid[row][col] = num

            if resolver(grid):
                return True

            grid[row][col] = 0

    return False


def contar_soluciones(grid, limite=2):
    """
    Cuenta cuantas soluciones tiene un sudoku, deteniendose
    apenas se alcanza 'limite' (por defecto 2), ya que para
    verificar unicidad basta con saber si hay 1 o mas de 1.

    No modifica el grid original (trabaja sobre una copia).
    """

    copia = [fila[:] for fila in grid]

    return _contar_soluciones_recursivo(copia, limite)


def _contar_soluciones_recursivo(grid, limite):

    celda = encontrar_celda_vacia(grid)

    if celda is None:
        return 1

    row, col = celda
    total = 0

    for num in range(1, 10):

        if es_valido(grid, row, col, num):

            grid[row][col] = num

            total += _contar_soluciones_recursivo(grid, limite)

            grid[row][col] = 0

            if total >= limite:
                return total

    return total
