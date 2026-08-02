import os


class Exporter:
    """
    Exporta un crucigrama a HTML profesional listo para imprimir en A4.
    """

    def __init__(self, data, title="Guia de Estudio", subtitle="Crucigrama", clues=None, resena=""):
        self.data = data
        self.title = title
        self.subtitle = subtitle
        self.clues = clues or {}
        self.resena = resena

    def _render_grid(self, grid, cell_size, show_letters=False, css_class="crossword"):
        """Renderiza una cuadricula como HTML."""
        html = f'<table class="{css_class}">'
        for row in grid:
            html += "<tr>"
            for cell in row:
                if cell["is_empty"]:
                    html += '<td class="empty"></td>'
                else:
                    number_span = ""
                    if cell.get("number"):
                        number_span = f'<span class="number">{cell["number"]}</span>'
                    content = cell["letter"] if show_letters and cell["letter"] else ""
                    html += f'<td style="width:{cell_size}px;height:{cell_size}px;">{number_span}{content}</td>'
            html += "</tr>"
        html += "</table>"
        return html

    def _line_for_word(self, word):
        """Genera una raya proporcional al tamano de la palabra usando subrayado."""
        length = len(word)
        num_spaces = max(12, length * 3 + 6)
        spaces = "&nbsp;" * num_spaces
        return f'<span class="answer-line">{spaces}</span>'

    def to_html(self):
        """Genera el HTML completo de la guia de estudio (2 paginas A4)."""
        grid = self.data["grid"]
        solved = self.data.get("solved_grid", grid)
        horizontal = self.data["horizontal"]
        vertical = self.data["vertical"]

        css = """
        <style>
            @page { size: A4 portrait; margin: 10mm; }
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: Arial, sans-serif; color: #000; background: #fff; font-size: 11pt; word-wrap: break-word; }
            .page { width: 100%; min-height: 284mm; position: relative; }
            .page-break { page-break-after: always; break-after: page; }
            .page1-header { text-align: center; margin-bottom: 10px; border-bottom: 2px solid #000; padding-bottom: 6px; }
            .page1-header h1 { font-size: 20pt; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 3px 0; font-weight: bold; }
            .page1-header h2 { font-size: 11pt; font-weight: normal; color: #333; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
            .intro-section { margin-bottom: 16px; }
            .intro-section h3 { font-size: 11pt; text-transform: uppercase; border-bottom: 1px solid #000; padding-bottom: 2px; margin: 0 0 6px 0; }
            .intro-text { font-size: 11pt; line-height: 1.5; text-align: justify; word-wrap: break-word; overflow-wrap: break-word; }
            .intro-text p { margin: 0 0 5px 0; }
            .miniature-section { text-align: center; margin-top: 14px; }
            .miniature-section h3 { font-size: 10pt; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 8px 0; color: #333; }
            .page2-header { text-align: center; margin-bottom: 8px; border-bottom: 2px solid #000; padding-bottom: 6px; }
            .page2-header h1 { font-size: 18pt; text-transform: uppercase; letter-spacing: 2px; margin: 0; font-weight: bold; }
            .board-section { text-align: center; margin-bottom: 10px; }
            table.crossword { border-collapse: collapse; margin: 0 auto; border: 2px solid #000; }
            table.crossword td { border: 1px solid #000; text-align: center; vertical-align: middle; position: relative; background: #fff; padding: 0; font-size: 15px; }
            table.crossword td.empty { background: transparent; border: none; }
            table.crossword td .number { position: absolute; top: 1px; left: 2px; font-size: 7pt; line-height: 1; color: #000; }
            table.miniature { border-collapse: collapse; margin: 0 auto; border: 1.5px solid #000; }
            table.miniature td { border: 0.5px solid #000; text-align: center; vertical-align: middle; position: relative; font-size: 8px; background: #fff; padding: 0; }
            table.miniature td.empty { background: transparent; border: none; }
            table.miniature td .number { position: absolute; top: 0; left: 1px; font-size: 5pt; line-height: 1; color: #000; }
            .clues-section { width: 100%; }
            .clues-section h3 { font-size: 11pt; text-transform: uppercase; letter-spacing: 1px; border-bottom: 2px solid #000; padding-bottom: 3px; margin: 0 0 6px 0; }
            .clues-row { display: flex; gap: 14px; }
            .clues-column { flex: 1; width: 50%; }
            .clues-column h4 { font-size: 10pt; text-transform: uppercase; margin: 0 0 5px 0; color: #000; border-bottom: 1px solid #999; padding-bottom: 2px; }
            .clues-column ol { padding-left: 16px; margin: 0; }
            .clues-column li { margin-top: 0; margin-bottom: 1px; padding-top: 0; padding-bottom: 0; font-size: 11pt; line-height: 1.15; color: #000; list-style-position: outside; }
            .answer-line { text-decoration: underline; text-decoration-thickness: 1.5px; text-underline-offset: 2px; white-space: pre; }
            .footer { text-align: center; margin-top: 8px; padding-top: 3px; border-top: 1px solid #ccc; font-size: 8pt; color: #555; }
        </style>
        """

        solved_html = self._render_grid(solved, cell_size=16, show_letters=True, css_class="miniature")

        # Usar la resena si existe, sino instrucciones genericas
        if self.resena:
            intro_text = self.resena.replace("\n", "<br>")
        else:
            intro_text = "Lee atentamente las pistas de cada direccion y completa el crucigrama con las palabras correspondientes. Este ejercicio te ayudara a reforzar tu conocimiento sobre el tema."

        page1 = f"""
        <div class="page">
            <div class="page1-header">
                <h1>{self.title}</h1>
                <h2>{self.subtitle}</h2>
            </div>
            <div class="intro-section">
                <h3>Resena del tema</h3>
                <div class="intro-text">
                    <p>{intro_text}</p>
                </div>
            </div>
            <div class="miniature-section">
                <h3>Hoja de Respuestas</h3>
                {solved_html}
            </div>
        </div>
        """

        student_html = self._render_grid(grid, cell_size=24, show_letters=False, css_class="crossword")

        def format_clues(clues_list, direction_name):
            items = ""
            for clue in clues_list:
                word = clue["word"]
                line = self._line_for_word(word)
                definition = self.clues.get(word, "")
                if definition:
                    clue_text = f'<span class="clue-text">{definition}</span>'
                else:
                    clue_text = '<span class="clue-text">______________________________________________</span>'
                items += (
                    f'<li value="{clue["number"]}">'
                    f'{line} {clue_text}'
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
                Guia de estudio generada automaticamente
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
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print("Archivo guardado en: " + filepath)
        return filepath