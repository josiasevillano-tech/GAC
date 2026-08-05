"""
generar_sitio.py
Genera el sitio completo con acordeones para escalar a 50+ semanas.
"""

import json
import re
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path("docs")
SEMANA_PATTERN = re.compile(r"semana[_\-](\d+)", re.I)

IGLESIA_PRINCIPAL = {
    "nombre": "Iglesia Agua Viva",
    "subtitulo": "Escuela del Pensamiento",
    "logo_src": "assets/logo.png",
}


def leer_json_semana(ruta_carpeta: Path) -> Dict:
    for archivo in ruta_carpeta.glob("*.json"):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            continue
    return {}


def extraer_titulo_html(ruta_html: Path) -> str:
    try:
        with open(ruta_html, "r", encoding="utf-8") as f:
            contenido = f.read(2000)
            match = re.search(r"<title>(.*?)</title>", contenido, re.IGNORECASE)
            if match:
                titulo = match.group(1).strip()
                if titulo and titulo != "Guia de Estudio":
                    return titulo
    except:
        pass
    return ""


def extraer_datos_semana(carpeta: Path) -> Dict:
    datos_json = leer_json_semana(carpeta)
    match = SEMANA_PATTERN.match(carpeta.name)
    numero = int(match.group(1)) if match else 0
    
    titulo = datos_json.get("tema", datos_json.get("title", f"Semana {numero}"))
    resena = datos_json.get("resena", datos_json.get("description", datos_json.get("summary", "")))
    resena_html = resena.replace("\n", "<br>") if resena else "<em>Reseña del tema próximamente...</em>"
    
    crucigramas = sorted(carpeta.glob("crucigrama_*_web.html"))
    
    lista_cruz = []
    for i, cruz in enumerate(crucigramas, 1):
        nombre_titulo = extraer_titulo_html(cruz)
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
    }


def encontrar_semanas() -> List[Dict]:
    if not BASE_DIR.exists():
        print(f"❌ No existe la carpeta '{BASE_DIR}'")
        return []
    
    semanas = []
    for carpeta in sorted(BASE_DIR.iterdir()):
        if carpeta.is_dir() and SEMANA_PATTERN.match(carpeta.name):
            semanas.append(extraer_datos_semana(carpeta))
    
    return sorted(semanas, key=lambda x: x["numero"])


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
        header .logo {
            width: 200px;
            height: auto;
            display: block;
            margin: 0 auto 16px auto;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
        }
        header h1 { color: var(--primario); font-size: 1.9rem; margin-bottom: 6px; }
        header p { color: #718096; font-size: 1.05rem; }
        
        /* === ACORDEÓN === */
        details {
            background: var(--card);
            border-radius: var(--radio);
            margin-bottom: 16px;
            box-shadow: var(--sombra);
            overflow: hidden;
        }
        details[open] { box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
        summary {
            list-style: none;
            cursor: pointer;
            padding: 20px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            transition: background 0.2s;
        }
        summary::-webkit-details-marker { display: none; }
        summary:hover { background: #f7fafc; }
        .summary-left {
            display: flex;
            align-items: center;
            gap: 14px;
            flex: 1;
        }
        .semana-num {
            background: var(--primario);
            color: white;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.95rem;
            flex-shrink: 0;
        }
        .semana-info h3 {
            color: var(--primario);
            font-size: 1.15rem;
            margin-bottom: 2px;
        }
        .semana-info span {
            color: #a0aec0;
            font-size: 0.85rem;
        }
        .flecha {
            color: #a0aec0;
            font-size: 1.2rem;
            transition: transform 0.3s;
        }
        details[open] .flecha { transform: rotate(180deg); }
        
        /* === CONTENIDO DEL ACORDEÓN === */
        .contenido {
            padding: 0 24px 24px;
            border-top: 1px solid var(--borde);
        }
        .resena {
            background: #f7fafc;
            border-left: 4px solid var(--secundario);
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
            font-size: 0.95rem;
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
            font-size: 0.9rem;
        }
        .btn:hover { background: #2b6cb0; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        
        .badge-nueva {
            background: #38a169;
            color: white;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-left: 8px;
        }
        
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
            header .logo { width: 160px; }
            summary { padding: 16px; }
            .contenido { padding: 0 16px 16px; }
            .grid { grid-template-columns: 1fr; }
        }
    </style>
"""


def generar_hub(semanas: List[Dict]) -> str:
    total = len(semanas)
    
    acordeones = []
    for i, sem in enumerate(semanas):
        es_ultima = (i == total - 1)
        abierto = " open" if es_ultima else ""
        badge_nueva = '<span class="badge-nueva">Nueva</span>' if es_ultima else ""
        
        botones = "\n".join([
            f'                <a class="btn" href="{sem["carpeta"]}/{cruz["archivo"]}">{cruz["titulo"]}</a>'
            for cruz in sem["crucigramas"]
        ]) or '                <span style="color:#a0aec0">Sin crucigramas aún</span>'
        
        acordeon = f'''        <details{abierto}>
            <summary>
                <div class="summary-left">
                    <div class="semana-num">{sem["numero"]}</div>
                    <div class="semana-info">
                        <h3>{sem["titulo"]}{badge_nueva}</h3>
                        <span>{len(sem["crucigramas"])} crucigramas</span>
                    </div>
                </div>
                <div class="flecha">▼</div>
            </summary>
            <div class="contenido">
                <div class="resena">
                    {sem["resena_html"]}
                </div>
                <div class="grid">
{botones}
                </div>
            </div>
        </details>'''
        acordeones.append(acordeon)
    
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
            <img class="logo" src="{IGLESIA_PRINCIPAL["logo_src"]}" alt="{IGLESIA_PRINCIPAL["nombre"]}">
            <h1>{IGLESIA_PRINCIPAL["nombre"]}</h1>
            <p>{IGLESIA_PRINCIPAL["subtitulo"]}</p>
        </header>

{chr(10).join(acordeones)}

        <footer>
            {IGLESIA_PRINCIPAL["nombre"]} — Guía de Estudio Interactiva
        </footer>
    </div>
</body>
</html>'''


def generar_pagina_semana(sem: Dict, total_semanas: int) -> str:
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
            <h1>{IGLESIA_PRINCIPAL["nombre"]}</h1>
            <p>{IGLESIA_PRINCIPAL["subtitulo"]} — Semana {sem["numero"]}</p>
        </header>

        <div style="background: var(--card); border-radius: var(--radio); padding: 24px; box-shadow: var(--sombra);">
            <h2 style="color: var(--primario); margin-bottom: 12px;">📝 Reseña del tema</h2>
            <div class="resena">
                {sem["resena_html"]}
            </div>
            
            <h2 style="color: var(--primario); margin: 20px 0 12px;">🎯 Crucigramas</h2>
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


def main():
    print("=" * 55)
    print("   GENERADOR DE SITIO — GUÍA DE ESTUDIO")
    print("=" * 55)
    
    semanas = encontrar_semanas()
    if not semanas:
        print("\n⚠️  No encontré carpetas tipo 'docs/semana-01/'")
        return
    
    print(f"\n📂 Encontradas {len(semanas)} semana(s)")
    for s in semanas:
        print(f"   • Semana {s['numero']}: {s['titulo']} ({len(s['crucigramas'])} crucigramas)")
    
    hub_html = generar_hub(semanas)
    ruta_hub = BASE_DIR / "index.html"
    with open(ruta_hub, "w", encoding="utf-8") as f:
        f.write(hub_html)
    print(f"\n✅ Hub principal generado: {ruta_hub}")
    
    for sem in semanas:
        pagina_html = generar_pagina_semana(sem, len(semanas))
        ruta_pagina = BASE_DIR / sem["carpeta"] / "index.html"
        with open(ruta_pagina, "w", encoding="utf-8") as f:
            f.write(pagina_html)
        print(f"   ✅ {sem['carpeta']}/index.html")
    
    ruta_iglesias = BASE_DIR / "iglesias"
    ruta_iglesias.mkdir(exist_ok=True)
    (ruta_iglesias / ".gitkeep").write_text("")
    
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
    print(f"   git commit -m 'feat: logo mas grande y centrado'")
    print(f"   git push origin guia-ia")


if __name__ == "__main__":
    main()