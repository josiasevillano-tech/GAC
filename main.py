import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gac'))

from generator import Generator
from exporter import Exporter
from web_exporter import WebExporter


def main():
    """Punto de entrada del GAC."""

    # ── CONFIGURACION ──────────────────────────────

    # Lista de palabras: Libros del Nuevo Testamento
    words = [
        "MATEO", "MARCOS", "LUCAS", "JUAN", "HECHOS",
        "ROMANOS", "CORINTIOS", "GALATAS", "EFESIOS", "FILIPENSES",
        "COLOSENSES", "TESALONICENSES", "TIMOTEO", "TITO", "FILEMON",
        "HEBREOS", "SANTIAGO", "PEDRO", "JUDAS", "APOCALIPSIS"
    ]

    # DICCIONARIO DE PISTAS: definiciones didacticas para cada libro
    clues = {
        "MATEO": "Evangelio escrito por el ex recaudador de impuestos que acompano a Jesus.",
        "MARCOS": "Evangelio mas corto, atribuido al discipulo de Pedro.",
        "LUCAS": "Evangelio escrito por el medico que tambien redacto Hechos.",
        "JUAN": "Evangelio del discipulo amado, que tambien escribio tres cartas.",
        "HECHOS": "Libro que narra la historia de la Iglesia primitiva tras la ascension.",
        "ROMANOS": "Carta magna de Pablo sobre la justificacion por la fe.",
        "CORINTIOS": "Dos cartas de Pablo a una iglesia dividida en una ciudad griega.",
        "GALATAS": "Carta donde Pablo defiende la libertad cristiana frente a la ley.",
        "EFESIOS": "Carta sobre la unidad de la Iglesia como cuerpo de Cristo.",
        "FILIPENSES": "Carta de alegria escrita desde la prision a una iglesia querida.",
        "COLOSENSES": "Carta que exalta la supremacia de Cristo sobre todo.",
        "TESALONICENSES": "Dos cartas sobre la segunda venida de Cristo y la esperanza.",
        "TIMOTEO": "Dos cartas pastorales de Pablo a su joven discipulo.",
        "TITO": "Carta pastoral sobre el orden de la iglesia en Creta.",
        "FILEMON": "Carta personal de Pablo pidiendo clemencia para un esclavo fugitivo.",
        "HEBREOS": "Carta que demuestra la superioridad de Cristo sobre el Antiguo Pacto.",
        "SANTIAGO": "Carta del hermano del Senor sobre la fe y las obras.",
        "PEDRO": "Dos cartas del apostol que nego a Jesus y luego murio martirizado.",
        "JUDAS": "Carta breve que advierte contra los falsos maestros.",
        "APOCALIPSIS": "Ultimo libro de la Biblia, vision del fin de los tiempos.",
    }

    # Tablero ajustado para A4: ancho suficiente para palabras largas
    rows = 15
    cols = 28
    max_attempts = 100
    output_file = "crucigrama.html"
    title = "Guia de Estudio: Libros del Nuevo Testamento"

    # NUEVO: Datos para la version web interactiva
    tema = "Historia Biblica"
    resena = (
        "El Nuevo Testamento es la segunda parte de la Biblia cristiana, "
        "compuesta por 27 libros escritos entre los siglos I y II d.C. "
        "Comienza con los cuatro evangelios (Mateo, Marcos, Lucas y Juan), "
        "continua con los Hechos de los Apostoles, las cartas de Pablo y otros apostoles, "
        "y culmina con el Apocalipsis. Estos textos fundamentaron la doctrina cristiana "
        "y han sido estudiados durante dos milenios como fuente de fe, moralidad y esperanza."
    )
    # ───────────────────────────────────────────────

    print("=" * 50)
    print("  GENERADOR AUTOMATICO DE CRUCIGRAMAS (GAC)")
    print("=" * 50)
    print()

    generator = Generator(rows=rows, cols=cols)
    generator.set_words(words)

    print(f"Generando crucigrama ({max_attempts} intentos)...")
    print(f"Dimensiones: {rows} filas x {cols} columnas")
    print(f"Palabras: {len(words)}")
    print()

    success = generator.generate_with_backtracking(max_attempts=max_attempts)

    if not success:
        print("X No se pudo generar el crucigrama.")
        return

    data = generator.get_crossword_data()

    if data is None:
        print("X No hay datos para exportar.")
        return

    # ── EXPORTAR VERSION PARA IMPRIMIR (Word / PDF) ──
    exporter = Exporter(data, title=title, clues=clues)
    filepath = exporter.save(output_file)

    # ── EXPORTAR VERSION WEB INTERACTIVA (nuevo) ──
    web_exporter = WebExporter(data, title=title, clues=clues, resena=resena, tema=tema)
    web_filepath = web_exporter.save("crucigrama_web.html")

    print()
    print("=" * 50)
    print("  INSTRUCCIONES")
    print("=" * 50)
    print(f"1. Abre el archivo en Word (para imprimir):")
    print(f"   {filepath}")
    print()
    print(f"2. Abre el archivo web (para jugar en celular):")
    print(f"   {web_filepath}")
    print("   Sube este archivo a GitHub Pages para compartirlo.")
    print()
    print("3. En Word, ajusta margenes si es necesario.")
    print()
    print("4. Las pistas ya llevan las definiciones didacticas.")
    print("   Si quieres modificarlas, edita el diccionario 'clues'")
    print("   en main.py y vuelve a ejecutar.")
    print()
    print("5. Imprime a PDF (2 paginas).")
    print("=" * 50)


if __name__ == "__main__":
    main()