import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gac'))

from generator import Generator
from exporter import Exporter


def main():
    """Punto de entrada del GAC."""

    # ── CONFIGURACIÓN ──────────────────────────────

    # Lista de palabras para el crucigrama
    words = [
        "ABRAHAM", "MOISES", "DAVID", "JOSE", "MARIA",
        "PEDRO", "PABLO", "JESUS", "ISAIAS", "DANIEL",
        "ESTER", "RUTH", "SARA", "REBECA", "LEAH",
        "NOE", "ADAN", "EVA", "JONAS", "SAMUEL"
    ]

    # DICCIONARIO DE PISTAS: cada palabra tiene su definición didáctica.
    # Si una palabra no está en este diccionario, aparecerá con línea en blanco.
    # Puedes agregar, quitar o modificar las definiciones aquí.
    clues = {
        "ABRAHAM": "Padre de la fe, llamado por Dios a dejar Ur de los caldeos.",
        "MOISES": "Líder que guió la salida de Egipto y recibió los Diez Mandamientos.",
        "DAVID": "Rey de Israel, vencedor de Goliat y compositor de salmos.",
        "JOSE": "Hijo predilecto de Jacob, vendido por sus hermanos a Egipto.",
        "MARIA": "Madre de Jesús, escogida por Dios para concebir al Mesías.",
        "PEDRO": "Pescador galileo, líder de los apóstoles y fundador de la Iglesia.",
        "PABLO": "Apóstol de los gentiles, autor de la mayoría de las epístolas.",
        "JESUS": "Hijo de Dios, Salvador del mundo, crucificado y resucitado.",
        "ISAIAS": "Gran profeta del Antiguo Testamento que anunció al Mesías.",
        "DANIEL": "Joven hebreo que interpretó sueños en la corte de Babilonia.",
        "ESTER": "Reina judía que salvó a su pueblo de la masacre en Persia.",
        "RUTH": "Moabita que se convirtió a Dios y fue bisabuela de David.",
        "SARA": "Esposa de Abraham, madre de Isaac en su vejez.",
        "REBECA": "Esposa de Isaac, madre de Esaú y Jacob.",
        "LEAH": "Primera esposa de Jacob, madre de seis de sus hijos.",
        "NOE": "Justo que construyó el arca para salvar a su familia del diluvio.",
        "ADAN": "Primer ser humano creado por Dios, padre de la humanidad.",
        "EVA": "Primera mujer, formada de la costilla de Adán.",
        "JONAS": "Profeta que predicó en Nínive después de tres días en el vientre de un gran pez.",
        "SAMUEL": "Último juez de Israel, quien ungió a Saúl y a David como reyes.",
    }

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

    # Pasar el diccionario de pistas al exporter
    exporter = Exporter(data, title=title, clues=clues)
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
    print("3. Las pistas ya llevan las definiciones didácticas.")
    print("   Si quieres modificarlas, edita el diccionario 'clues'")
    print("   en main.py y vuelve a ejecutar.")
    print()
    print("4. Imprime a PDF (2 páginas).")
    print("=" * 50)


if __name__ == "__main__":
    main()