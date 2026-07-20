from src.gac.board import Board
from src.gac.direction import Direction


class Generator:
    """
    Generador automático de crucigramas.
    """

    COMPACTNESS_WEIGHT = 1
    INTERSECTIONS_WEIGHT = 1

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(self, rows=15, cols=15):
        self.board = Board(rows, cols)
        self.words = []

    # =====================================================
    # CONFIGURACIÓN
    # =====================================================

    def set_words(self, words):
        """
        Establece la lista de palabras a generar.
        """

        self.words = []

        for word in words:
            self.words.append(word.strip().upper())
            
        self.words.sort(
            key=len,
            reverse=True
        )

    def is_word_placed(self, word):
        """
        Indica si una palabra ya fue colocada.
        """

        for placement in self.board.placements:

            if placement["word"] == word:
                return True

        return False
    
    # =====================================================
    # GENERACIÓN DEL CRUCIGRAMA
    # =====================================================

    def generate(self):
        """
        Genera un crucigrama.
        """

        if not self.words:
            return False

        first_word = self.words[0]

        row = self.board.rows // 2
        col = (self.board.cols - len(first_word)) // 2

        self.board.place_word(
            row,
            col,
            first_word,
            Direction.HORIZONTAL
        )

        for word in self.words[1:]:

            if self.is_word_placed(word):
                continue

            placed_ok = False

            for placed in reversed(self.board.placements):

                if self.try_place_word(placed, word):
                    placed_ok = True
                    break

        return True
    
    # =====================================================
    # BÚSQUEDA DE CANDIDATOS
    # =====================================================
    
    def find_common_letters(self, word1, word2):
        """
        Devuelve las letras comunes entre dos palabras.
        """

        common = []

        for letter in word1:
            if letter in word2 and letter not in common:
                common.append(letter)

        return common
    
    def find_letter_positions(self, word, letter):
        """
        Devuelve todas las posiciones de una letra
        dentro de una palabra.
        """

        positions = []

        for index, current in enumerate(word):
            if current == letter:
                positions.append(index)

        return positions
    
    def find_crosses(self, word1, word2):
        """
        Devuelve todas las posibilidades de cruce
        entre dos palabras.
        """

        crosses = []

        common = self.find_common_letters(word1, word2)

        for letter in common:

            positions1 = self.find_letter_positions(word1, letter)
            positions2 = self.find_letter_positions(word2, letter)

            for p1 in positions1:
                for p2 in positions2:
                    crosses.append((letter, p1, p2))

        return crosses
    
    def compute_start_position(
        self,
        placed_row,
        placed_col,
        placed_direction,
        placed_index,
        new_index
    ):
        """
        Calcula la posición inicial de una palabra
        para cruzarla con otra ya colocada.
        """

        dr, dc = placed_direction.value

        cross_row = placed_row + placed_index * dr
        cross_col = placed_col + placed_index * dc

        if placed_direction == Direction.HORIZONTAL:

            row = cross_row - new_index
            col = cross_col

        else:

            row = cross_row
            col = cross_col - new_index

        return row, col
    
    # =====================================================
    # EVALUACIÓN DE CANDIDATOS
    # =====================================================
        
    def evaluate_candidate(
        self,
        board,
        word,
        candidate
    ):
        """
        Asigna una puntuación a un candidato.
        """

        test_board = board.clone()

        test_board.place_word(
            candidate["row"],
            candidate["col"],
            word,
            candidate["direction"]
        )
        score = 0

        compactness = self.score_compactness(
            test_board
        )

        intersections = self.score_intersections(
            test_board
        )

        score += (
            compactness *
            self.COMPACTNESS_WEIGHT
        )

        score += (
            intersections *
            self.INTERSECTIONS_WEIGHT
        )

        return score

    def score_compactness(
        self,
        board
    ):
        """
        Calcula la puntuación por compacidad.
        """

        return -board.bounding_area()
    
    def score_intersections(
        self,
        board
    ):
        """
        Premia las palabras que generan cruces.
        """

        score = 0

        for placement in board.placements:

            row = placement["row"]
            col = placement["col"]

            if placement["direction"] == Direction.HORIZONTAL:

                for i in range(len(placement["word"])):

                    if (
                        (row - 1, col + i) in board.cells and
                        (row + 1, col + i) in board.cells
                    ):
                        score += 1

            else:

                for i in range(len(placement["word"])):

                    if (
                        (row + i, col - 1) in board.cells and
                        (row + i, col + 1) in board.cells
                    ):
                        score += 1

        return score
      
    def choose_best_candidate(
        self,
        candidates,
        word
    ):
        """
        Selecciona el mejor candidato disponible.
        """

        if not candidates:
            return None

        best = candidates[0]
        best_score = self.evaluate_candidate(
            self.board,
            word,
            best
        )

        for candidate in candidates[1:]:

            score = self.evaluate_candidate(
                self.board,
                word,
                candidate
        )

            if score > best_score:
                best = candidate
                best_score = score

        return best
    
    def find_candidate_positions(self, placed, word):
        """
        Encuentra todas las posiciones válidas donde una palabra
        podría colocarse cruzándose con otra.
        """

        candidates = []

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

            if placed["direction"] == Direction.HORIZONTAL:
                direction = Direction.VERTICAL
            else:
                direction = Direction.HORIZONTAL

            if self.board.can_place_word(
                row,
                col,
                word,
                direction
            ):
                candidates.append({
                    "row": row,
                    "col": col,
                    "direction": direction
                })

        return candidates
        
    def try_place_word(self, placed, word):
        """
        Intenta colocar una palabra utilizando los candidatos disponibles.
        """

        candidates = self.find_candidate_positions(
            placed,
            word
        )

        if not candidates:
            return False

        candidate = self.choose_best_candidate(
            candidates,
            word
        )

        self.board.place_word(
            candidate["row"],
            candidate["col"],
            word,
            candidate["direction"]
        )

        return True