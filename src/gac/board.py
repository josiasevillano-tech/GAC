class Board:
    """
    Representa el estado de un tablero de crucigrama.
    """

    def __init__(self, rows=15, cols=15):
        """Crea un tablero vacío."""
        self.rows = rows
        self.cols = cols
        self.cells = {}          # (fila, columna) -> letra
        self.placements = []     # lista de palabras colocadas

    def is_empty(self, row, col):
        """Devuelve True si la casilla está vacía."""
        return (row, col) not in self.cells

    def is_inside(self, row, col):
        """Devuelve True si la coordenada pertenece al tablero."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def set_cell(self, row, col, letter):
        """Coloca una letra en una casilla del tablero."""
        self.cells[(row, col)] = letter

    def get_cell(self, row, col):
        """Devuelve la letra almacenada en una casilla. None si está vacía."""
        return self.cells.get((row, col))

    def can_place_word(self, row, col, word, direction):
        """
        Determina si una palabra puede colocarse en el tablero.
        Reglas:
          1. Dentro de los límites.
          2. Letras coincidentes en cruces.
          3. NO formar palabras accidentales perpendiculares.
          4. Extremos libres: antes y después de la palabra no debe haber letras.
        """
        dr, dc = direction.value

        # ── Regla 4: Extremos libres ──
        # Celda ANTES del inicio
        before_r, before_c = row - dr, col - dc
        if self.is_inside(before_r, before_c) and self.get_cell(before_r, before_c) is not None:
            return False

        # Celda DESPUÉS del final
        after_r, after_c = row + len(word) * dr, col + len(word) * dc
        if self.is_inside(after_r, after_c) and self.get_cell(after_r, after_c) is not None:
            return False

        current_row, current_col = row, col

        for letter in word:
            # Regla 1: Dentro del tablero
            if not self.is_inside(current_row, current_col):
                return False

            # Regla 2: Letra coincidente en cruces
            current_letter = self.get_cell(current_row, current_col)
            if current_letter is not None and current_letter != letter:
                return False

            # Regla 3: No formar palabras accidentales perpendiculares
            if current_letter is None:
                if dr == 0:  # Horizontal: verificar arriba/abajo
                    if (self.is_inside(current_row - 1, current_col) and
                            self.get_cell(current_row - 1, current_col) is not None):
                        return False
                    if (self.is_inside(current_row + 1, current_col) and
                            self.get_cell(current_row + 1, current_col) is not None):
                        return False
                else:  # Vertical: verificar izquierda/derecha
                    if (self.is_inside(current_row, current_col - 1) and
                            self.get_cell(current_row, current_col - 1) is not None):
                        return False
                    if (self.is_inside(current_row, current_col + 1) and
                            self.get_cell(current_row, current_col + 1) is not None):
                        return False

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

    def clone(self):
        """Devuelve una copia independiente del tablero."""
        board = Board(self.rows, self.cols)
        board.cells = self.cells.copy()
        board.placements = [p.copy() for p in self.placements]
        return board

    def word_count(self):
        """Devuelve la cantidad de palabras colocadas."""
        return len(self.placements)

    def bounding_box(self):
        """Devuelve el rectángulo mínimo que contiene todas las letras."""
        if not self.cells:
            return None

        rows = [row for row, _ in self.cells]
        cols = [col for _, col in self.cells]

        return {
            "min_row": min(rows),
            "max_row": max(rows),
            "min_col": min(cols),
            "max_col": max(cols)
        }

    def bounding_area(self):
        """Devuelve el área del rectángulo mínimo que contiene todas las letras."""
        box = self.bounding_box()
        if box is None:
            return 0
        height = box["max_row"] - box["min_row"] + 1
        width = box["max_col"] - box["min_col"] + 1
        return height * width

    # =====================================================
    # Sistema de numeración de palabras
    # =====================================================

    def assign_numbers(self):
        """
        Asigna números a las palabras según la posición de inicio
        en el tablero (de arriba a abajo, de izquierda a derecha).
        Palabras que inician en la misma casilla comparten número.
        """
        if not self.placements:
            return

        sorted_placements = sorted(
            self.placements,
            key=lambda p: (p["row"], p["col"])
        )

        number = 1
        position_to_number = {}

        for p in sorted_placements:
            pos = (p["row"], p["col"])
            if pos not in position_to_number:
                position_to_number[pos] = number
                number += 1
            p["number"] = position_to_number[pos]

    def get_numbered_placements(self):
        """Devuelve las palabras ordenadas por número y dirección."""
        if not self.placements:
            return []
        if "number" not in self.placements[0]:
            self.assign_numbers()
        return sorted(
            self.placements,
            key=lambda p: (p["number"], p["direction"].name)
        )

    def get_clue_cells(self):
        """
        Devuelve un diccionario {(row, col): number}
        con las casillas que deben mostrar un número.
        """
        if not self.placements:
            return {}
        if "number" not in self.placements[0]:
            self.assign_numbers()
        return {
            (p["row"], p["col"]): p["number"]
            for p in self.placements
        }

    def to_grid(self):
        """
        Devuelve una matriz 2D con la información de cada celda
        dentro del área delimitadora (vacío con números para estudiante).
        """
        if not self.cells:
            return []

        box = self.bounding_box()
        if box is None:
            return []

        clue_cells = self.get_clue_cells()
        grid = []

        for r in range(box["min_row"], box["max_row"] + 1):
            row = []
            for c in range(box["min_col"], box["max_col"] + 1):
                letter = self.cells.get((r, c))
                row.append({
                    "letter": letter,
                    "number": clue_cells.get((r, c)),
                    "is_empty": letter is None
                })
            grid.append(row)

        return grid

    def to_solved_grid(self):
        """
        Devuelve una matriz 2D con las LETRAS visibles
        dentro del área delimitadora (para vista en miniatura del maestro).
        """
        if not self.cells:
            return []

        box = self.bounding_box()
        if box is None:
            return []

        grid = []
        for r in range(box["min_row"], box["max_row"] + 1):
            row = []
            for c in range(box["min_col"], box["max_col"] + 1):
                letter = self.cells.get((r, c))
                row.append({
                    "letter": letter if letter else "",
                    "number": None,
                    "is_empty": letter is None
                })
            grid.append(row)
        return grid