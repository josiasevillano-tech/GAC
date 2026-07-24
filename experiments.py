import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gac'))

from generator import Generator
from metrics import Metrics


def run_single_attempt(words, weight_compactness, weight_intersections):
    """
    Ejecuta UNA generación con pesos específicos y devuelve métricas.
    """
    generator = Generator()
    generator.weight_compactness = weight_compactness
    generator.weight_intersections = weight_intersections
    generator.set_words(words)
    generator.generate()

    metrics = Metrics(generator.board)

    return {
        "words": metrics.word_count(),
        "crosses": metrics.cross_count(),
        "area": metrics.bounding_area(),
        "density": metrics.density()
    }


def run_experiment(words, weight_compactness, weight_intersections, attempts=10):
    """
    Ejecuta múltiples intentos con los mismos pesos y devuelve el mejor resultado.
    """
    best_result = None
    best_score = -1

    for attempt in range(attempts):
        result = run_single_attempt(words, weight_compactness, weight_intersections)

        # Puntuación: más palabras, más cruces, menor área
        score = result["words"] * 100 + result["crosses"] * 10 - result["area"]

        if score > best_score:
            best_score = score
            best_result = result
            best_result["attempt"] = attempt + 1

    return best_result


def main():
    """
    Prueba diferentes combinaciones de pesos con múltiples intentos cada una.
    """
    words = [
        "CONSTITUCIÓN", "ELEFANTE", "BIBLIOTECA", "ASTRONOMÍA",
        "CASA", "LUNA", "SOL", "SAL", "ALA", "SALA", "MAR", "LUZ",
        "RÍO", "MONTAÑA", "ESTRELLA", "PLANETA", "GALAXIA"
    ]

    # Diferentes configuraciones de pesos a probar
    configs = [
        (1, 1),   # Balanceado
        (2, 1),   # Más peso a compacidad
        (1, 2),   # Más peso a intersecciones
        (3, 1),   # Mucho peso a compacidad
        (1, 3),   # Mucho peso a intersecciones
        (2, 3),   # Favor intersecciones
        (3, 2),   # Favor compacidad
    ]

    attempts_per_config = 10

    print("=" * 80)
    print("  EXPERIMENTOS DE OPTIMIZACIÓN DE PESOS")
    print(f"  {attempts_per_config} intentos por configuración")
    print("=" * 80)
    print()

    results = []

    for compactness, intersections in configs:
        result = run_experiment(words, compactness, intersections, attempts_per_config)
        result["compactness"] = compactness
        result["intersections"] = intersections
        results.append(result)

        print(f"Config: C={compactness}, I={intersections} | "
              f"Mejor intento: #{result['attempt']} | "
              f"Palabras: {result['words']} | "
              f"Cruces: {result['crosses']} | "
              f"Área: {result['area']} | "
              f"Densidad: {result['density']:.2f}")

    print()
    print("=" * 80)
    print("  MEJOR CONFIGURACIÓN GLOBAL")
    print("=" * 80)

    # Encontrar la mejor configuración
    best = max(results, key=lambda r: (r['words'], r['crosses'], -r['area']))

    print(f"  Pesos: C={best['compactness']}, I={best['intersections']}")
    print(f"  Mejor intento: #{best['attempt']}")
    print(f"  Palabras: {best['words']}")
    print(f"  Cruces: {best['crosses']}")
    print(f"  Área: {best['area']}")
    print(f"  Densidad: {best['density']:.2f}")
    print("=" * 80)


if __name__ == "__main__":
    main()