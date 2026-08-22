import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gac.generator import Generator
from gac.exporter import Exporter
from gac.web_exporter import WebExporter
from gac.boletin_exporter import BoletinExporter

# ============================================================
# CONFIGURACION: ruta al archivo JSON de la guia
# ============================================================
GUIA_JSON = os.path.join(os.path.dirname(__file__), "data", "semana_03.json")

FORZAR = "--forzar" in sys.argv
argumentos_json = [a for a in sys.argv[1:] if not a.startswith("--")]
if argumentos_json:
    GUIA_JSON = os.path.abspath(argumentos_json[0])

TIPOS_CRUCIGRAMA = {"sermon", "personaje_biblico", "libro_biblico", "vocabulario"}


def load_guia(path):
    """Carga la guia desde un archivo JSON."""
    with open(path, "r", encoding="utf-8") as f2:
        return json.load(f2)


def generar_bloque_crucigrama(idx, bloque, output_dir):
    """Genera un crucigrama a partir de un bloque (sermon/personaje/libro/vocabulario)."""
    tipo = bloque["tipo"]
    crucigrama_cfg = bloque["crucigrama"]
    tema = crucigrama_cfg["tema"]
    resena_raw = bloque["resena"]
    if isinstance(resena_raw, list):
        resena = "\n\n".join(resena_raw)
    else:
        resena = resena_raw
    words_data = crucigrama_cfg["words"]
    rows = crucigrama_cfg.get("rows", 15)
    cols = crucigrama_cfg.get("cols", 20)
    max_attempts = crucigrama_cfg.get("max_attempts", 200)

    print("\n" + "=" * 60)
    print(f"Generando bloque {idx} ({tipo}): {tema}")
    print("=" * 60)

    words = [item["word"] for item in words_data]
    word_clue_map = {item["word"]: item["clue"] for item in words_data}

    generator = Generator(rows=rows, cols=cols)
    generator.set_words(words)
    success = generator.generate_with_backtracking(max_attempts=max_attempts)

    if not success:
        print(f"  ERROR: No se pudo generar el crucigrama del bloque {idx}")
        return False

    data = generator.get_crossword_data()
    if data is None:
        print(f"  ERROR: No se obtuvieron datos del crucigrama del bloque {idx}")
        return False

    placed = data.get("metrics", {}).get("word_count", 0)
    total = len(words)
    print(f"  Palabras colocadas: {placed} de {total}")

    clues = word_clue_map

    # --- Titulo y sello segun el tipo de bloque ---
    if tipo == "sermon":
        pastor = bloque["pastor"]
        titulo = bloque["titulo"]
        sello = f"PREDICACIÓN DEL PASTOR {pastor.upper()}"
        title = titulo
    else:
        sello = None
        title = tema

    exporter = Exporter(data, title=title, clues=clues, resena=resena, sello=sello)
    print_path = os.path.join(output_dir, f"crucigrama_{idx}.html")
    exporter.save(print_path)
    print(f"  Exportado: {print_path}")

    web_exporter = WebExporter(data, title, clues, resena, tema, sello=sello)
    web_path = os.path.join(output_dir, f"crucigrama_{idx}_web.html")
    web_exporter.save(web_path)
    print(f"  Exportado: {web_path}")

    return True


def generar_bloque_boletin(idx, bloque, output_dir):
    """Genera la pagina del bloque tipo 'boletin' (no es un crucigrama)."""
    titulo = bloque["titulo"]
    introduccion = bloque.get("introduccion", "")
    actividades = bloque["actividades"]

    print("\n" + "=" * 60)
    print(f"Generando bloque {idx} (boletin): {titulo}")
    print("=" * 60)

    boletin_exporter = BoletinExporter(titulo=titulo, introduccion=introduccion, actividades=actividades)
    web_path = os.path.join(output_dir, f"boletin_{idx}_web.html")
    boletin_exporter.save(web_path)
    print(f"  Exportado: {web_path}")

    return True


def generate_and_export(idx, bloque, output_dir):
    """Genera un bloque, decidiendo la ruta segun su tipo."""
    tipo = bloque["tipo"]
    if tipo in TIPOS_CRUCIGRAMA:
        return generar_bloque_crucigrama(idx, bloque, output_dir)
    elif tipo == "boletin":
        return generar_bloque_boletin(idx, bloque, output_dir)
    else:
        print(f"  ERROR: Tipo de bloque desconocido: {tipo!r}")
        return False


def _texto_boton_para_bloque(idx, bloque):
    """Arma el texto descriptivo del boton, segun el tipo de bloque.
    Sigue el mismo estilo que ya usan docs/semana-01 y docs/semana-02:
    el texto del boton ES el nombre descriptivo, sin palabras genericas
    como 'Jugar'."""
    tipo = bloque["tipo"]

    if tipo == "sermon":
        pastor = bloque["pastor"]
        titulo = bloque["titulo"]
        texto = f"Predicación del Pastor {pastor}: {titulo}"
        href = f"crucigrama_{idx}_web.html"
    elif tipo in TIPOS_CRUCIGRAMA:
        tema = bloque["crucigrama"]["tema"]
        texto = tema
        href = f"crucigrama_{idx}_web.html"
    elif tipo == "boletin":
        texto = bloque["titulo"]
        href = f"boletin_{idx}_web.html"
    else:
        texto = "Bloque desconocido"
        href = "#"

    return texto, href


def generate_semana_index(guia_data, output_dir, carpeta):
    """
    Genera el index.html propio de la carpeta de la semana (docs/semana-0N/),
    siguiendo el mismo diseño que ya usan semana-01 y semana-02 (sin acordeon,
    sin 'Jugar', boton = texto descriptivo completo).

    IMPORTANTE: esta funcion NUNCA toca docs/index.html (el hub principal).
    Ese archivo se sigue actualizando a mano, como ya se ha hecho hasta ahora.
    """
    guia_numero = guia_data["guia_numero"]
    bloques = guia_data["bloques"]

    botones_html = []
    for i, bloque in enumerate(bloques, 1):
        texto, href = _texto_boton_para_bloque(i, bloque)
        botones_html.append(f'            <a class="btn" href="{href}">{texto}</a>')
    botones_html_str = "\n".join(botones_html)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Semana {guia_numero} — Iglesia Agua Viva</title>

    <style>
        :root {{
            --primario: #2c5282;
            --secundario: #3182ce;
            --fondo: #f5f7fa;
            --card: #ffffff;
            --texto: #2d3748;
            --borde: #e2e8f0;
            --sombra: 0 2px 8px rgba(0,0,0,0.08);
            --radio: 12px;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
            background: var(--fondo);
            color: var(--texto);
            padding: 24px 16px;
            min-height: 100vh;
            line-height: 1.6;
        }}
        .contenedor {{ max-width: 800px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 36px; }}
        header h1 {{ color: var(--primario); font-size: 1.9rem; margin-bottom: 6px; }}
        header p {{ color: #718096; font-size: 1.05rem; }}
        .resena {{
            background: #f7fafc;
            border-left: 4px solid var(--secundario);
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
            font-size: 0.95rem;
            color: #4a5568;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }}
        .btn {{
            display: block;
            text-align: center;
            padding: 14px;
            background: var(--secundario);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
            font-size: 0.9rem;
        }}
        .btn:hover {{ background: #2b6cb0; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
        .volver {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 20px;
            color: var(--primario);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        .volver:hover {{ text-decoration: underline; }}
        footer {{
            text-align: center;
            margin-top: 48px;
            padding-top: 24px;
            border-top: 1px solid var(--borde);
            color: #a0aec0;
            font-size: 0.85rem;
        }}
        @media (max-width: 480px) {{
            header h1 {{ font-size: 1.5rem; }}
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <a class="volver" href="../index.html">← Volver al inicio</a>

        <header>
            <h1>Iglesia Agua Viva</h1>
            <p>Escuela del Pensamiento — Semana {guia_numero}</p>
        </header>

        <div style="background: var(--card); border-radius: var(--radio); padding: 24px; box-shadow: var(--sombra);">
            <h2 style="color: var(--primario); margin-bottom: 12px;">📝 Reseña del tema</h2>
            <div class="resena">
                <em>Reseña del tema próximamente...</em>
            </div>

            <h2 style="color: var(--primario); margin: 20px 0 12px;">🎯 Contenido de la semana</h2>
            <div class="grid">
{botones_html_str}
            </div>
        </div>

        <footer>
            Iglesia Agua Viva — <a href="../index.html" style="color: var(--secundario);">Ver todas las semanas</a>
        </footer>
    </div>
</body>
</html>"""

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f2:
        f2.write(html)
    print(f"\n  Generado: {index_path}")
    print(f"  NOTA: docs/index.html (el hub principal) NO fue modificado.")
    print(f"        Recuerda actualizarlo a mano para enlazar la carpeta '{carpeta}'.")


# ============================================================
# PUNTO DE ENTRADA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    guia = load_guia(GUIA_JSON)
    iglesia = guia["iglesia"]
    guia_numero = guia["guia_numero"]
    carpeta = f"semana-{guia_numero:02d}"
    output_dir = os.path.join("docs", carpeta)

    print("=" * 60)
    print(f"GAC - Guia {guia_numero} - Iglesia {iglesia}")
    print(f"Carpeta de salida: {output_dir}")
    print("=" * 60)

    if os.path.isdir(output_dir) and not FORZAR:
        print(f"\nERROR: {output_dir} ya existe.")
        print("No se sobrescribira para proteger contenido ya generado/publicado.")
        print(f"Si de verdad quieres regenerarlo, corre de nuevo agregando --forzar")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    resultados = []
    for i, bloque in enumerate(guia["bloques"], 1):
        resultados.append(generate_and_export(i, bloque, output_dir))

    generate_semana_index(guia, output_dir, carpeta)

    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    for i, (ok, bloque) in enumerate(zip(resultados, guia["bloques"]), 1):
        estado = "OK" if ok else "FALLIDO"
        print(f"  Bloque {i} ({bloque['tipo']}): {estado}")
    print(f"\nArchivos generados en la carpeta {output_dir}/")
    print(f"Listo para: git add {output_dir}/ && git commit && git push")
    print("\nRECORDATORIO: actualiza docs/index.html a mano para enlazar esta semana.")
