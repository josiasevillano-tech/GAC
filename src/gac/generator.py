"""
Generador automático de crucigramas.

Interfaz principal (compatible con la arquitectura original):
    gen = Generator(datos_crucigrama)
    resultado = gen.generate()

Interfaz de pruebas (conservada):
    gen = Generator(rows=20, cols=20)
    gen.set_words([...])
    resultado = gen.generate()
"""

from .board import Board
from .direction import Direction
from .metrics import Metrics


class Generator:
    """
    Generador automático de crucigramas.
    """

    COMPACTNESS_WEIGHT = 1
    INTERSECTIONS_WEIGHT = 1

    def __init__(self, datos=None, rows=15, cols=15, max_attempts=50000):
        """
        Inicializa el generador.

        Modo original (interfaz pública):
            Generator(datos_crucigrama)  # dict con 'words', opcional 'rows', 'cols'

        Modo de pruebas (conservado):
            Generator(rows=20, cols=20)
        """
        # Inicializar SIEMPRE primero para evitar que set_words() sea sobreescrito
        self.words = []
        self.weight_compactness = 1
        self.weight_intersections = 1
        self.max_attempts = max_attempts
        self.datos = None

        if isinstance(datos, dict):
            self.datos = datos
            self.rows = datos.get("rows", rows)
            self.cols = datos.get("cols", cols)
            if "words" in datos:
                self.set_words(datos["words"])
        else:
            # Modo compatible: Generator(20, 20) o Generator()
            self.rows = datos if isinstance(datos, int) else rows
            self.cols = cols if isinstance(cols, int) else 20

        self.board = Board(self.rows, self.cols)

    def set_words(self, words):
        """
        Establece la lista de palabras a generar.
        Ordena por longitud descendente y baraja aleatoriamente
        dentro de cada grupo del mismo tamaño.
        """
        import random
        from itertools import groupby

        self.words = [word.strip().upper() for word in words]
        self.words.sort(key=len, reverse=True)

        grouped = []
        for length, group in groupby(self.words, key=len):
            group_list = list(group)
            random.shuffle(group_list)
            grouped.extend(group_list)

        self.words = grouped

    def is_word_placed(self, word):
        """Indica si una palabra ya fue colocada."""
        for placement in self.board.placements:
            if placement["word"] == word:
                return True
        return False

    def generate(self):
        """
        Genera un crucigrama mediante backtracking y devuelve los datos
        listos para los exportadores (Exporter / WebExporter).

        Si no se han cargado palabras manualmente y existe self.datos,
        intenta cargarlas desde el diccionario.

        Returns:
            dict con grid, solved_grid, horizontal, vertical, metrics.
            None si no se pudo generar.
        """
        # Si no hay palabras cargadas pero tenemos datos, intentar cargar
        if not self.words and self.datos and "words" in self.datos:
            self.set_words(self.datos["words"])

        if not self.words:
            return None

        # Ejecutar el backtracking reparado (cuerpo probado: 20/20 palabras)
        success = self.generate_with_backtracking(max_attempts=self.max_attempts)

        if success:
            return self.get_crossword_data()
        else:
            return None

    def generate_with_backtracking(self, max_attempts=50000):
        """
        Genera el mejor crucigrama mediante búsqueda con retroceso.

        Prioridad:
        1. Colocar todas las palabras posibles.
        2. Maximizar los cruces.
        3. Minimizar el área delimitadora.
        """

        import random

        if not self.words:
            return False

        original_words = list(self.words)

        best_board = None
        best_word_count = -1
        best_cross_count = -1
        best_area = float("inf")

        # Contador global de nodos (reiniciado por cada intento)
        nodes = 0

        def evaluate_board(board):
            metrics = Metrics(board)

            return (
                metrics.word_count(),
                metrics.cross_count(),
                metrics.bounding_area()
            )

        def save_if_better(board):
            nonlocal best_board
            nonlocal best_word_count
            nonlocal best_cross_count
            nonlocal best_area

            word_count, cross_count, area = evaluate_board(board)

            better = False

            if word_count > best_word_count:
                better = True

            elif word_count == best_word_count:
                if cross_count > best_cross_count:
                    better = True

                elif (
                    cross_count == best_cross_count
                    and area < best_area
                ):
                    better = True

            if better:
                best_word_count = word_count
                best_cross_count = cross_count
                best_area = area
                best_board = board.clone()

        def candidate_positions(board, word):
            candidates = []

            for placed in board.placements:
                crosses = self.find_crosses(
                    placed["word"],
                    word
                )

                for _, placed_index, new_index in crosses:

                    row, col = self.compute_start_position(
                        placed["row"],
                        placed["col"],
                        placed["direction"],
                        placed_index,
                        new_index
                    )

                    if (
                        placed["direction"]
                        == Direction.HORIZONTAL
                    ):
                        direction = Direction.VERTICAL
                    else:
                        direction = Direction.HORIZONTAL

                    if board.can_place_word(
                        row,
                        col,
                        word,
                        direction
                    ):
                        candidate = {
                            "row": row,
                            "col": col,
                            "direction": direction
                        }

                        if candidate not in candidates:
                            candidates.append(candidate)

            random.shuffle(candidates)

            return candidates

        def search(board, remaining, max_nodes):
            nonlocal nodes

            nodes += 1

            if nodes > max_nodes:
                return

            save_if_better(board)

            if not remaining:
                return

            # Elegimos primero la palabra con menos
            # posibilidades. Esto es una heurística
            # fundamental para el backtracking.
            options = []

            for word in remaining:
                candidates = candidate_positions(
                    board,
                    word
                )

                options.append(
                    (len(candidates), word, candidates)
                )

            # CORRECCIÓN 1: Filtrar solo palabras que tienen
            # al menos 1 candidato válido. Si la palabra más
            # restringida (MVR) tiene 0 candidatos, no abandonamos
            # el camino completo; en su lugar, intentamos con las
            # palabras que SÍ pueden colocarse para "abrir" el
            # tablero y crear nuevos cruces para las difíciles.
            valid_options = [
                opt for opt in options if opt[0] > 0
            ]

            if not valid_options:
                # Ninguna palabra restante puede colocarse en
                # este tablero: camino inválido.
                return

            # Primero la palabra más restringida ENTRE LAS VÁLIDAS.
            valid_options.sort(key=lambda item: item[0])

            candidate_count, word, candidates = valid_options[0]

            new_remaining = [
                w for w in remaining
                if w != word
            ]

            for candidate in candidates:
                row = candidate["row"]
                col = candidate["col"]
                direction = candidate["direction"]

                new_board = board.clone()

                if not new_board.place_word(
                    row,
                    col,
                    word,
                    direction
                ):
                    continue

                search(
                    new_board,
                    new_remaining,
                    max_nodes
                )

                # Si ya conseguimos todas, no hace falta
                # seguir buscando en este nivel.
                if best_word_count == len(original_words):
                    return

        # ==================================================
        # Probamos diferentes palabras iniciales.
        # ==================================================

        # CORRECCIÓN 2: En lugar de barajar aleatoriamente y
        # tomar la primera, probamos CADA palabra como inicial
        # empezando por la más larga. Las palabras largas tienen
        # más letras y por tanto más oportunidades de cruce,
        # lo que aumenta drásticamente las probabilidades de
        # éxito del backtracking.
        words_by_length = sorted(
            original_words,
            key=len,
            reverse=True
        )

        for first_word in words_by_length:

            # CORRECCIÓN 3: Reiniciar el contador de nodos para
            # cada intento con palabra inicial diferente. Antes
            # el contador era global y los intentos posteriores
            # se quedaban sin presupuesto de exploración.
            nodes = 0

            board = Board(
                self.board.rows,
                self.board.cols
            )

            row = board.rows // 2
            col = (
                board.cols - len(first_word)
            ) // 2

            if not board.can_place_word(
                row,
                col,
                first_word,
                Direction.HORIZONTAL
            ):
                continue

            if not board.place_word(
                row,
                col,
                first_word,
                Direction.HORIZONTAL
            ):
                continue

            remaining = [
                w for w in original_words
                if w != first_word
            ]
            random.shuffle(remaining)

            # Presupuesto de nodos proporcional al total,
            # con un mínimo razonable para no abortar muy pronto.
            max_nodes = max(
                max_attempts // len(words_by_length),
                10000
            )

            search(
                board,
                remaining,
                max_nodes
            )

            if best_word_count == len(original_words):
                break

        if best_board is None:
            return False

        self.board = best_board
        self.board.assign_numbers()

        metrics = Metrics(self.board)
        metrics.report()

        return best_word_count == len(original_words)

    def try_place_anywhere(self, word, placed_words):
        """
        Intenta colocar una palabra en cualquier posición válida."""

        candidates = []

        for placed in self.board.placements:
            crosses = self.find_crosses(placed["word"], word)
            for _, placed_index, new_index in crosses:
                row, col = self.compute_start_position(
                    placed["row"], placed["col"], placed["direction"],
                    placed_index, new_index
                )

                direction = (
                    Direction.VERTICAL
                    if placed["direction"] == Direction.HORIZONTAL
                    else Direction.HORIZONTAL
                )

                if self.board.can_place_word(row, col, word, direction):
                    candidates.append({"row": row, "col": col, "direction": direction})

        if not candidates:
            return False

        best = self.choose_best_candidate(candidates, word)
        self.board.place_word(best["row"], best["col"], word, best["direction"])
        return True

    def try_place_word(self, placed, word):
        """Intenta colocar una palabra utilizando los candidatos disponibles."""
        candidates = self.find_candidate_positions(placed, word)
        if not candidates:
            return False

        candidate = self.choose_best_candidate(candidates, word)
        self.board.place_word(
            candidate["row"], candidate["col"], word, candidate["direction"]
        )
        return True

    def find_common_letters(self, word1, word2):
        """Devuelve las letras comunes entre dos palabras."""
        common = []
        for letter in word1:
            if letter in word2 and letter not in common:
                common.append(letter)
        return common

    def find_letter_positions(self, word, letter):
        """Devuelve todas las posiciones de una letra dentro de una palabra."""
        return [i for i, c in enumerate(word) if c == letter]

    def find_crosses(self, word1, word2):
        """Devuelve todas las posibilidades de cruce entre dos palabras."""
        crosses = []
        common = self.find_common_letters(word1, word2)
        for letter in common:
            for p1 in self.find_letter_positions(word1, letter):
                for p2 in self.find_letter_positions(word2, letter):
                    crosses.append((letter, p1, p2))
        return crosses

    def compute_start_position(self, placed_row, placed_col, placed_direction,
                               placed_index, new_index):
        """Calcula la posición inicial de una palabra para cruzarla con otra."""
        dr, dc = placed_direction.value
        cross_row = placed_row + placed_index * dr
        cross_col = placed_col + placed_index * dc

        if placed_direction == Direction.HORIZONTAL:
            return cross_row - new_index, cross_col
        else:
            return cross_row, cross_col - new_index

    def find_candidate_positions(self, placed, word):
        """Encuentra todas las posiciones válidas para colocar una palabra."""
        candidates = []
        crosses = self.find_crosses(placed["word"], word)

        for _, placed_index, new_index in crosses:
            row, col = self.compute_start_position(
                placed["row"], placed["col"], placed["direction"],
                placed_index, new_index
            )

            direction = (
                Direction.VERTICAL
                if placed["direction"] == Direction.HORIZONTAL
                else Direction.HORIZONTAL
            )

            if self.board.can_place_word(row, col, word, direction):
                candidates.append({"row": row, "col": col, "direction": direction})

        return candidates

    def choose_best_candidate(self, candidates, word):
        """Selecciona el mejor candidato disponible."""
        if not candidates:
            return None

        best = candidates[0]
        best_score = self.evaluate_candidate(self.board, word, best)

        for candidate in candidates[1:]:
            score = self.evaluate_candidate(self.board, word, candidate)
            if score > best_score:
                best = candidate
                best_score = score

        return best

    def evaluate_candidate(self, board, word, candidate):
        """Asigna una puntuación a un candidato."""
        test_board = board.clone()
        test_board.place_word(
            candidate["row"], candidate["col"], word, candidate["direction"]
        )

        compactness = self.score_compactness(test_board)
        intersections = self.score_intersections(test_board)

        return (
            compactness * self.weight_compactness +
            intersections * self.weight_intersections
        )

    def score_compactness(self, board):
        """Calcula la puntuación por compacidad."""
        return -board.bounding_area()

    def score_intersections(self, board):
        """Premia las palabras que generan cruces."""
        score = 0
        for placement in board.placements:
            row, col = placement["row"], placement["col"]
            if placement["direction"] == Direction.HORIZONTAL:
                for i in range(len(placement["word"])):
                    if (row - 1, col + i) in board.cells and (row + 1, col + i) in board.cells:
                        score += 1
            else:
                for i in range(len(placement["word"])):
                    if (row + i, col - 1) in board.cells and (row + i, col + 1) in board.cells:
                        score += 1
        return score

    def get_crossword_data(self):
        """
        Devuelve todos los datos necesarios para exportar el crucigrama.
        """
        if not self.board.placements:
            return None

        self.board.assign_numbers()

        horizontal = []
        vertical = []

        for p in self.board.placements:
            entry = {
                "number": p["number"],
                "word": p["word"],
                "row": p["row"],
                "col": p["col"],
                "length": len(p["word"])
            }
            if p["direction"] == Direction.HORIZONTAL:
                horizontal.append(entry)
            else:
                vertical.append(entry)

        horizontal.sort(key=lambda x: x["number"])
        vertical.sort(key=lambda x: x["number"])

        return {
            "grid": self.board.to_grid(),
            "solved_grid": self.board.to_solved_grid(),
            "horizontal": horizontal,
            "vertical": vertical,
            "metrics": {
                "word_count": self.board.word_count(),
                "bounding_area": self.board.bounding_area()
            }
        }