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
        Determina si una palabra puede colocarse legalmente.

        Permite:
        - colocar dentro del tablero;
        - cruzar letras existentes si coinciden;
        - impedir contactos laterales que no sean cruces;
        - impedir letras pegadas inmediatamente antes o después.
        """
        dr, dc = direction.value

        # La posición inicial debe estar dentro del tablero.
        if not self.is_inside(row, col):
            return False

        # Calcular la posición final.
        end_row = row + (len(word) - 1) * dr
        end_col = col + (len(word) - 1) * dc

        # La palabra completa debe quedar dentro del tablero.
        if not self.is_inside(end_row, end_col):
            return False

        # Celda inmediatamente anterior.
        before_row = row - dr
        before_col = col - dc

        if self.is_inside(before_row, before_col):
            if self.get_cell(before_row, before_col) is not None:
                return False

        # Celda inmediatamente posterior.
        after_row = end_row + dr
        after_col = end_col + dc

        if self.is_inside(after_row, after_col):
            if self.get_cell(after_row, after_col) is not None:
                return False

        current_row = row
        current_col = col
        crossings = 0

        for letter in word:
            current_letter = self.get_cell(current_row, current_col)

            # Si ya existe una letra, debe coincidir.
            if current_letter is not None:
                if current_letter != letter:
                    return False

                crossings += 1

            else:
                # Las casillas nuevas no pueden tocar lateralmente
                # otras palabras.
                if dr == 0:
                    # Palabra horizontal.
                    above = self.get_cell(
                        current_row - 1,
                        current_col
                    )
                    below = self.get_cell(
                        current_row + 1,
                        current_col
                    )

                    if above is not None or below is not None:
                        return False

                else:
                    # Palabra vertical.
                    left = self.get_cell(
                        current_row,
                        current_col - 1
                    )
                    right = self.get_cell(
                        current_row,
                        current_col + 1
                    )

                    if left is not None or right is not None:
                        return False

            current_row += dr
            current_col += dc

        # Si ya hay palabras en el tablero, una nueva palabra
        # debe conectarse mediante al menos un cruce.
        if self.cells and crossings == 0:
            return False

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