# Arquitectura del GAC

Versión: 0.3.4

## Objetivo

Generar crucigramas automáticos maximizando:

- cantidad de palabras
- número de cruces
- compacidad

---

## Estructura del proyecto

src/
│
├── board.py
├── generator.py
├── direction.py
└── ...

---

## Responsabilidad de cada módulo

board.py
    Representa el tablero.

generator.py
    Implementa el algoritmo de generación.

direction.py
    Define las orientaciones posibles.

...

---

## Arquitectura de Generator

CONSTRUCTOR
    __init__

CONFIGURACIÓN
    set_words
    is_word_placed

GENERACIÓN
    generate
    try_place_word

BÚSQUEDA DE CANDIDATOS
    find_common_letters
    find_letter_positions
    find_crosses
    compute_start_position
    find_candidate_positions

SELECCIÓN DE CANDIDATOS
    choose_best_candidate

EVALUACIÓN
    evaluate_candidate

HEURÍSTICAS
    score_compactness
    score_intersections