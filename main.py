import sys
import os

# Añadir src/gac/ al path para importar los módulos directamente
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gac'))

from generator import Generator
from exporter import Exporter


def main():
    """
    Punto de entrada del GAC.
    Genera un crucigrama y lo exporta a HTML.
    """

    # ── CONFIGURACIÓN ──────────────────────────────
    words = [
        "ABRAHAM", "MOISES", "DAVID", "JOSE", "MARIA",
        "PEDRO", "PABLO", "JESUS", "ISAIAS", "DANIEL",
        "ESTER", "RUTH", "SARA", "REBECA", "LEAH",
        "NOE", "ADAN", "EVA", "JONAS", "SAMUEL"
    ]

    rows = 20
    cols = 20
    max_attempts = 50
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
    print(f"1. Abre el archivo en tu navegador:")
    print(f"   {filepath}")
    print()
    print("2. Para editar en Word:")
    print("   Abre Word → Archivo → Abrir → selecciona el HTML")
    print()
    print("3. Reemplaza las palabras en las pistas por tus")
    print("   definiciones didácticas.")
    print()
    print("4. Imprime a PDF cuando esté listo.")
    print("=" * 50)


if __name__ == "__main__":
    main()