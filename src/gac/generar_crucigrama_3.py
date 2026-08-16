import os
from .generator import Generator
from .web_exporter import WebExporter
from .exporter import Exporter

# Datos del crucigrama 3 de la Semana 02: Vocabulario
datos_crucigrama_3 = {
    "title": "La Importancia de la Comprensión Espiritual",
    "tema": "Familia léxica de comprender y la asimilación de la verdad",
    "slug": "vocabulario_comprender",
    "resena": (
        "<h3>I. Introducción: Escuchar versus Comprender</h3>"
        "<p>Vivimos rodeados de información. Cada día escuchamos conversaciones, leemos mensajes y recibimos una enorme cantidad de ideas. "
        "Sin embargo, oír información no significa comprenderla. Una persona puede escuchar una explicación completa, repetirla de memoria "
        "y aun así no haber captado realmente su significado ni permitir que transforme su manera de pensar y vivir.</p>"

        "<h3>II. El Valor Bíblico del Entendimiento</h3>"
        "<p>La Biblia le da un valor enorme a la comprensión. Dios no sólo desea que escuchemos su Palabra, sino que la entendamos, la meditemos y la pongamos en práctica. "
        "Jesús enseñó que muchos oían sus palabras, pero no las comprendían; en cambio, quienes las recibían con entendimiento daban fruto abundante.</p>"
        "<blockquote style='margin: 15px 0; padding: 10px 15px; border-left: 4px solid #2b5797; background-color: #f3f3f3;'>"
        "<b>Mateo 13:23:</b> «Mas el que fue sembrado en buena tierra, este es el que oye y entiende la palabra, y da fruto; y produce a ciento, a sesenta, y a treinta por uno.»"
        "</blockquote>"

        "<h3>III. La Comprensión y el Crecimiento Espiritual</h3>"
        "<p>Comprender implica reconocer relaciones entre ideas, descubrir propósitos y aplicar la verdad a la vida diaria. "
        "Por esta razón, desarrollar la capacidad de comprensión es una parte fundamental del crecimiento espiritual. "
        "Ampliar nuestro vocabulario nos da matices nuevos para expresar la verdad, interpretar correctamente las Escrituras y comunicar con claridad lo que creemos.</p>"

        "<h3>IV. Propósito del Crucigrama y Aplicación Práctica</h3>"
        "<p>Este crucigrama no pretende solo aumentar vocabulario, sino ayudar a ejercitar la observación, la reflexión y el análisis. "
        "Cada palabra encontrada es una oportunidad para ampliar el pensamiento y comprender mejor la Palabra de Dios. "
        "Escuchar mejor, reflexionar con calma y permitir que la verdad moldee nuestra forma de vivir es, en el fondo, el objetivo. "
        "Al resolver este crucigrama, pregúntate qué aporta cada palabra al sentido de esta familia léxica de «comprender» y cómo puedes usarla en tus conversaciones y estudio bíblico.</p>"
    ),
    "rows": 20,
    "cols": 20,
    "words": [
        "COMPRENSION", "COMPRENSIBLE", "INCOMPRENSION", "ENTENDIMIENTO", "INTERPRETACION",
        "ANALISIS", "ASIMILAR", "REFLEXIONAR", "RAZONAR", "EXPLICAR",
        "ACLARAR", "CONOCIMIENTO", "ASIMILACION", "MEDITAR", "PONDERAR",
        "DESCIFRAR", "ILUSTRAR", "SINTETIZAR", "CAPACITAR", "ESCLARECER"
    ],
    "clues": {
        "COMPRENSION": "Capacidad de entender correctamente lo que se estudia o escucha.",
        "COMPRENSIBLE": "Que puede entenderse con facilidad.",
        "INCOMPRENSION": "Falta de entendimiento o dificultad para captar un mensaje.",
        "ENTENDIMIENTO": "Facultad de razonar y comprender las cosas.",
        "INTERPRETACION": "Explicación que se da al sentido de algo.",
        "ANALISIS": "Estudio detallado de un asunto o texto.",
        "ASIMILAR": "Incorporar un conocimiento hasta hacerlo propio.",
        "REFLEXIONAR": "Pensar con detenimiento antes de sacar conclusiones.",
        "RAZONAR": "Relacionar ideas de forma lógica para llegar a una conclusión.",
        "EXPLICAR": "Hacer que algo sea entendido con claridad.",
        "ACLARAR": "Quitar dudas o hacer más comprensible un asunto.",
        "CONOCIMIENTO": "Resultado de haber comprendido y aprendido una verdad o información.",
        "ASIMILACION": "Proceso de integrar profundamente una verdad hasta convertirla en parte de la propia vida.",
        "MEDITAR": "Considerar detenidamente y en silencio una verdad espiritual para aplicarla al corazón.",
        "PONDERAR": "Examinar con cuidado y peso el valor de una idea antes de tomar una decisión.",
        "DESCIFRAR": "Llegar a penetrar o comprender el sentido de un mensaje complejo o velado.",
        "ILUSTRAR": "Hacer más comprensible un concepto mediante ejemplos, explicaciones o metáforas.",
        "SINTETIZAR": "Resumir y organizar las ideas principales de un asunto para comprender su esencia.",
        "CAPACITAR": "Preparar la mente o el entendimiento para comprender y aplicar la verdad.",
        "ESCLARECER": "Traer luz sobre un tema oscuro o confuso para facilitar su entendimiento."
    }
}

# --- RUTA PARA LA SEMANA 2 ---
output_dir = "docs/semana-02"
os.makedirs(output_dir, exist_ok=True)

# Generar crucigrama
gen = Generator(
    rows=datos_crucigrama_3["rows"],
    cols=datos_crucigrama_3["cols"]
)
gen.set_words(datos_crucigrama_3["words"])
resultado = gen.generate()

# Exportar HTMLs
web = WebExporter(
    resultado,
    title=datos_crucigrama_3["title"],
    tema=datos_crucigrama_3["tema"],
    clues=datos_crucigrama_3["clues"],
    resena=datos_crucigrama_3["resena"]
)
web.save(os.path.join(output_dir, f"crucigrama_{datos_crucigrama_3['slug']}_web.html"))

estatico = Exporter(
    resultado,
    title=datos_crucigrama_3["title"],
    subtitle=datos_crucigrama_3["tema"],
    clues=datos_crucigrama_3["clues"],
    resena=datos_crucigrama_3["resena"]
)
estatico.save(os.path.join(output_dir, f"crucigrama_{datos_crucigrama_3['slug']}.html"))

print("✅ Archivos creados correctamente en la carpeta 'docs/semana-02/'.")