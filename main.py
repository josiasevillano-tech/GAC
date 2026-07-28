import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gac'))

from generator import Generator
from exporter import Exporter


def main():
    """Punto de entrada del GAC."""

    # ── CONFIGURACIÓN ──────────────────────────────
    words = [
        "ABRAHAM", "MOISES", "DAVID", "JOSE", "MARIA",
        "PEDRO", "PABLO", "JESUS", "ISAIAS", "DANIEL",
        "ESTER", "RUTH", "SARA", "REBECA", "LEAH",
        "NOE", "ADAN", "EVA", "JONAS", "SAMUEL"
    ]

    # Tablero ajustado para A4: ancho suficiente pero no excesivo
    rows = 12
    cols = 22
    max_attempts = 80
    output_file = "crucigrama.html"
    title = "Guía de Estudio: Personajes Bíblicos"
    # ───────────────────────────────────────────────

    print("=" * 50)
    print("  GENERADOR AUTOMÁTICO DE CRUCIGRAMAS (GAC)")
    print("=" * 50)
    print()

    generator = Generator(rows=rows, cols=cols)
    generator.set_words(words)

    print(f"Generando crucigrama ({max_attempts} intentos)...")
    print(f"Dimensiones: {rows} filas × {cols} columnas")
    print()

    success = generator.generate_with_backtracking(max_attempts=max_attempts)

    if not success:
        print("❌ No se pudo generar el crucigrama.")
        return

    data = generator.get_crossword_data()

    if data is None:
        print("❌ No hay datos para exportar.")
        return

    exporter = Exporter(data, title=title)
    filepath = exporter.save(output_file)

    print()
    print("=" * 50)
    print("  INSTRUCCIONES")
    print("=" * 50)
    print(f"1. Abre el archivo en Word:")
    print(f"   {filepath}")
    print()
    print("2. En Word, ajusta márgenes si es necesario.")
    print()
    print("3. Reemplaza las líneas en las pistas por tus")
    print("   definiciones didácticas.")
    print()
    print("4. Imprime a PDF (2 páginas).")
    print("=" * 50)


if __name__ == "__main__":
    main()