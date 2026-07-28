import os


class Exporter:
    """
    Exporta un crucigrama a HTML profesional listo para imprimir en A4.
    Página 1: miniatura resuelta + intro
    Página 2: tablero + pistas (todo contenido)
    """

    def __init__(self, data, title="Guía de Estudio", subtitle="Crucigrama"):
        self.data = data
        self.title = title
        self.subtitle = subtitle

    def _render_grid(self, grid, cell_size, number_size, show_letters=False):
        """Renderiza una cuadrícula como HTML."""
        html = f'<table class="crossword" style="font-family: Arial, sans-serif;">'
        for row in grid:
            html += "<tr>"
            for cell in row:
                if cell["is_empty"]:
                    html += '<td class="empty"></td>'
                else:
                    number_span = ""
                    if cell.get("number"):
                        number_span = f'<span class="number" style="font-size:{number_size}px;font-family:Arial,sans-serif;">{cell["number"]}</span>'
                    content = cell["letter"] if show_letters and cell["letter"] else ""
                    html += f'<td style="width:{cell_size}px;height:{cell_size}px;">{number_span}{content}</td>'
            html += "</tr>"
        html += "</table>"
        return html

    def _line_for_word(self, word):
        """Genera una línea de subrayado proporcional al tamaño de la palabra."""
        length = len(word)
        # Cada letra ≈ 12px de ancho en Arial 11
        width = max(60, length * 12 + 20)
        return f'<span class="answer-line" style="width:{width}px;"></span>'

    def to_html(self):
        """Genera el HTML completo de la guía de estudio (2 páginas A4)."""
        grid = self.data["grid"]
        solved = self.data.get("solved_grid", grid)
        horizontal = self.data["horizontal"]
        vertical = self.data["vertical"]

        css = """
        <style>
            @page { size: A4 portrait; margin: 15mm 18mm; }

            * { box-sizing: border-box; }

            body {
                font-family: Arial, "Segoe UI", sans-serif;
                margin: 0;
                padding: 0;
                color: #000;
                background: #fff;
                font-size: 11pt;
            }

            .page {
                width: 100%;
                min-height: 257mm;
                padding: 0;
                position: relative;
            }

            .page-break {
                page-break-after: always;
                break-after: page;
            }

            /* ===== PÁGINA 1 ===== */
            .page1-header {
                text-align: center;
                margin-bottom: 20px;
                border-bottom: 2px solid #000;
                padding-bottom: 12px;
            }
            .page1-header h1 {
                font-family: Arial, sans-serif;
                font-size: 20pt;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin: 0 0 6px 0;
                font-weight: bold;
            }
            .page1-header h2 {
                font-family: Arial, sans-serif;
                font-size: 12pt;
                font-weight: normal;
                color: #333;
                margin: 0;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .intro-section {
                margin-bottom: 25px;
            }
            .intro-section h3 {
                font-family: Arial, sans-serif;
                font-size: 12pt;
                text-transform: uppercase;
                border-bottom: 1px solid #000;
                padding-bottom: 4px;
                margin: 0 0 10px 0;
            }
            .intro-text {
                font-family: Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                text-align: justify;
            }
            .intro-text p {
                margin: 0 0 8px 0;
            }

            .miniature-section {
                text-align: center;
                margin-top: 30px;
            }
            .miniature-section h3 {
                font-family: Arial, sans-serif;
                font-size: 11pt;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin: 0 0 12px 0;
                color: #333;
            }

            /* ===== PÁGINA 2 ===== */
            .page2-header {
                text-align: center;
                margin-bottom: 15px;
                border-bottom: 2px solid #000;
                padding-bottom: 10px;
            }
            .page2-header h1 {
                font-family: Arial, sans-serif;
                font-size: 18pt;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin: 0;
                font-weight: bold;
            }

            .board-section {
                text-align: center;
                margin-bottom: 18px;
            }

            /* Tablero principal */
            table.crossword {
                border-collapse: collapse;
                margin: 0 auto;
                border: 2px solid #000;
            }
            table.crossword td {
                border: 1px solid #000;
                text-align: center;
                vertical-align: middle;
                position: relative;
                font-family: Arial, sans-serif;
                font-weight: bold;
                background: #fff;
                padding: 0;
                font-size: 14px;
            }
            table.crossword td.empty {
                background: transparent;
                border: none;
            }
            table.crossword td .number {
                position: absolute;
                top: 1px;
                left: 2px;
                font-family: Arial, sans-serif;
                line-height: 1;
                color: #000;
            }

            /* Miniatura */
            table.miniature {
                border-collapse: collapse;
                margin: 0 auto;
                border: 1.5px solid #000;
            }
            table.miniature td {
                border: 0.5px solid #000;
                text-align: center;
                vertical-align: middle;
                position: relative;
                font-family: Arial, sans-serif;
                font-size: 6px;
                font-weight: bold;
                background: #fff;
                padding: 0;
            }
            table.miniature td.empty {
                background: transparent;
                border: none;
            }
            table.miniature td .number {
                position: absolute;
                top: 0;
                left: 1px;
                font-family: Arial, sans-serif;
                font-size: 5px;
                line-height: 1;
                color: #000;
            }

            /* Pistas */
            .clues-section {
                width: 100%;
            }
            .clues-section h3 {
                font-family: Arial, sans-serif;
                font-size: 12pt;
                text-transform: uppercase;
                letter-spacing: 1px;
                border-bottom: 2px solid #000;
                padding-bottom: 5px;
                margin: 0 0 10px 0;
            }
            .clues-row {
                display: flex;
                gap: 25px;
            }
            .clues-column {
                flex: 1;
                width: 50%;
            }
            .clues-column h4 {
                font-family: Arial, sans-serif;
                font-size: 11pt;
                text-transform: uppercase;
                margin: 0 0 8px 0;
                color: #000;
                border-bottom: 1px solid #999;
                padding-bottom: 3px;
            }
            .clues-column ol {
                padding-left: 22px;
                margin: 0;
            }
            .clues-column li {
                margin-bottom: 6px;
                font-family: Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.35;
                color: #000;
            }
            .clues-column li .clue-text {
                display: inline;
            }
            .answer-line {
                display: inline-block;
                border-bottom: 1px solid #000;
                height: 14px;
                vertical-align: bottom;
                margin-right: 4px;
            }

            .footer {
                text-align: center;
                margin-top: 15px;
                padding-top: 6px;
                border-top: 1px solid #ccc;
                font-family: Arial, sans-serif;
                font-size: 8pt;
                color: #555;
            }
        </style>
        """

        # ========== PÁGINA 1 ==========
        solved_html = self._render_grid(solved, cell_size=14, number_size=5, show_letters=True)

        page1 = f"""
        <div class="page">
            <div class="page1-header">
                <h1>{self.title}</h1>
                <h2>{self.subtitle}</h2>
            </div>

            <div class="intro-section">
                <h3>Instrucciones</h3>
                <div class="intro-text">
                    <p>Lee atentamente las pistas de cada dirección y completa el crucigrama 
                    con los personajes bíblicos correspondientes. Este ejercicio te ayudará 
                    a reforzar tu conocimiento sobre las figuras fundamentales de la historia 
                    de la salvación.</p>
                    <p><em>(Reemplaza este texto por tu contenido didáctico específico del tema.)</em></p>
                </div>
            </div>

            <div class="miniature-section">
                <h3>Hoja de Respuestas (Vista en Miniatura)</h3>
                {solved_html}
            </div>
        </div>
        """

        # ========== PÁGINA 2 ==========
        # Tablero principal con números (más grande)
        student_html = self._render_grid(grid, cell_size=22, number_size=7, show_letters=False)

        def format_clues(clues, direction_name):
            items = ""
            for clue in clues:
                line = self._line_for_word(clue["word"])
                items += (
                    f'<li value="{clue["number"]}">'
                    f'{line} '
                    f'<span class="clue-text">______________________________________________</span>'
                    f'</li>'
                )
            return f"""
            <div class="clues-column">
                <h4>{direction_name}</h4>
                <ol>{items}</ol>
            </div>
            """

        page2 = f"""
        <div class="page">
            <div class="page2-header">
                <h1>{self.title}</h1>
            </div>

            <div class="board-section">
                {student_html}
            </div>

            <div class="clues-section">
                <h3>Pistas</h3>
                <div class="clues-row">
                    {format_clues(horizontal, "Horizontales")}
                    {format_clues(vertical, "Verticales")}
                </div>
            </div>

            <div class="footer">
                Guía de estudio generada automáticamente — Escuela del Pensamiento
            </div>
        </div>
        """

        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    {css}
</head>
<body>
    {page1}
    <div class="page-break"></div>
    {page2}
</body>
</html>"""

    def save(self, filename="crucigrama.html"):
        """Guarda el HTML en un archivo con ruta absoluta."""
        html = self.to_html()
        filepath = os.path.abspath(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Archivo guardado en: {filepath}")
        return filepath