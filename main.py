import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'gac'))

from generator import Generator
from exporter import Exporter
from web_exporter import WebExporter

# ============================================================
# CONFIGURACION: ruta al archivo JSON de la guia
# ============================================================
GUIA_JSON = os.path.join(os.path.dirname(__file__), "data", "semana_01.json")


def load_guia(path):
    """Carga la guia desde un archivo JSON."""
    with open(path, "r", encoding="utf-8") as f2:
        return json.load(f2)


def generate_and_export(idx, config, guia_numero):
    """Genera un crucigrama a partir de la configuracion y exporta ambas versiones."""
    tema = config["tema"]
    resena_raw = config["resena"]
    if isinstance(resena_raw, list):
        resena = "\n\n".join(resena_raw)
    else:
        resena = resena_raw
    words_data = config["words"]
    rows = config.get("rows", 15)
    cols = config.get("cols", 20)
    max_attempts = config.get("max_attempts", 200)

    print("\n" + "=" * 60)
    print(f"Generando crucigrama {idx}: {tema}")
    print("=" * 60)

    words = [item["word"] for item in words_data]
    word_clue_map = {item["word"]: item["clue"] for item in words_data}

    generator = Generator(rows=rows, cols=cols)
    generator.set_words(words)
    success = generator.generate_with_backtracking(max_attempts=max_attempts)

    if not success:
        print(f"  ERROR: No se pudo generar el crucigrama {idx}")
        return False

    data = generator.get_crossword_data()
    if data is None:
        print(f"  ERROR: No se obtuvieron datos del crucigrama {idx}")
        return False

    placed = data.get("metrics", {}).get("word_count", 0)
    total = len(words)
    print(f"  Palabras colocadas: {placed} de {total}")

    clues = word_clue_map
    title = f"Guia {guia_numero} - {tema}"

    exporter = Exporter(data, title=title, clues=clues, resena=resena)
    print_path = os.path.join("docs", f"crucigrama_{idx}.html")
    exporter.save(print_path)
    print(f"  Exportado: {print_path}")

    web_exporter = WebExporter(data, title, clues, resena, tema)
    web_path = os.path.join("docs", f"crucigrama_{idx}_web.html")
    web_exporter.save(web_path)
    print(f"  Exportado: {web_path}")

    return True


def generate_index(guia_data, resultados):
    """Genera la pagina principal index.html."""
    iglesia = guia_data["iglesia"]
    guia_numero = guia_data["guia_numero"]
    crucigramas = guia_data["crucigramas"]

    cards = []
    for i, config in enumerate(crucigramas, 1):
        num = str(i)
        dia = config["dia"]
        tema = config["tema"]
        cards.append(f"""
        <div class="card">
          <h3>{dia}</h3>
          <p class="tema">{tema}</p>
          <a href="crucigrama_{num}_web.html" class="btn-jugar">Jugar</a>
        </div>""")
    cards_html = "\n".join(cards)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Escuela del Pensamiento - Guia {guia_numero}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
      min-height: 100vh;
      color: #fff;
      padding: 20px;
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
      text-align: center;
    }}
    h1 {{
      font-size: 2.2rem;
      margin-bottom: 5px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    .subtitle {{
      font-size: 1.1rem;
      opacity: 0.9;
      margin-bottom: 30px;
    }}
    .iglesia {{
      font-size: 1.3rem;
      font-weight: bold;
      margin-bottom: 30px;
      color: #ffeb3b;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }}
    .card {{
      background: rgba(255,255,255,0.15);
      border-radius: 16px;
      padding: 25px 15px;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255,255,255,0.2);
      transition: transform 0.3s, box-shadow 0.3s;
    }}
    .card:hover {{
      transform: translateY(-5px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    .card h3 {{
      font-size: 1.4rem;
      margin-bottom: 8px;
      color: #ffeb3b;
    }}
    .card .tema {{
      font-size: 0.95rem;
      margin-bottom: 15px;
      min-height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .btn-jugar {{
      display: inline-block;
      background: #ff9800;
      color: #fff;
      text-decoration: none;
      padding: 12px 30px;
      border-radius: 30px;
      font-weight: bold;
      font-size: 1rem;
      transition: background 0.3s;
    }}
    .btn-jugar:hover {{
      background: #f57c00;
    }}
    .btn-whatsapp {{
      display: inline-block;
      background: #25d366;
      color: #fff;
      text-decoration: none;
      padding: 14px 35px;
      border-radius: 30px;
      font-weight: bold;
      font-size: 1.1rem;
      margin-top: 10px;
      transition: background 0.3s;
    }}
    .btn-whatsapp:hover {{
      background: #128c7e;
    }}
    footer {{
      margin-top: 40px;
      font-size: 0.85rem;
      opacity: 0.7;
    }}
    @media (max-width: 500px) {{
      h1 {{ font-size: 1.6rem; }}
      .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Escuela del Pensamiento</h1>
    <p class="subtitle">Guia {guia_numero} - Iglesia {iglesia}</p>
    <p class="iglesia">Semana de crucigramas educativos</p>
    <div class="grid">
{cards_html}
    </div>
    <a href="https://wa.me/?text=Mira%20los%20crucigramas%20de%20la%20Escuela%20del%20Pensamiento%3A%20https%3A%2F%2Fjosiasevillano-tech.github.io%2FGAC%2F"
       class="btn-whatsapp" target="_blank">Compartir por WhatsApp</a>
    <footer>
      <p>Generado con amor para la Iglesia {iglesia}</p>
    </footer>
  </div>
</body>
</html>"""

    index_path = os.path.join("docs", "index.html")
    with open(index_path, "w", encoding="utf-8") as f2:
        f2.write(html)
    print(f"\n  Generado: {index_path}")


# ============================================================
# PUNTO DE ENTRADA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    guia = load_guia(GUIA_JSON)
    iglesia = guia["iglesia"]
    guia_numero = guia["guia_numero"]

    print("=" * 60)
    print(f"GAC - Guia {guia_numero} - Iglesia {iglesia}")
    print("=" * 60)

    os.makedirs("docs", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    resultados = []
    for i, config in enumerate(guia["crucigramas"], 1):
        resultados.append(generate_and_export(i, config, guia_numero))

    generate_index(guia, resultados)

    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    for i, (ok, config) in enumerate(zip(resultados, guia["crucigramas"]), 1):
        estado = "OK" if ok else "FALLIDO"
        print(f"  Crucigrama {i} ({config['tema']}): {estado}")
    print("\nArchivos generados en la carpeta docs/")
    print("Listo para: git add docs/ && git commit && git push")