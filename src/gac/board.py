class Board:
    """
    Representa el estado de un tablero de crucigrama.
    """

    def __init__(self, rows=15, cols=15):
        """
        Crea un tablero vacío.
        """

        # Dimensiones
        self.rows = rows
        self.cols = cols

        # Casillas ocupadas.
        # Clave: (fila, columna)
        # Valor: letra
        self.cells = {}

        # Lista de palabras colocadas.
        self.placements = []

    def is_empty(self, row, col):
        """
        Devuelve True si la casilla está vacía.
        """

        return (row, col) not in self.cells

    def is_inside(self, row, col):
        """
        Devuelve True si la coordenada pertenece al tablero.
        """

        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def set_cell(self, row, col, letter):
        """
        Coloca una letra en una casilla del tablero.
        """

        self.cells[(row, col)] = letter

    def get_cell(self, row, col):
        """
        Devuelve la letra almacenada en una casilla.

        Si la casilla está vacía devuelve None.
        """

        return self.cells.get((row, col))

    def can_place_word(self, row, col, word, direction):
        """
        Determina si una palabra puede colocarse en el tablero.

        No modifica el tablero.
        Devuelve True o False.
        """

        dr, dc = direction.value

        current_row = row
        current_col = col

        for letter in word:

            # 1. Debe estar dentro del tablero.
            if not self.is_inside(current_row, current_col):
                return False

            # 2. Si la casilla está ocupada,
            #    la letra debe coincidir.
            current_letter = self.get_cell(current_row, current_col)

            if current_letter is not None:
                if current_letter != letter:
                    return False

            print(letter, "->", (current_row, current_col))

            current_row += dr
            current_col += dc

        return True

    def place_word(self, row, col, word, direction):
        """
        Coloca una palabra en el tablero.

        Se asume que la posición ya fue validada.
        """

        if not self.can_place_word(row, col, word, direction):
            return False

        dr, dc = direction.value

        current_row = row
        current_col = col

        for letter in word:
            self.set_cell(current_row, current_col, letter)

            current_row += dr
            current_col += dc

        self.placements.append(
            {
                "word": word,
                "row": row,
                "col": col,
                "direction": direction,
            }
        )

        return True
    
    def clear(self):
        """
        Limpia completamente el tablero.
        """

        self.cells.clear()
        self.placements.clear()

    def word_count(self):
        """
        Devuelve la cantidad de palabras colocadas.
        """

        return len(self.placements)