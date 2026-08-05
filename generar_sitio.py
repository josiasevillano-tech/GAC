"""
generar_sitio.py
Genera el sitio completo:
  - Hub principal (docs/index.html) → para tu iglesia
  - Página de cada semana (docs/semana-XX/index.html) → para usuarios foráneos
  - Solo muestra versiones _web.html (interactivas)
  - Lee el <title> de cada HTML para nombrar los botones
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict


# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────

BASE_DIR = Path("docs")
SEMANA_PATTERN = re.compile(r"semana[_\-](\d+)", re.I)

IGLESIA_PRINCIPAL = {
    "nombre": "Escuela del Pensamiento",
    "subtitulo": "Análisis Estructural del Evangelio de Juan",
    "logo_emoji": "📖",
}


# ─────────────────────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ─────────────────────────────────────────────────────────────

def leer_json_semana(ruta_carpeta: Path) -> Dict:
    """Busca un .json dentro de la carpeta de la semana para extraer tema y reseña."""
    for archivo in ruta_carpeta.glob("*.json"):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            continue
    return {}


def extraer_titulo_html(ruta_html: Path) -> str:
    """Lee el <title> del HTML para usarlo como nombre del botón."""
    try:
        with open(ruta_html, "r", encoding="utf-8") as f:
            contenido = f.read(2000)  # Solo leemos el inicio
            match = re.search(r"<title>(.*?)</title>", contenido, re.IGNORECASE)
            if match:
                titulo = match.group(1).strip()
                # Si el título es muy genérico, lo limpiamos
                if titulo and titulo != "Guia de Estudio":
                    return titulo
    except:
        pass
    return ""


def extraer_datos_semana(carpeta: Path) -> Dict:
    """Extrae título, reseña y lista de crucigramas de una carpeta semana-XX."""
    datos_json = leer_json_semana(carpeta)
    
    match = SEMANA_PATTERN.match(carpeta.name)
    numero = int(match.group(1)) if match else 0
    
    titulo = datos_json.get("tema", datos_json.get("title", f"Semana {numero}"))
    resena = datos_json.get("resena", datos_json.get("description", datos_json.get("summary", "")))
    resena_html = resena.replace("\n", "<br>") if resena else "<em>Reseña del tema próximamente...</em>"
    
    # Solo archivos _web.html (interactivos), ignorar los .html de impresión
    crucigramas = sorted(carpeta.glob("crucigrama_*_web.html"))
    
    lista_cruz = []
    for i, cruz in enumerate(crucigramas, 1):
        # Intentar sacar el nombre del <title> del HTML
        nombre_titulo = extraer_titulo_html(cruz)
        
        # Si no tiene title útil, usar el nombre del archivo limpio
        if not nombre_titulo:
            nombre_titulo = f"Crucigrama {i}"
        
        lista_cruz.append({
            "numero": i,
            "archivo": cruz.name,
            "titulo": nombre_titulo
        })
    
    return {
        "numero": numero,
        "carpeta": carpeta.name,
        "titulo": titulo,
        "resena_html": resena_html,
        "crucigramas": lista_cruz,
        "ruta_relativa": f"{carpeta.name}/index.html"
    }


def encontrar_semanas() -> List[Dict]:
    """Escanea docs/ y devuelve datos de todas las semanas encontradas."""
    if not BASE_DIR.exists():
        print(f"❌ No existe la carpeta '{BASE_DIR}'")
        return []
    
    semanas = []
    for carpeta in sorted(BASE_DIR.iterdir()):
        if carpeta.is_dir() and SEMANA_PATTERN.match(carpeta.name):
            semanas.append(extraer_datos_semana(carpeta))
    
    return sorted(semanas, key=lambda x: x["numero"])


# ─────────────────────────────────────────────────────────────
# PLANTILLAS HTML
# ─────────────────────────────────────────────────────────────

CSS_GLOBAL = """
    <style>
        :root {
            --primario: #2c5282;
            --secundario: #3182ce;
            --fondo: #f5f7fa;
            --card: #ffffff;
            --texto: #2d3748;
            --borde: #e2e8f0;
            --sombra: 0 2px 8px rgba(0,0,0,0.08);
            --radio: 12px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
            background: var(--fondo);
            color: var(--texto);
            padding: 24px 16px;
            min-height: 100vh;
            line-height: 1.6;
        }
        .contenedor { max-width: 800px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 36px; }
        header .emoji { font-size: 3rem; margin-bottom: 8px; display: block; }
        header h1 { color: var(--primario); font-size: 1.9rem; margin-bottom: 6px; }
        header p { color: #718096; font-size: 1.05rem; }
        .semana-card {
            background: var(--card);
            border-radius: var(--radio);
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: var(--sombra);
        }
        .semana-card h2 {
            color: var(--primario);
            font-size: 1.25rem;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--borde);
        }
        .resena {
            background: #f7fafc;
            border-left: 4px solid var(--secundario);
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            font-size: 1rem;
            color: #4a5568;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }
        .btn {
            display: block;
            text-align: center;
            padding: 14px;
            background: var(--secundario);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
            font-size: 0.95rem;
        }
        .btn:hover { background: #2b6cb0; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .btn-outline {
            background: white;
            color: var(--secundario);
            border: 2px solid var(--secundario);
        }
        .btn-outline:hover { background: var(--secundario); color: white; }
        .volver {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 20px;
            color: var(--primario);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
        }
        .volver:hover { text-decoration: underline; }
        .badge {
            display: inline-block;
            background: #c6f6d5;
            color: #22543d;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        footer {
            text-align: center;
            margin-top: 48px;
            padding-top: 24px;
            border-top: 1px solid var(--borde);
            color: #a0aec0;
            font-size: 0.85rem;
        }
        @media (max-width: 480px) {
            header h1 { font-size: 1.5rem; }
            .semana-card { padding: 16px; }
            .grid { grid-template-columns: 1fr; }
        }
    </style>
"""


def generar_hub(semanas: List[Dict]) -> str:
    """Genera el index.html principal (para tu iglesia, acumulativo)."""
    
    secciones = []
    for sem in semanas:
        botones = "\n".join([
            f'                <a class="btn" href="{sem["carpeta"]}/{cruz["archivo"]}">{cruz["titulo"]}</a>'
            for cruz in sem["crucigramas"]
        ]) or '                <span style="color:#a0aec0">Sin crucigramas aún</span>'
        
        seccion = f'''        <div class="semana-card">
            <div class="badge">Semana {sem["numero"]}</div>
            <h2>{sem["titulo"]}</h2>
            <div class="grid">
{botones}
            </div>
        </div>'''
        secciones.append(seccion)
    
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{IGLESIA_PRINCIPAL["nombre"]}</title>
    {CSS_GLOBAL}
</head>
<body>
    <div class="contenedor">
        <header>
            <span class="emoji">{IGLESIA_PRINCIPAL["logo_emoji"]}</span>
            <h1>{IGLESIA_PRINCIPAL["nombre"]}</h1>
            <p>{IGLESIA_PRINCIPAL["subtitulo"]}</p>
        </header>

{chr(10).join(secciones)}

        <footer>
            {IGLESIA_PRINCIPAL["nombre"]} — Guía de Estudio Interactiva
        </footer>
    </div>
</body>
</html>'''


def generar_pagina_semana(sem: Dict, total_semanas: int) -> str:
    """Genera el index.html de una semana individual (para usuarios foráneos)."""
    
    botones = "\n".join([
        f'            <a class="btn" href="{cruz["archivo"]}">{cruz["titulo"]}</a>'
        for cruz in sem["crucigramas"]
    ]) or '            <span style="color:#a0aec0">Crucigramas en preparación...</span>'
    
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{sem["titulo"]} — {IGLESIA_PRINCIPAL["nombre"]}</title>
    {CSS_GLOBAL}
</head>
<body>
    <div class="contenedor">
        <a class="volver" href="../index.html">← Volver al inicio</a>
        
        <header>
            <span class="emoji">📚</span>
            <h1>{sem["titulo"]}</h1>
            <p>Guía de Estudio — Semana {sem["numero"]}</p>
        </header>

        <div class="semana-card">
            <h2>📝 Reseña del tema</h2>
            <div class="resena">
                {sem["resena_html"]}
            </div>
            
            <h2 style="margin-top: 20px; margin-bottom: 12px;">🎯 Crucigramas</h2>
            <div class="grid">
{botones}
            </div>
        </div>

        <footer>
            {IGLESIA_PRINCIPAL["nombre"]} — <a href="../index.html" style="color: var(--secundario);">Ver todas las semanas</a>
        </footer>
    </div>
</body>
</html>'''


# ─────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("   GENERADOR DE SITIO — GUÍA DE ESTUDIO")
    print("=" * 55)
    
    semanas = encontrar_semanas()
    if not semanas:
        print("\n⚠️  No encontré carpetas tipo 'docs/semana-01/'")
        print("   Crea al menos una carpeta con sus crucigramas _web.html")
        return
    
    print(f"\n📂 Encontradas {len(semanas)} semana(s)")
    for s in semanas:
        print(f"   • Semana {s['numero']}: {s['titulo']} ({len(s['crucigramas'])} crucigramas interactivos)")
        for c in s["crucigramas"]:
            print(f"      - {c['titulo']}")
    
    hub_html = generar_hub(semanas)
    ruta_hub = BASE_DIR / "index.html"
    with open(ruta_hub, "w", encoding="utf-8") as f:
        f.write(hub_html)
    print(f"\n✅ Hub principal generado: {ruta_hub}")
    print(f"   🔗 https://TU_USUARIO.github.io/GAC/")
    
    for sem in semanas:
        pagina_html = generar_pagina_semana(sem, len(semanas))
        ruta_pagina = BASE_DIR / sem["carpeta"] / "index.html"
        with open(ruta_pagina, "w", encoding="utf-8") as f:
            f.write(pagina_html)
        print(f"   ✅ {sem['carpeta']}/index.html → Guía individual")
    
    ruta_iglesias = BASE_DIR / "iglesias"
    ruta_iglesias.mkdir(exist_ok=True)
    (ruta_iglesias / ".gitkeep").write_text("")
    print(f"\n🚪 Carpeta 'iglesias/' lista para futuras suscripciones")
    
    print("\n" + "=" * 55)
    print("   RESUMEN DE LINKS")
    print("=" * 55)
    print(f"\n🏠 PARA TU IGLESIA (acumulativo):")
    print(f"   https://TU_USUARIO.github.io/GAC/")
    print(f"\n🌍 PARA USUARIOS FORÁNEOS (guía individual):")
    for sem in semanas:
        print(f"   Semana {sem['numero']}: https://TU_USUARIO.github.io/GAC/{sem['carpeta']}/")
    print(f"\n📋 Próximos pasos:")
    print(f"   git add docs/ generar_sitio.py")
    print(f"   git commit -m 'feat: genera sitio con semana {semanas[-1]['numero']}'")
    print(f"   git push origin guia-ia")


if __name__ == "__main__":
    main()