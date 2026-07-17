from src.gac.board import Board
from src.gac.direction import Direction


class Generator:
    """
    Generador automático de crucigramas.
    """

    def __init__(self, rows=15, cols=15):
        self.board = Board(rows, cols)
        self.words = []

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

            placed_ok = False

            for placed in reversed(self.board.placements):

                if self.try_place_word(placed, word):
                    placed_ok = True
                    break

        return True
    
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
    
    def try_place_word(self, placed, word):
        """
        Intenta encontrar una posición válida para una palabra.
        """

        crosses = self.find_crosses(placed["word"], word)

        for _, placed_index, new_index in crosses:

            row, col = self.compute_start_position(
                placed["row"],
                placed["col"],
                placed["direction"],
                placed_index,
                new_index
            )
            if placed["direction"] == Direction.HORIZONTAL:
                new_direction = Direction.VERTICAL
            else:
                new_direction = Direction.HORIZONTAL
            if self.board.can_place_word(
                row,
                col,
                word,
                new_direction
            ):
                self.board.place_word(
                    row,
                    col,
                    word,
                    new_direction
                )

                return True

        return False