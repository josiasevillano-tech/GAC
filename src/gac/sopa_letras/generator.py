import random
import string

from .board import Board
from .direction import Direction


class Generator:
    """
    Generador automatico de sopas de letras.

    A diferencia del crucigrama, las palabras no necesitan
    cruzarse entre si: cada una se coloca en linea recta,
    en cualquiera de las 8 direcciones, y el resto del
    tablero se rellena con letras aleatorias.
    """

    # Letras usadas para el relleno (sin acentos ni Ñ).
    LETRAS_RELLENO = string.ascii_uppercase

    def __init__(self, rows=15, cols=15, max_attempts=200):
        self.board = Board(rows, cols)
        self.words = []
        self.max_attempts = max_attempts

    # =====================================================
    # CONFIGURACION
    # =====================================================

    def set_words(self, words):
        """
        Establece la lista de palabras a colocar.

        Se ordenan de mayor a menor longitud para colocar
        primero las mas dificiles de ubicar.
        """

        self.words = []

        for word in words:
            self.words.append(word.strip().upper())

        self.words.sort(key=len, reverse=True)

    # =====================================================
    # GENERACION
    # =====================================================

    def generate(self):
        """
        Genera la sopa de letras completa: coloca todas las
        palabras posibles y rellena el resto del tablero.

        Devuelve True si se colocaron todas las palabras,
        False si alguna no pudo ubicarse.
        """

        self.board = Board(self.board.rows, self.board.cols)

        todas_colocadas = True

        for word in self.words:
            if not self._colocar_palabra(word):
                todas_colocadas = False

        self._rellenar_espacios_vacios()

        return todas_colocadas

    def _colocar_palabra(self, word):
        """
        Intenta colocar una palabra en una posicion y
        direccion aleatoria, probando hasta max_attempts veces.
        """

        direcciones = list(Direction)

        for _ in range(self.max_attempts):

            direction = random.choice(direcciones)
            row = random.randint(0, self.board.rows - 1)
            col = random.randint(0, self.board.cols - 1)

            if self.board.can_place_word(row, col, word, direction):
                self.board.place_word(row, col, word, direction)
                return True

        return False

    def _rellenar_espacios_vacios(self):
        """
        Rellena todas las celdas vacias del tablero con
        letras aleatorias (A-Z, sin acentos ni Ñ).
        """

        for row in range(self.board.rows):
            for col in range(self.board.cols):

                if self.board.is_empty(row, col):
                    letra = random.choice(self.LETRAS_RELLENO)
                    self.board.set_cell(row, col, letra)

    # =====================================================
    # METRICAS
    # =====================================================

    def word_count(self):
        """
        Devuelve la cantidad de palabras colocadas.
        """

        return self.board.word_count()

    def words_not_placed(self):
        """
        Devuelve la lista de palabras que NO se lograron colocar.
        """

        colocadas = [p["word"] for p in self.board.placements]

        return [w for w in self.words if w not in colocadas]
