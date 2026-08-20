"""
boletin_exporter.py
Exportador del bloque "boletin" (actividades de la semana).
No genera crucigrama: es una pagina informativa con tarjetas de actividades.
Usa la misma paleta de colores que el resto del sitio, para verse consistente.
"""

import os


class BoletinExporter:
    """
    Exporta un bloque de tipo 'boletin' a una pagina HTML con tarjetas
    de actividades (titulo, fecha, hora, descripcion, imagen/video opcionales).
    """

    def __init__(self, titulo="Boletin de actividades", introduccion="", actividades=None):
        self.titulo = titulo
        self.introduccion = introduccion or ""
        self.actividades = actividades or []

    def _render_actividad(self, act):
        titulo = act.get("titulo", "Actividad")
        fecha = act.get("fecha", "")
        hora = act.get("hora", "")
        descripcion = act.get("descripcion", "")
        imagen = act.get("imagen")
        video = act.get("video")

        meta_partes = []
        if fecha:
            meta_partes.append(f'<span class="meta-item">📅 {fecha}</span>')
        if hora:
            meta_partes.append(f'<span class="meta-item">🕒 {hora}</span>')
        meta_html = "".join(meta_partes)

        imagen_html = ""
        if imagen:
            imagen_html = f'<img class="actividad-img" src="{imagen}" alt="{titulo}">'

        video_html = ""
        if video:
            video_html = f'''
            <div class="actividad-video">
                <video controls src="{video}"></video>
            </div>
            '''

        return f"""
        <div class="actividad-card">
            {imagen_html}
            <div class="actividad-contenido">
                <h3>{titulo}</h3>
                {f'<div class="actividad-meta">{meta_html}</div>' if meta_html else ''}
                {f'<p class="actividad-desc">{descripcion}</p>' if descripcion else ''}
                {video_html}
            </div>
        </div>
        """

    def to_html(self):
        css = """
        <style>
            :root {
                --color-fondo: #f5f7fa;
                --color-primario: #2c5282;
                --color-secundario: #3182ce;
                --color-texto: #2d3748;
                --color-borde: #cbd5e0;
                --sombra: 0 2px 8px rgba(0,0,0,0.08);
                --radio: 8px;
            }
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
                background: var(--color-fondo);
                color: var(--color-texto);
                line-height: 1.5;
                padding: 16px;
                min-height: 100vh;
            }
            .contenedor { max-width: 800px; margin: 0 auto; }
            header { text-align: center; margin-bottom: 24px; }
            header h1 { font-size: 1.6rem; color: var(--color-primario); margin-bottom: 8px; }
            .introduccion {
                background: white; padding: 18px 20px; border-radius: var(--radio);
                box-shadow: var(--sombra); margin-bottom: 24px;
                font-size: 1.05rem; line-height: 1.7;
                border-left: 4px solid var(--color-secundario);
            }
            .actividades { display: flex; flex-direction: column; gap: 16px; }
            .actividad-card {
                background: white; border-radius: var(--radio);
                box-shadow: var(--sombra); overflow: hidden;
            }
            .actividad-img { width: 100%; max-height: 280px; object-fit: cover; display: block; }
            .actividad-contenido { padding: 18px 20px; }
            .actividad-contenido h3 { font-size: 1.2rem; color: var(--color-primario); margin-bottom: 8px; }
            .actividad-meta { margin-bottom: 10px; }
            .meta-item {
                display: inline-block; font-size: 0.85rem; color: #718096;
                background: #edf2f7; padding: 4px 10px; border-radius: 20px;
                margin-right: 6px; font-weight: 600;
            }
            .actividad-desc { font-size: 0.98rem; line-height: 1.6; color: var(--color-texto); }
            .actividad-video { margin-top: 12px; }
            .actividad-video video { width: 100%; border-radius: 6px; }
            footer {
                text-align: center; margin-top: 24px; padding-top: 16px;
                border-top: 1px solid var(--color-borde); font-size: 0.8rem; color: #a0aec0;
            }
        </style>
        """

        introduccion_html = ""
        if self.introduccion:
            introduccion_html = f'<div class="introduccion"><p>{self.introduccion}</p></div>'

        actividades_html = "".join(self._render_actividad(a) for a in self.actividades)

        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.titulo}</title>
    {css}
</head>
<body>
    <div class="contenedor">
        <header>
            <h1>{self.titulo}</h1>
        </header>
        {introduccion_html}
        <div class="actividades">
            {actividades_html}
        </div>
        <footer>
            Escuela del Pensamiento - Boletin de actividades
        </footer>
    </div>
</body>
</html>"""

    def save(self, filename="boletin_web.html"):
        """Guarda el HTML en un archivo con ruta absoluta."""
        html = self.to_html()
        filepath = os.path.abspath(filename)
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print("Boletin guardado en: " + filepath)
        return filepath
