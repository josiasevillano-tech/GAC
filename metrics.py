"""
Módulo de métricas del GAC.

Calcula indicadores objetivos de calidad de un crucigrama generado.
"""


class Metrics:
    """
    Sistema de métricas para evaluar crucigramas.
    """

    def __init__(self, board):
        """
        Inicializa el sistema de métricas con un tablero.
        """
        self.board = board

    # =====================================================
    # MÉTRICAS BÁSICAS
    # =====================================================

    def word_count(self):
        """
        Número de palabras colocadas en el tablero.
        """
        return self.board.word_count()

    def bounding_area(self):
        """
        Área del rectángulo mínimo que contiene todas las letras.
        """
        return self.board.bounding_area()

    def letter_count(self):
        """
        Número total de letras colocadas en el tablero.
        """
        return len(self.board.cells)

    # =====================================================
    # MÉTRICA: CRUCES
    # =====================================================

    def cross_count(self):
        """
        Número de cruces reales entre palabras.

        Un cruce ocurre cuando dos palabras distintas comparten
        la misma casilla con la misma letra.
        """

        # Conjunto de casillas ocupadas por cada palabra
        word_cells = []

        for placement in self.board.placements:
            cells = set()
            dr, dc = placement["direction"].value

            for i in range(len(placement["word"])):
                row = placement["row"] + i * dr
                col = placement["col"] + i * dc
                cells.add((row, col))

            word_cells.append(cells)

        # Contar intersecciones entre pares de palabras
        crosses = 0

        for i in range(len(word_cells)):
            for j in range(i + 1, len(word_cells)):
                intersection = word_cells[i] & word_cells[j]
                crosses += len(intersection)

        return crosses

    # =====================================================
    # MÉTRICA: DENSIDAD
    # =====================================================

    def density(self):
        """
        Densidad del crucigrama = letras / área ocupada.

        Un valor cercano a 1 indica que el área está bien aprovechada.
        Un valor bajo indica muchos espacios vacíos dentro del área.
        """

        area = self.bounding_area()

        if area == 0:
            return 0.0

        return self.letter_count() / area

    # =====================================================
    # REPORTE
    # =====================================================

    def report(self):
        """
        Genera y muestra un reporte completo de métricas.
        """

        print("=" * 40)
        print("  MÉTRICAS DEL CRUCIGRAMA")
        print("=" * 40)

        print(f"  Palabras colocadas: {self.word_count()}")
        print(f"  Cruces:             {self.cross_count()}")
        print(f"  Área ocupada:       {self.bounding_area()}")
        print(f"  Letras totales:     {self.letter_count()}")
        print(f"  Densidad:           {self.density():.2f}")

        print("=" * 40)