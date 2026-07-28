class Metrics:
    """
    Sistema de métricas del GAC.
    Mide objetivamente la calidad de un crucigrama generado.
    """

    def __init__(self, board):
        self.board = board

    def word_count(self):
        """Devuelve la cantidad de palabras colocadas."""
        return self.board.word_count()

    def cross_count(self):
        """
        Cuenta las intersecciones entre palabras.
        Una intersección es una celda que tiene vecinos
        tanto horizontales como verticales.
        """
        count = 0
        for (row, col) in self.board.cells:
            has_horizontal = (
                (row, col - 1) in self.board.cells or
                (row, col + 1) in self.board.cells
            )
            has_vertical = (
                (row - 1, col) in self.board.cells or
                (row + 1, col) in self.board.cells
            )
            if has_horizontal and has_vertical:
                count += 1
        return count

    def bounding_area(self):
        """Devuelve el área del rectángulo mínimo que contiene todas las letras."""
        return self.board.bounding_area()

    def density(self):
        """Devuelve la densidad del crucigrama (celdas ocupadas / área total)."""
        area = self.bounding_area()
        if area == 0:
            return 0.0
        return len(self.board.cells) / area

    def report(self):
        """Muestra el reporte de métricas en consola."""
        print("=" * 42)
        print("         MÉTRICAS DEL CRUCIGRAMA")
        print("=" * 42)
        print(f"  Palabras colocadas:  {self.word_count()}")
        print(f"  Cruces:              {self.cross_count()}")
        print(f"  Área delimitadora:   {self.bounding_area()}")
        print(f"  Densidad:            {self.density():.2%}")
        print("=" * 42)