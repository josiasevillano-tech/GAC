import random
import string

from .board import Board
from .direction import Direction


class Generator:
    """
    Generador automatico de sopas de letras.

    A diferencia del crucigrama, las palabras no necesitan
    cruzarse entre si: cada una se coloca en linea recta,
    en una direccion permitida segun la dificultad elegida,
    y el resto del tablero se rellena con letras aleatorias.
    """

    # Letras usadas para el relleno (sin acentos ni Ñ).
    LETRAS_RELLENO = string.ascii_uppercase

    # Direcciones permitidas segun el nivel de dificultad.
    # FACIL: solo hacia adelante, mas facil de detectar a simple vista.
    # MEDIO: suma un par de direcciones invertidas.
    # DIFICIL: las 8 direcciones completas.
    DIRECCIONES_POR_DIFICULTAD = {
        "facil": [
            Direction.HORIZONTAL,
            Direction.VERTICAL,
            Direction.DIAGONAL_ABAJO_DERECHA,
        ],
        "medio": [
            Direction.HORIZONTAL,
            Direction.HORIZONTAL_INVERSA,
            Direction.VERTICAL,
            Direction.VERTICAL_INVERSA,
            Direction.DIAGONAL_ABAJO_DERECHA,
            Direction.DIAGONAL_ABAJO_IZQUIERDA,
        ],
        "dificil": list(Direction),
    }

    # Intentos maximos para regenerar SOLO el relleno si se detecta
    # una palabra accidental duplicada.
    MAX_INTENTOS_RELLENO = 30

    # Intentos maximos de regenerar el TABLERO COMPLETO desde cero
    # si no se lograron colocar todas las palabras.
    MAX_INTENTOS_TABLERO = 20

    def __init__(self, rows=15, cols=15, max_attempts=200, dificultad="dificil"):
        self.board = Board(rows, cols)
        self.words = []
        self.max_attempts = max_attempts
        self.set_dificultad(dificultad)

    # =====================================================
    # CONFIGURACION
    # =====================================================

    def set_dificultad(self, dificultad):
        """
        Establece el nivel de dificultad, que determina que
        direcciones estan permitidas para colocar palabras.
        """

        if dificultad not in self.DIRECCIONES_POR_DIFICULTAD:
            raise ValueError(
                f"Dificultad '{dificultad}' invalida. "
                f"Usar: {list(self.DIRECCIONES_POR_DIFICULTAD.keys())}"
            )

        self.dificultad = dificultad
        self.direcciones_permitidas = self.DIRECCIONES_POR_DIFICULTAD[dificultad]

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
        Genera la sopa de letras completa, reintentando el
        tablero desde cero (con nuevas posiciones aleatorias)
        hasta lograr colocar el 100% de las palabras, o hasta
        agotar MAX_INTENTOS_TABLERO.

        Si ningun intento logra el 100%, se conserva el mejor
        resultado obtenido (el que coloco mas palabras).

        Devuelve True si se colocaron todas las palabras,
        False si el mejor intento quedo incompleto (en ese
        caso, usar words_not_placed() para ver cuales faltaron).
        """

        mejor_board = None
        mejor_cantidad = -1

        for _ in range(self.MAX_INTENTOS_TABLERO):

            if self._generar_un_intento():
                # Se colocaron todas las palabras: listo.
                self._rellenar_sin_duplicados()
                return True

            # Este intento quedo incompleto; nos quedamos con
            # el mejor hasta ahora por si hace falta usarlo.
            if self.board.word_count() > mejor_cantidad:
                mejor_cantidad = self.board.word_count()
                mejor_board = self.board

        # Ningun intento logro el 100%: usamos el mejor obtenido.
        self.board = mejor_board
        self._rellenar_sin_duplicados()

        return False

    def _generar_un_intento(self):
        """
        Hace UN intento de colocar todas las palabras en un
        tablero nuevo y vacio. Devuelve True si se lograron
        colocar todas.
        """

        self.board = Board(self.board.rows, self.board.cols)

        todas_colocadas = True

        for word in self.words:
            if not self._colocar_palabra(word):
                todas_colocadas = False

        return todas_colocadas

    def _colocar_palabra(self, word):
        """
        Intenta colocar una palabra en una posicion aleatoria,
        usando solo direcciones permitidas por la dificultad.
        """

        for _ in range(self.max_attempts):

            direction = random.choice(self.direcciones_permitidas)
            row = random.randint(0, self.board.rows - 1)
            col = random.randint(0, self.board.cols - 1)

            if self.board.can_place_word(row, col, word, direction):
                self.board.place_word(row, col, word, direction)
                return True

        return False

    def _rellenar_sin_duplicados(self):
        """
        Rellena las celdas vacias con letras aleatorias,
        verificando que no se forme una copia adicional de
        alguna de las palabras buscadas. Si se detecta una
        copia accidental, se regenera solo el relleno.
        """

        celdas_vacias = [
            (row, col)
            for row in range(self.board.rows)
            for col in range(self.board.cols)
            if self.board.is_empty(row, col)
        ]

        for _ in range(self.MAX_INTENTOS_RELLENO):

            for row, col in celdas_vacias:
                letra = random.choice(self.LETRAS_RELLENO)
                self.board.set_cell(row, col, letra)

            if not self._hay_palabras_duplicadas():
                return True

        # Si tras varios intentos sigue habiendo duplicados,
        # se deja el ultimo relleno generado (caso muy raro).
        return False

    def _hay_palabras_duplicadas(self):
        """
        Revisa si alguna palabra de la lista aparece mas veces
        de las que fue colocada intencionalmente (es decir, si
        el relleno aleatorio formo una copia accidental).
        """

        for word in self.words:
            apariciones_esperadas = sum(
                1 for p in self.board.placements if p["word"] == word
            )

            if self._contar_apariciones(word) > apariciones_esperadas:
                return True

        return False

    def _contar_apariciones(self, word):
        """
        Cuenta cuantas veces aparece una palabra en el tablero
        completo, en cualquiera de las 8 direcciones posibles
        (independientemente de la dificultad configurada).
        """

        total = 0

        for row in range(self.board.rows):
            for col in range(self.board.cols):
                for direction in Direction:
                    if self._coincide_en(row, col, word, direction):
                        total += 1

        return total

    def _coincide_en(self, row, col, word, direction):
        """
        Verifica si la palabra aparece exactamente en esa
        posicion y direccion (sin usar can_place_word, ya que
        aqui solo queremos LEER, no validar para colocar).
        """

        dr, dc = direction.value
        current_row, current_col = row, col

        for letter in word:

            if not self.board.is_inside(current_row, current_col):
                return False

            if self.board.get_cell(current_row, current_col) != letter:
                return False

            current_row += dr
            current_col += dc

        return True

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

    # =====================================================
    # DATOS PARA EXPORTAR (uso futuro del armador de PDF)
    # =====================================================

    def to_grid(self):
        """
        Devuelve la cuadricula completa como una matriz 2D de
        letras (lista de listas), lista para dibujarse en una
        pagina del libro.
        """

        grid = []

        for row in range(self.board.rows):
            fila = []
            for col in range(self.board.cols):
                fila.append(self.board.get_cell(row, col))
            grid.append(fila)

        return grid

    def get_word_paths(self):
        """
        Devuelve, para cada palabra colocada, la lista exacta
        de coordenadas (fila, columna) que ocupa en el tablero.

        Util para dibujar la pagina de soluciones, marcando
        o resaltando cada palabra encontrada.

        Formato:
        [
            {"word": "MOISES", "coords": [(fila, col), (fila, col), ...]},
            ...
        ]
        """

        rutas = []

        for placement in self.board.placements:

            dr, dc = placement["direction"].value
            row, col = placement["row"], placement["col"]

            coords = []
            current_row, current_col = row, col

            for _ in placement["word"]:
                coords.append((current_row, current_col))
                current_row += dr
                current_col += dc

            rutas.append({
                "word": placement["word"],
                "coords": coords,
            })

        return rutas
