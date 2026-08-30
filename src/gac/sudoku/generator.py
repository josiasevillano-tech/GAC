import random

from .solver import es_valido, resolver, contar_soluciones


class Generator:
    """
    Generador automatico de sudokus.

    Genera una cuadricula 9x9 completa y valida, y luego
    perfora celdas (las vacia) hasta alcanzar la cantidad de
    pistas visibles correspondiente al nivel de dificultad,
    garantizando en todo momento que el puzzle resultante
    tenga una unica solucion posible.
    """

    # Cantidad aproximada de pistas (celdas visibles) segun
    # el nivel de dificultad. Es un objetivo, no una garantia
    # exacta: si no se puede quitar mas celdas sin perder la
    # unicidad de la solucion, el puzzle puede quedar con
    # algunas pistas de mas.
    PISTAS_POR_DIFICULTAD = {
        "facil": 40,
        "medio": 32,
        "dificil": 26,
    }

    def __init__(self, dificultad="medio"):
        self.set_dificultad(dificultad)
        self.solution = None
        self.puzzle = None

    # =====================================================
    # CONFIGURACION
    # =====================================================

    def set_dificultad(self, dificultad):
        """
        Establece el nivel de dificultad, que determina cuantas
        celdas quedaran visibles como pistas.
        """

        if dificultad not in self.PISTAS_POR_DIFICULTAD:
            raise ValueError(
                f"Dificultad '{dificultad}' invalida. "
                f"Usar: {list(self.PISTAS_POR_DIFICULTAD.keys())}"
            )

        self.dificultad = dificultad
        self.pistas_objetivo = self.PISTAS_POR_DIFICULTAD[dificultad]

    # =====================================================
    # GENERACION
    # =====================================================

    def generate(self):
        """
        Genera un sudoku completo: la solucion y el puzzle
        (con celdas vacias) listo para jugarse.
        """

        self.solution = self._generar_grid_completo()
        self.puzzle = self._perforar_celdas(self.solution)

        return True

    def _generar_grid_completo(self):
        """
        Genera una cuadricula 9x9 completamente resuelta y
        valida, usando backtracking con orden aleatorio de
        candidatos (para que cada sudoku generado sea distinto).
        """

        grid = [[0] * 9 for _ in range(9)]

        self._rellenar_con_backtracking(grid)

        return grid

    def _rellenar_con_backtracking(self, grid):
        """
        Rellena el grid completo usando backtracking, probando
        los numeros del 1 al 9 en orden aleatorio en cada celda.
        """

        for row in range(9):
            for col in range(9):

                if grid[row][col] != 0:
                    continue

                numeros = list(range(1, 10))
                random.shuffle(numeros)

                for num in numeros:

                    if es_valido(grid, row, col, num):

                        grid[row][col] = num

                        if self._rellenar_con_backtracking(grid):
                            return True

                        grid[row][col] = 0

                return False

        return True

    def _perforar_celdas(self, solution):
        """
        Parte de la solucion completa y va vaciando celdas en
        orden aleatorio, siempre y cuando el puzzle resultante
        conserve una unica solucion posible. Se detiene al
        llegar a la cantidad de pistas objetivo, o antes si ya
        no se puede quitar ninguna celda mas sin perder la
        unicidad de la solucion.
        """

        puzzle = [fila[:] for fila in solution]

        posiciones = [(row, col) for row in range(9) for col in range(9)]
        random.shuffle(posiciones)

        celdas_visibles = 81

        for row, col in posiciones:

            if celdas_visibles <= self.pistas_objetivo:
                break

            valor_original = puzzle[row][col]
            puzzle[row][col] = 0

            if contar_soluciones(puzzle, limite=2) == 1:
                celdas_visibles -= 1
            else:
                # Quitar esta celda rompe la unicidad: se
                # restaura y se prueba con la siguiente.
                puzzle[row][col] = valor_original

        return puzzle

    # =====================================================
    # DATOS PARA EXPORTAR (uso futuro del armador de PDF)
    # =====================================================

    def to_grid(self):
        """
        Devuelve el puzzle (con 0 en las celdas vacias) como
        matriz 2D, listo para dibujarse en una pagina del libro.
        """

        return [fila[:] for fila in self.puzzle]

    def to_solved_grid(self):
        """
        Devuelve la solucion completa como matriz 2D, para la
        pagina de soluciones al final del libro.
        """

        return [fila[:] for fila in self.solution]

    def pistas_actuales(self):
        """
        Devuelve la cantidad real de celdas visibles en el
        puzzle generado (puede ser mayor al objetivo si no se
        pudo perforar mas sin perder la unicidad).
        """

        return sum(1 for fila in self.puzzle for celda in fila if celda != 0)

    def imprimir(self):
        """
        Imprime el puzzle como texto en la consola, con
        separadores visuales cada 3 filas/columnas, para
        verificacion visual rapida.
        """

        for i, fila in enumerate(self.puzzle):

            if i % 3 == 0 and i != 0:
                print("-" * 21)

            texto_fila = []

            for j, celda in enumerate(fila):

                if j % 3 == 0 and j != 0:
                    texto_fila.append("|")

                texto_fila.append(str(celda) if celda != 0 else ".")

            print(" ".join(texto_fila))
