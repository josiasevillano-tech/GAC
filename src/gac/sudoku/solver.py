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


# =====================================================
# SOLUCIONADOR LOGICO (naked singles + hidden singles)
#
# Estas son las dos tecnicas de escaneo mas basicas que
# usaria cualquier jugador principiante. Si un puzzle se
# puede resolver COMPLETO usando solo estas dos tecnicas,
# es un puzzle facil/medio sin importar cuantas pistas
# tenga visibles. Si el solucionador se queda "atascado"
# sin completar el tablero, el puzzle exige tecnicas mas
# avanzadas (o prueba y error) - eso es lo que realmente
# lo hace dificil para un jugador experto.
# =====================================================

def obtener_candidatos(grid, row, col):
    """
    Devuelve el conjunto de numeros que podrian ir en una
    celda vacia, segun lo que ya existe en su fila, columna
    y bloque de 3x3.
    """

    if grid[row][col] != 0:
        return set()

    posibles = set(range(1, 10))

    for c in range(9):
        posibles.discard(grid[row][c])

    for r in range(9):
        posibles.discard(grid[r][col])

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            posibles.discard(grid[r][c])

    return posibles


def _aplicar_naked_singles(grid):
    """
    Busca celdas que solo tienen UN candidato posible y las
    completa. Devuelve True si se completo alguna celda.
    """

    hubo_cambio = False

    for row in range(9):
        for col in range(9):

            if grid[row][col] == 0:

                candidatos = obtener_candidatos(grid, row, col)

                if len(candidatos) == 1:
                    grid[row][col] = candidatos.pop()
                    hubo_cambio = True

    return hubo_cambio


def _celdas_de_unidad(tipo, indice):
    """
    Devuelve la lista de coordenadas (fila, columna) que
    pertenecen a una unidad (fila, columna o bloque de 3x3).
    """

    if tipo == "fila":
        return [(indice, c) for c in range(9)]

    if tipo == "columna":
        return [(r, indice) for r in range(9)]

    # tipo == "bloque"
    box_row = (indice // 3) * 3
    box_col = (indice % 3) * 3

    return [
        (r, c)
        for r in range(box_row, box_row + 3)
        for c in range(box_col, box_col + 3)
    ]


def _aplicar_hidden_singles(grid):
    """
    Para cada unidad (fila, columna o bloque), revisa si algun
    numero del 1 al 9 solo puede colocarse en UNA celda vacia
    dentro de esa unidad, aunque esa celda tenga otros candidatos
    posibles ademas de ese numero. Si es asi, coloca ese numero.

    Devuelve True si se completo alguna celda.
    """

    hubo_cambio = False

    for tipo in ("fila", "columna", "bloque"):
        for indice in range(9):

            celdas = _celdas_de_unidad(tipo, indice)

            for num in range(1, 10):

                if any(grid[r][c] == num for r, c in celdas):
                    continue

                celdas_posibles = [
                    (r, c)
                    for r, c in celdas
                    if grid[r][c] == 0 and num in obtener_candidatos(grid, r, c)
                ]

                if len(celdas_posibles) == 1:
                    r, c = celdas_posibles[0]
                    grid[r][c] = num
                    hubo_cambio = True

    return hubo_cambio


def resolver_logico(grid):
    """
    Intenta resolver el sudoku usando SOLO naked singles e
    hidden singles (sin adivinar ni hacer backtracking).

    No modifica el grid original. Devuelve una tupla:
    (grid_resultante, resuelto_completamente: bool)
    """

    copia = [fila[:] for fila in grid]

    progreso = True

    while progreso:

        progreso = _aplicar_naked_singles(copia)
        progreso = _aplicar_hidden_singles(copia) or progreso

    resuelto = all(
        copia[r][c] != 0 for r in range(9) for c in range(9)
    )

    return copia, resuelto


def requiere_tecnicas_avanzadas(grid):
    """
    Devuelve True si el puzzle NO se puede resolver por
    completo usando solo naked singles e hidden singles, es
    decir, si exige tecnicas mas avanzadas o prueba y error.

    Esto es lo que realmente distingue un puzzle "experto"
    de uno que solo tiene pocas pistas pero sigue siendo
    mecanicamente facil de resolver.
    """

    _, resuelto = resolver_logico(grid)

    return not resuelto
