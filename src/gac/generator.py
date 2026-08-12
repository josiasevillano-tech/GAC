from .board import Board
from .direction import Direction
from .metrics import Metrics


class Generator:
    """
    Generador automÃ¡tico de crucigramas.
    """

    COMPACTNESS_WEIGHT = 1
    INTERSECTIONS_WEIGHT = 1

    def __init__(self, rows=15, cols=15):
        self.board = Board(rows, cols)
        self.words = []
        self.weight_compactness = 1
        self.weight_intersections = 1

    def set_words(self, words):
        """
        Establece la lista de palabras a generar.
        Ordena por longitud descendente y baraja aleatoriamente
        dentro de cada grupo del mismo tamaÃ±o.
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
        Genera un crucigrama (versiÃ³n bÃ¡sica).
        """
        if not self.words:
            return False

        self.board = Board(self.board.rows, self.board.cols)

        first_word = self.words[0]
        row = self.board.rows // 2
        col = (self.board.cols - len(first_word)) // 2

        self.board.place_word(row, col, first_word, Direction.HORIZONTAL)

        for word in self.words[1:]:
            if self.is_word_placed(word):
                continue
            for placed in reversed(self.board.placements):
                if self.try_place_word(placed, word):
                    break

        self.board.assign_numbers()

        metrics = Metrics(self.board)
        metrics.report()

        return True

    def generate_with_backtracking(self, max_attempts=100):
        """
        Genera un crucigrama usando mÃºltiples intentos
        y seleccionando el mejor tablero.
        """
        import random

        if not self.words:
            return False

        best_board = None
        best_score = -1

        for attempt in range(max_attempts):
            self.board = Board(self.board.rows, self.board.cols)

            shuffled = self.words.copy()
            random.shuffle(shuffled)

            first_word = shuffled[0]
            row = self.board.rows // 2
            col = (self.board.cols - len(first_word)) // 2
            self.board.place_word(row, col, first_word, Direction.HORIZONTAL)

            placed_words = [first_word]
            failed_words = []

            for word in shuffled[1:]:
                if self.try_place_anywhere(word, placed_words):
                    placed_words.append(word)
                else:
                    failed_words.append(word)

            metrics = Metrics(self.board)
            score = (
                metrics.word_count() * 100 +
                metrics.cross_count() * 10 -
                metrics.bounding_area()
            )

            if score > best_score:
                best_score = score
                best_board = self.board.clone()

        self.board = best_board
        self.board.assign_numbers()

        metrics = Metrics(self.board)
        metrics.report()

        return True

    def try_place_anywhere(self, word, placed_words):
        """Intenta colocar una palabra en cualquier posiciÃ³n vÃ¡lida."""
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
        """Calcula la posiciÃ³n inicial de una palabra para cruzarla con otra."""
        dr, dc = placed_direction.value
        cross_row = placed_row + placed_index * dr
        cross_col = placed_col + placed_index * dc

        if placed_direction == Direction.HORIZONTAL:
            return cross_row - new_index, cross_col
        else:
            return cross_row, cross_col - new_index

    def find_candidate_positions(self, placed, word):
        """Encuentra todas las posiciones vÃ¡lidas para colocar una palabra."""
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
        """Asigna una puntuaciÃ³n a un candidato."""
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
        """Calcula la puntuaciÃ³n por compacidad."""
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
