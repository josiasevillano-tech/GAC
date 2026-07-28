import os


class Exporter:
    """
    Exporta un crucigrama a HTML profesional.
    El archivo resultante se abre perfectamente en Word o navegador.
    """

    def __init__(self, data, title="Crucigrama"):
        self.data = data
        self.title = title

    def to_html(self):
        """Genera el HTML completo del crucigrama."""
        grid = self.data["grid"]
        horizontal = self.data["horizontal"]
        vertical = self.data["vertical"]
        cell_size = 35

        css = f"""
        <style>
            body {{
                font-family: "Segoe UI", Arial, sans-serif;
                margin: 40px;
                color: #222;
            }}
            h1 {{
                text-align: center;
                font-size: 24px;
                margin-bottom: 30px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .crossword-container {{
                text-align: center;
                margin: 30px 0;
            }}
            table.crossword {{
                border-collapse: collapse;
                margin: 0 auto;
                border: 3px solid #000;
            }}
            table.crossword td {{
                width: {cell_size}px;
                height: {cell_size}px;
                border: 1px solid #000;
                text-align: center;
                vertical-align: middle;
                position: relative;
                font-size: 18px;
                font-weight: bold;
                background: #fff;
            }}
            table.crossword td.empty {{
                background-color: #222;
                border: 1px solid #222;
            }}
            table.crossword td .number {{
                position: absolute;
                top: 1px;
                left: 3px;
                font-size: 9px;
                font-weight: normal;
                color: #000;
                line-height: 1;
            }}
            .clues-container {{
                display: flex;
                justify-content: center;
                margin-top: 40px;
                gap: 60px;
            }}
            .clues-column {{
                flex: 1;
                max-width: 45%;
            }}
            .clues-column h2 {{
                border-bottom: 2px solid #000;
                padding-bottom: 8px;
                font-size: 16px;
                text-transform: uppercase;
                margin-bottom: 15px;
            }}
            .clues-column ol {{
                padding-left: 25px;
                margin: 0;
            }}
            .clues-column li {{
                margin-bottom: 10px;
                font-size: 13px;
                line-height: 1.4;
            }}
            .footer {{
                text-align: center;
                margin-top: 50px;
                font-size: 11px;
                color: #666;
            }}
        </style>
        """

        # Tablero (versión vacía para el estudiante)
        board_html = '<div class="crossword-container"><table class="crossword">'
        for row in grid:
            board_html += "<tr>"
            for cell in row:
                if cell["is_empty"]:
                    board_html += '<td class="empty"></td>'
                else:
                    number_span = ""
                    if cell["number"]:
                        number_span = f'<span class="number">{cell["number"]}</span>'
                    board_html += f'<td>{number_span}</td>'
            board_html += "</tr>"
        board_html += "</table></div>"

        def format_clues(clues, direction_name):
            html = f'<div class="clues-column"><h2>Pistas {direction_name}</h2><ol>'
            for clue in clues:
                html += (
                    f'<li value="{clue["number"]}">'
                    f'<strong>{clue["word"]}</strong> '
                    f'({clue["length"]} letras)'
                    f'</li>'
                )
            html += "</ol></div>"
            return html

        clues_html = '<div class="clues-container">'
        clues_html += format_clues(horizontal, "Horizontales")
        clues_html += format_clues(vertical, "Verticales")
        clues_html += "</div>"

        footer = (
            '<div class="footer">'
            'Guía de estudio generada automáticamente — Escuela del Pensamiento'
            '</div>'
        )

        return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    {css}
</head>
<body>
    <h1>{self.title}</h1>
    {board_html}
    {clues_html}
    {footer}
</body>
</html>"""

    def save(self, filename="crucigrama.html"):
        """
        Guarda el HTML en un archivo.
        Usa ruta absoluta para evitar confusiones de carpeta.
        """
        html = self.to_html()
        filepath = os.path.abspath(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Archivo guardado en: {filepath}")
        return filepath