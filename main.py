# ==============================================================================
# IMPORTS
# ==============================================================================
from src.gac.board import Board
from src.gac.direction import Direction
from src.gac.generator import Generator


# ==============================================================================
# INSPECCIÓN DE BOARD (TABLERO, CASILLAS, LÍMITES, LECTURA / ESCRITURA Y MÉTODOS)
# ==============================================================================
board = Board()

print("=== INSPECCIÓN DEL TABLERO ===")
print("Filas:", board.rows)
print("Columnas:", board.cols)
print("Casillas:", board.cells)
print("Palabras:", board.placements)

print()
print("=== INSPECCIÓN DE CASILLAS ===")
print("(5,8):", board.is_empty(5, 8))
print("(10,3):", board.is_empty(10, 3))

print()
print("=== INSPECCIÓN DE LÍMITES ===")
print("(0,0):", board.is_inside(0, 0))
print("(7,8):", board.is_inside(7, 8))
print("(14,14):", board.is_inside(14, 14))
print("(15,14):", board.is_inside(15, 14))
print("(-1,8):", board.is_inside(-1, 8))
print("(8,15):", board.is_inside(8, 15))

print()
print("=== INSPECCIÓN DE ESCRITURA ===")
board.set_cell(7, 5, "A")
print(board.cells)
print("(7,5):", board.is_empty(7, 5))

print()
print("=== INSPECCIÓN DE LECTURA ===")
print("(7,5):", board.get_cell(7, 5))
print("(2,2):", board.get_cell(2, 2))


# ==============================================================================
# INSPECCIÓN DE DIRECTION
# ==============================================================================
print()
print("=== INSPECCIÓN DE DIRECTION ===")
print(Direction.HORIZONTAL)
print(Direction.VERTICAL)


# ==============================================================================
# INSPECCIÓN DE REGLAS DE COLOCACIÓN Y CRUCES (CAN_PLACE_WORD)
# ==============================================================================
print()
print("=== INSPECCIÓN DE can_place_word ===")
print(
    board.can_place_word(
        7,
        5,
        "CASA",
        Direction.HORIZONTAL
    )
)

print()
print("=== INSPECCIÓN DE can_place_word ===")
print(
    board.can_place_word(
        7,
        5,
        "CASA",
        Direction.HORIZONTAL
    )
)
print(
    board.can_place_word(
        14,
        13,
        "CASA",
        Direction.HORIZONTAL
    )
)

print()
print("=== INSPECCIÓN DE CASILLA OCUPADA ===")
board = Board()
board.set_cell(7, 6, "X")
print(board.can_place_word(
    7,
    5,
    "CASA",
    Direction.HORIZONTAL
))

print()
print("=== INSPECCIÓN DE CRUCE CORRECTO ===")
board = Board()
board.set_cell(7, 6, "A")
print(
    board.can_place_word(
        7,
        5,
        "CASA",
        Direction.HORIZONTAL
    )
)

print()
print("=== INSPECCIÓN DE CRUCE INCORRECTO ===")
board = Board()
board.set_cell(7, 6, "X")
print(
    board.can_place_word(
        7,
        5,
        "CASA",
        Direction.HORIZONTAL
    )
)


# ==============================================================================
# INSPECCIÓN DE OPERACIONES EN BOARD (PLACE, CLEAR, CLONE)
# ==============================================================================
print()
print("=== INSPECCIÓN DE place_word ===")
board = Board()
result = board.place_word(
    7,
    5,
    "CASA",
    Direction.HORIZONTAL
)
print(result)
print(board.cells)
print(board.placements)

print()
board = Board()
result = board.place_word(
    14,
    13,
    "CASA",
    Direction.HORIZONTAL
)
print(result)
print(board.cells)
print(board.placements)

print()
print("=== INSPECCIÓN DE clear ===")
board = Board()
board.place_word(
    7,
    5,
    "CASA",
    Direction.HORIZONTAL
)
print("Antes:")
print(board.cells)
print(board.placements)

board.clear()
print()
print("Después:")
print(board.cells)
print(board.placements)

print()
print("=== INSPECCIÓN DE clone ===")
board = Board()
board.place_word(
    7,
    5,
    "CASA",
    Direction.HORIZONTAL
)
copy_board = board.clone()
copy_board.place_word(
    4,
    6,
    "LUNA",
    Direction.VERTICAL
)
print("Original:")
print(board.cells)
print()
print("Copia:")
print(copy_board.cells)


# ==============================================================================
# INSPECCIÓN DE MÉTRICAS Y ÁREAS (WORD_COUNT, BOUNDING BOX / AREA)
# ==============================================================================
print()
print("=== INSPECCIÓN DE word_count ===")
board = Board()
print(board.word_count())

board.place_word(
    7,
    5,
    "CASA",
    Direction.HORIZONTAL
)
print(board.word_count())

board.place_word(
    5,
    10,
    "SOL",
    Direction.VERTICAL
)
print(board.word_count())

print()
print("=== INSPECCIÓN DE bounding_box ===")
board = Board()
board.place_word(
    7,
    5,
    "CASA",
    Direction.HORIZONTAL
)
board.place_word(
    4,
    6,
    "LUNA",
    Direction.VERTICAL
)
print(board.bounding_box())

print()
print("=== INSPECCIÓN DE bounding_area ===")
board = Board()
board.place_word(
    7,
    5,
    "CASA",
    Direction.HORIZONTAL
)
board.place_word(
    4,
    6,
    "LUNA",
    Direction.VERTICAL
)
print(board.bounding_area())


# ==============================================================================
# INSPECCIÓN DE GENERATOR (INICIALIZACIÓN, LISTAS DE PALABRAS Y ORDENAMIENTO)
# ==============================================================================
print()
print("=== INSPECCIÓN DE Generator ===")
generator = Generator()
print(generator.board.rows)
print(generator.board.cols)
print(generator.board.word_count())

print()
print("=== INSPECCIÓN DE Generator ===")
generator = Generator()
print("Filas:", generator.board.rows)
print("Columnas:", generator.board.cols)
print("Palabras:", generator.board.word_count())

print()
print("=== INSPECCIÓN DE words ===")
generator = Generator()
print(generator.words)
print(len(generator.words))

print()
print("=== INSPECCIÓN DE set_words ===")
print()
print("=== INSPECCIÓN DE ORDENAMIENTO ===")
generator = Generator()
generator.set_words([
    "SOL",
    "CONSTITUCIÓN",
    "MAR",
    "LUNA",
    "CASA"
])
print(generator.words)


# ==============================================================================
# INSPECCIÓN DE HEURÍSTICAS Y MÉTODOS AUXILIARES DEL GENERATOR
# ==============================================================================
print()
print("=== INSPECCIÓN DE find_common_letters ===")
generator = Generator()
print(generator.find_common_letters("CASA", "SOL"))
print(generator.find_common_letters("CASA", "BARCA"))
print(generator.find_common_letters("CASA", "LUNA"))

print()
print("=== INSPECCIÓN DE find_letter_positions ===")
generator = Generator()
print(generator.find_letter_positions("CASA", "A"))
print(generator.find_letter_positions("CASA", "C"))
print(generator.find_letter_positions("CASA", "S"))
print(generator.find_letter_positions("CASA", "X"))

print()
print("=== INSPECCIÓN DE find_crosses ===")
generator = Generator()
for cross in generator.find_crosses("CASA", "LUNA"):
    print(cross)

print()
print("=== INSPECCIÓN DE compute_start_position ===")
generator = Generator()
print(
    generator.compute_start_position(
        7,
        5,
        Direction.HORIZONTAL,
        3,
        3
    )
)

print()
print("=== INSPECCIÓN DE find_candidate_positions ===")
generator = Generator()
generator.set_words([
    "CASA"
])
generator.generate()
placed = generator.board.placements[0]
candidates = generator.find_candidate_positions(
    placed,
    "LUNA"
)
print(candidates)


# ==============================================================================
# INSPECCIÓN DE EJECUCIÓN / GENERACIÓN DE CRUCIGRAMAS (GENERATE V0.2, V0.3 Y FINAL)
# ==============================================================================
print()
print("=== INSPECCIÓN DE generate v0.2 ===")
generator = Generator()
generator.set_words([
    "CASA",
    "LUNA",
    "SOL",
    "SAL",
    "ALA"
])
generator.generate()

print()
print("Cantidad:", generator.board.word_count())
for placement in generator.board.placements:
    print(placement)

print()
print("=== INSPECCIÓN DE generate v0.3 ===")
generator = Generator()
generator.set_words([
    "CASA",
    "LUNA",
    "SOL",
    "SAL",
    "ALA",
    "SALA"
])
generator.generate()

print("Cantidad:", generator.board.word_count())
for placement in generator.board.placements:
    print(placement)

print()
print("=== GENERADOR ===")
generator = Generator()
generator.set_words([
    "CASA",
    "LUNA"
])
generator.generate()