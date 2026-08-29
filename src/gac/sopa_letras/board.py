class Board:
    """
    Representa el estado de un tablero de sopa de letras.

    A diferencia del tablero de crucigrama, aqui NO se exige que
    las palabras se crucen entre si, y SI se permite que las letras
    queden adyacentes a otras palabras (al final todo el tablero
    se rellena de letras de todos modos).
    """

    def __init__(self, rows=15, cols=15):
        """Crea un tablero vacio."""
        self.rows = rows
        self.cols = cols
        self.cells = {}          # (fila, columna) -> letra
        self.placements = []     # lista de palabras colocadas

    def is_empty(self, row, col):
        """Devuelve True si la casilla esta vacia."""
        return (row, col) not in self.cells

    def is_inside(self, row, col):
        """Devuelve True si la coordenada pertenece al tablero."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def set_cell(self, row, col, letter):
        """Coloca una letra en una casilla del tablero."""
        self.cells[(row, col)] = letter

    def get_cell(self, row, col):
        """Devuelve la letra almacenada en una casilla. None si esta vacia."""
        return self.cells.get((row, col))

    def can_place_word(self, row, col, word, direction):
        """
        Determina si una palabra puede colocarse.

        Unica regla: cada letra debe caer dentro del tablero, y si
        la casilla ya tiene una letra, debe coincidir exactamente.
        No se exige cruce ni se prohibe contacto lateral.
        """
        dr, dc = direction.value

        current_row = row
        current_col = col

        for letter in word:

            if not self.is_inside(current_row, current_col):
                return False

            current_letter = self.get_cell(current_row, current_col)

            if current_letter is not None and current_letter != letter:
                return False

            current_row += dr
            current_col += dc

        return True

    def place_word(self, row, col, word, direction):
        """
        Coloca una palabra en el tablero.
        Se asume que la posicion ya fue validada.
        """
        if not self.can_place_word(row, col, word, direction):
            return False

        dr, dc = direction.value
        current_row, current_col = row, col

        for letter in word:
            self.set_cell(current_row, current_col, letter)
            current_row += dr
            current_col += dc

        self.placements.append({
            "word": word,
            "row": row,
            "col": col,
            "direction": direction,
        })

        return True

    def clear(self):
        """Limpia completamente el tablero."""
        self.cells.clear()
        self.placements.clear()

    def word_count(self):
        """Devuelve la cantidad de palabras colocadas."""
        return len(self.placements)

    def imprimir(self):
        """
        Imprime el tablero como texto en la consola,
        para verificacion visual rapida.
        """
        for row in range(self.rows):
            fila = []
            for col in range(self.cols):
                letra = self.get_cell(row, col)
                fila.append(letra if letra else ".")
            print(" ".join(fila))
