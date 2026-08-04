"""
web_exporter.py
Exportador web interactivo para el GAC.
Recibe los mismos datos que Exporter (data, title, clues) y genera HTML jugable.
Compatible con GitHub Pages.
"""

import json
import os
from typing import List, Dict, Any


class WebExporter:
    """
    Exporta crucigramas a HTML interactivo con JavaScript puro.
    Recibe exactamente los mismos parametros que tu Exporter actual.
    """

    def __init__(self, data, title="Guia de Estudio", clues=None, resena="", tema=""):
        self.data = data
        self.title = title
        self.clues = clues or {}
        self.resena = resena
        self.tema = tema

    def save(self, filename="crucigrama_web.html") -> str:
        """Genera y guarda el HTML jugable."""
        matriz = self._extraer_matriz()
        palabras = self._extraer_palabras(matriz)
        filas = len(matriz)
        columnas = len(matriz[0]) if matriz else 0

        print(f"[DEBUG] Filas: {filas}, Columnas: {columnas}, Palabras: {len(palabras)}")
        for p in palabras[:3]:
            print(f"  - {p['palabra']} ({p['direccion']}) en [{p['fila_inicio']},{p['columna_inicio']}]")

        html = self._generar_html(matriz, palabras, filas, columnas)
        filepath = os.path.abspath(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print("Web interactiva guardada en: " + filepath)
        return filepath

    def _extraer_matriz(self) -> List[List[str]]:
        """Convierte la cuadricula del generador a matriz de letras/#."""
        grid = self.data.get("solved_grid") or self.data.get("grid", [])
        if not grid:
            return []
        matriz = []
        for row in grid:
            fila = []
            for cell in row:
                if isinstance(cell, dict):
                    if cell.get("is_empty"):
                        fila.append("#")
                    else:
                        letra = cell.get("letter", "")
                        fila.append(letra.upper() if letra else " ")
                else:
                    # Si cell es un string directo
                    fila.append(str(cell).upper() if str(cell).strip() else "#")
            matriz.append(fila)
        return matriz

    def _get_clue_lists(self):
        """Obtiene las listas de pistas probando varias claves posibles."""
        # Probar varias combinaciones de claves
        h_keys = ["horizontal", "across", "h", "horizontales"]
        v_keys = ["vertical", "down", "v", "verticales"]

        h_list = []
        v_list = []

        for k in h_keys:
            if k in self.data:
                h_list = self.data[k]
                break
        for k in v_keys:
            if k in self.data:
                v_list = self.data[k]
                break

        return h_list, v_list

    def _get_word_from_item(self, item):
        """Extrae la palabra de un item de pista probando varias claves."""
        for key in ["word", "text", "answer", "palabra", "w"]:
            if key in item:
                return item[key]
        return ""

    def _get_number_from_item(self, item):
        """Extrae el numero de un item de pista probando varias claves."""
        for key in ["number", "num", "id", "n", "numero"]:
            if key in item:
                return item[key]
        return None

    def _buscar_posicion(self, grid, numero) -> tuple:
        """Busca en la cuadricula la celda que tiene este numero."""
        if numero is None:
            return None, None
        num_str = str(numero)
        for f, row in enumerate(grid):
            for c, cell in enumerate(row):
                if isinstance(cell, dict):
                    cell_num = cell.get("number") or cell.get("num") or cell.get("id") or cell.get("n")
                    if cell_num is not None and str(cell_num) == num_str:
                        return f, c
        return None, None

    def _buscar_palabra_en_matriz(self, matriz, palabra, direccion) -> tuple:
        """Busca una palabra en la matriz letra por letra."""
        if not palabra or not matriz:
            return None, None
        palabra = palabra.upper()
        filas = len(matriz)
        columnas = len(matriz[0]) if filas > 0 else 0

        for f in range(filas):
            for c in range(columnas):
                if matriz[f][c] == palabra[0] or matriz[f][c] == " ":
                    if direccion == "horizontal":
                        if c + len(palabra) <= columnas:
                            match = True
                            for i in range(len(palabra)):
                                if matriz[f][c + i] not in (palabra[i], " "):
                                    match = False
                                    break
                            if match:
                                return f, c
                    else:  # vertical
                        if f + len(palabra) <= filas:
                            match = True
                            for i in range(len(palabra)):
                                if matriz[f + i][c] not in (palabra[i], " "):
                                    match = False
                                    break
                            if match:
                                return f, c
        return None, None

    def _extraer_palabras(self, matriz) -> List[Dict[str, Any]]:
        """Extrae todas las palabras con sus posiciones."""
        h_list, v_list = self._get_clue_lists()
        palabras = []

        # Procesar horizontales
        for item in h_list:
            word = self._get_word_from_item(item)
            num = self._get_number_from_item(item)
            pista = self.clues.get(word, "")

            fila, col = self._buscar_posicion(self.data.get("solved_grid") or self.data.get("grid", []), num)

            # Fallback: buscar en la matriz directamente
            if fila is None and matriz:
                fila, col = self._buscar_palabra_en_matriz(matriz, word, "horizontal")

            if fila is not None:
                palabras.append({
                    "palabra": word,
                    "pista": pista,
                    "direccion": "horizontal",
                    "fila_inicio": fila,
                    "columna_inicio": col,
                    "numero": num if num is not None else len(palabras) + 1
                })

        # Procesar verticales
        for item in v_list:
            word = self._get_word_from_item(item)
            num = self._get_number_from_item(item)
            pista = self.clues.get(word, "")

            fila, col = self._buscar_posicion(self.data.get("solved_grid") or self.data.get("grid", []), num)

            # Fallback: buscar en la matriz directamente
            if fila is None and matriz:
                fila, col = self._buscar_palabra_en_matriz(matriz, word, "vertical")

            if fila is not None:
                palabras.append({
                    "palabra": word,
                    "pista": pista,
                    "direccion": "vertical",
                    "fila_inicio": fila,
                    "columna_inicio": col,
                    "numero": num if num is not None else len(palabras) + 1
                })

        return palabras

    def _generar_html(self, matriz, palabras, filas, columnas) -> str:
        """Genera el HTML completo con CSS y JavaScript embebidos."""
        palabras_js = json.dumps(palabras, ensure_ascii=False)
        total_palabras = len(palabras)
        resena_html = self.resena.replace("\n", "<br>")

        css = """
        :root {
            --color-fondo: #f5f7fa;
            --color-primario: #2c5282;
            --color-secundario: #3182ce;
            --color-acierto: #38a169;
            --color-error: #e53e3e;
            --color-negra: #1a202c;
            --color-texto: #2d3748;
            --color-borde: #cbd5e0;
            --color-celda-activa: #bee3f8;
            --color-celda-seleccionada: #90cdf4;
            --sombra: 0 2px 8px rgba(0,0,0,0.08);
            --radio: 8px;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--color-fondo);
            color: var(--color-texto);
            line-height: 1.5;
            padding: 16px;
            min-height: 100vh;
        }
        .contenedor { max-width: 800px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 20px; }
        header h1 { font-size: 1.5rem; color: var(--color-primario); margin-bottom: 4px; }
        header .tema { font-size: 0.9rem; color: #718096; font-weight: 500; }
        .resena {
            background: white; padding: 16px; border-radius: var(--radio);
            box-shadow: var(--sombra); margin-bottom: 20px;
            font-size: 1.25rem; line-height: 1.75;
            border-left: 4px solid var(--color-secundario);
        }
        .resena h3 { font-size: 1.35rem; color: var(--color-primario); margin-bottom: 12px; }
        .barra-progreso {
            background: white; padding: 12px 16px; border-radius: var(--radio);
            box-shadow: var(--sombra); margin-bottom: 16px;
            display: flex; justify-content: space-between; align-items: center;
            flex-wrap: wrap; gap: 8px;
        }
        .barra-progreso .info { font-size: 0.9rem; font-weight: 500; }
        .barra-progreso .progreso-visual {
            flex: 1; min-width: 120px; height: 10px;
            background: #e2e8f0; border-radius: 5px; overflow: hidden;
        }
        .barra-progreso .progreso-visual .relleno {
            height: 100%; width: 0%; background: var(--color-acierto);
            border-radius: 5px; transition: width 0.4s ease;
        }
        .botones {
            display: flex; gap: 10px; flex-wrap: wrap;
            justify-content: center; margin-bottom: 16px;
        }
        .btn {
            padding: 10px 20px; border: none; border-radius: var(--radio);
            font-size: 0.9rem; font-weight: 600; cursor: pointer;
            transition: all 0.2s; touch-action: manipulation;
        }
        .btn-primario { background: var(--color-primario); color: white; }
        .btn-primario:hover { background: var(--color-secundario); }
        .btn-secundario { background: #edf2f7; color: var(--color-texto); }
        .btn-secundario:hover { background: #e2e8f0; }
        .btn-pista { background: #faf089; color: #744210; }
        .btn-pista:hover { background: #f6e05e; }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .layout { display: flex; flex-direction: column; gap: 20px; }
        @media (min-width: 768px) { .layout { flex-direction: row; align-items: flex-start; } }
        .tablero-wrapper { flex: 1; min-width: 0; display: flex; justify-content: center; }
        .tablero {
            display: grid; gap: 1px; background: var(--color-borde);
            border: 2px solid var(--color-borde); border-radius: var(--radio);
            overflow: hidden; box-shadow: var(--sombra);
            width: 100%; max-width: 500px;
        }
        .celda {
            position: relative; background: white;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: clamp(10px, 4vw, 18px);
            color: var(--color-texto); cursor: pointer;
            user-select: none; transition: background 0.15s;
            aspect-ratio: 1;
        }
        .celda.negra { background: var(--color-negra); cursor: default; }
        .celda.activa { background: var(--color-celda-activa); }
        .celda.seleccionada { background: var(--color-celda-seleccionada); }
        .celda.correcta { background: #c6f6d5; color: #22543d; }
        .celda.incorrecta { background: #fed7d7; color: #742a2a; }
        .celda .numero {
            position: absolute; top: 1px; left: 2px;
            font-size: clamp(6px, 2vw, 10px); font-weight: 600;
            color: #4a5568; line-height: 1;
        }
        .celda input {
            width: 100%; height: 100%; border: none; background: transparent;
            text-align: center; font-weight: 700; font-size: inherit;
            color: inherit; text-transform: uppercase; outline: none; padding: 0;
            caret-color: var(--color-primario);
        }
        .pistas { flex: 1; min-width: 280px; }
        .pistas h3 {
            font-size: 1rem; color: var(--color-primario); margin-bottom: 10px;
            padding-bottom: 6px; border-bottom: 2px solid var(--color-borde);
        }
        .pista-item {
            background: white; padding: 10px 12px; margin-bottom: 8px;
            border-radius: 6px; box-shadow: var(--sombra); font-size: 0.9rem;
            cursor: pointer; transition: all 0.2s; border-left: 3px solid transparent;
        }
        .pista-item:hover { background: #f7fafc; }
        .pista-item.activa { border-left-color: var(--color-secundario); background: #ebf8ff; }
        .pista-item.completada {
            opacity: 0.6; text-decoration: line-through;
            background: #f0fff4; border-left-color: var(--color-acierto);
        }
        .pista-item .num { font-weight: 700; color: var(--color-primario); margin-right: 6px; }
        .mensaje {
            position: fixed; top: 16px; left: 50%;
            transform: translateX(-50%) translateY(-100px);
            background: var(--color-primario); color: white;
            padding: 12px 24px; border-radius: var(--radio); font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000;
            transition: transform 0.3s ease; text-align: center; max-width: 90vw;
        }
        .mensaje.visible { transform: translateX(-50%) translateY(0); }
        .mensaje.exito { background: var(--color-acierto); }
        .mensaje.error { background: var(--color-error); }
        .mensaje.pista-msg { background: #d69e2e; }
        footer {
            text-align: center; margin-top: 24px; padding-top: 16px;
            border-top: 1px solid var(--color-borde); font-size: 0.8rem; color: #a0aec0;
        }
        .teclado {
            display: none; position: fixed; bottom: 0; left: 0; right: 0;
            background: #edf2f7; padding: 8px; gap: 4px;
            justify-content: center; flex-wrap: wrap; z-index: 500;
            box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
        }
        @media (max-width: 767px) {
            .teclado { display: flex; }
            body { padding-bottom: 80px; }
        }
        .tecla {
            min-width: 32px; height: 42px; background: white;
            border: 1px solid var(--color-borde); border-radius: 5px;
            font-weight: 700; font-size: 1rem; color: var(--color-texto);
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            flex: 1; max-width: 40px;
        }
        .tecla:active { background: var(--color-celda-seleccionada); }
        .tecla-borrar { background: #fed7d7; color: #742a2a; }
        """

        js = f"""
        const PALABRAS = {palabras_js};
        const FILAS = {filas};
        const COLUMNAS = {columnas};
        const TOTAL_PALABRAS = {total_palabras};

        let celdaActiva = null;
        let direccionActiva = 'horizontal';
        let palabrasCompletadas = new Set();

        function init() {{
            renderTablero();
            renderPistas();
            document.addEventListener('keydown', manejarTecla);
        }}

        function renderTablero() {{
            const tablero = document.getElementById('tablero');
            tablero.innerHTML = '';
            tablero.style.gridTemplateColumns = 'repeat(' + COLUMNAS + ', 1fr)';
            tablero.style.aspectRatio = COLUMNAS + ' / ' + FILAS;

            for (let f = 0; f < FILAS; f++) {{
                for (let c = 0; c < COLUMNAS; c++) {{
                    const celda = document.createElement('div');
                    celda.className = 'celda';
                    celda.dataset.fila = f;
                    celda.dataset.columna = c;

                    const esNegra = !PALABRAS.some(p => {{
                        const df = p.direccion === 'horizontal' ? 0 : 1;
                        const dc = p.direccion === 'horizontal' ? 1 : 0;
                        for (let i = 0; i < p.palabra.length; i++) {{
                            if (p.fila_inicio + i * df === f && p.columna_inicio + i * dc === c) return true;
                        }}
                        return false;
                    }});

                    if (esNegra) {{
                        celda.classList.add('negra');
                        tablero.appendChild(celda);
                        continue;
                    }}

                    const palabraInicio = PALABRAS.find(p => p.fila_inicio === f && p.columna_inicio === c);
                    if (palabraInicio) {{
                        const num = document.createElement('span');
                        num.className = 'numero';
                        num.textContent = palabraInicio.numero || getNumero(palabraInicio);
                        celda.appendChild(num);
                    }}

                    const input = document.createElement('input');
                    input.type = 'text';
                    input.maxLength = 1;
                    input.dataset.fila = f;
                    input.dataset.columna = c;
                    input.addEventListener('focus', () => seleccionarCelda(f, c));
                    input.addEventListener('input', (e) => manejarInput(e, f, c));
                    input.addEventListener('keydown', (e) => manejarTeclaCelda(e, f, c));
                    input.addEventListener('click', (e) => {{ e.stopPropagation(); seleccionarCelda(f, c); }});
                    celda.appendChild(input);
                    tablero.appendChild(celda);
                }}
            }}
        }}

        function getNumero(palabra) {{
            const ordenadas = [...PALABRAS].sort((a, b) => {{
                if (a.fila_inicio !== b.fila_inicio) return a.fila_inicio - b.fila_inicio;
                return a.columna_inicio - b.columna_inicio;
            }});
            for (let i = 0; i < ordenadas.length; i++) {{
                if (ordenadas[i] === palabra) return i + 1;
            }}
            return 1;
        }}

        function renderPistas() {{
            const ph = document.getElementById('pistas-h');
            const pv = document.getElementById('pistas-v');
            ph.innerHTML = '';
            pv.innerHTML = '';

            PALABRAS.forEach(p => {{
                const div = document.createElement('div');
                div.className = 'pista-item';
                div.dataset.palabra = p.palabra;
                div.innerHTML = '<span class="num">' + (p.numero || getNumero(p)) + '.</span>' + p.pista;
                div.onclick = () => irAPalabra(p);
                if (p.direccion === 'horizontal') ph.appendChild(div);
                else pv.appendChild(div);
            }});
        }}

        function seleccionarCelda(f, c) {{
            celdaActiva = {{ fila: f, columna: c }};
            document.querySelectorAll('.celda').forEach(el => el.classList.remove('activa', 'seleccionada'));
            const celdaEl = getCeldaElement(f, c);
            if (celdaEl) celdaEl.classList.add('seleccionada');
            const palabra = encontrarPalabraEn(f, c, direccionActiva);
            if (palabra) resaltarPalabra(palabra);
            document.querySelectorAll('.pista-item').forEach(el => el.classList.remove('activa'));
            if (palabra) {{
                const pistaEl = document.querySelector('.pista-item[data-palabra="' + palabra.palabra + '"]');
                if (pistaEl) pistaEl.classList.add('activa');
            }}
        }}

        function encontrarPalabraEn(f, c, direccion) {{
            return PALABRAS.find(p => {{
                if (p.direccion !== direccion) return false;
                const df = direccion === 'horizontal' ? 0 : 1;
                const dc = direccion === 'horizontal' ? 1 : 0;
                for (let i = 0; i < p.palabra.length; i++) {{
                    if (p.fila_inicio + i * df === f && p.columna_inicio + i * dc === c) return true;
                }}
                return false;
            }});
        }}

        function resaltarPalabra(palabra) {{
            const df = palabra.direccion === 'horizontal' ? 0 : 1;
            const dc = palabra.direccion === 'horizontal' ? 1 : 0;
            for (let i = 0; i < palabra.palabra.length; i++) {{
                const el = getCeldaElement(palabra.fila_inicio + i * df, palabra.columna_inicio + i * dc);
                if (el) el.classList.add('activa');
            }}
        }}

        function getCeldaElement(f, c) {{
            return document.querySelector('.celda[data-fila="' + f + '"][data-columna="' + c + '"]');
        }}

        function getInput(f, c) {{
            const celda = getCeldaElement(f, c);
            return celda ? celda.querySelector('input') : null;
        }}

        function irAPalabra(palabra) {{
            direccionActiva = palabra.direccion;
            seleccionarCelda(palabra.fila_inicio, palabra.columna_inicio);
            const input = getInput(palabra.fila_inicio, palabra.columna_inicio);
            if (input) input.focus();
        }}

        function manejarInput(e, f, c) {{
            const val = e.target.value.toUpperCase();
            e.target.value = val;
            if (val.length === 1) {{
                moverSiguiente(f, c);
            }}
        }}

        function manejarTeclaCelda(e, f, c) {{
            if (e.key === 'Enter') {{ e.preventDefault(); verificarTodo(); return; }}
            if (e.key === 'Backspace' && !e.target.value) {{ e.preventDefault(); moverAnterior(f, c); return; }}
            if (e.key === 'ArrowRight') {{ direccionActiva = 'horizontal'; mover(f, c, 0, 1); }}
            if (e.key === 'ArrowLeft') {{ direccionActiva = 'horizontal'; mover(f, c, 0, -1); }}
            if (e.key === 'ArrowDown') {{ direccionActiva = 'vertical'; mover(f, c, 1, 0); }}
            if (e.key === 'ArrowUp') {{ direccionActiva = 'vertical'; mover(f, c, -1, 0); }}
            if (e.key === ' ') {{ e.preventDefault(); direccionActiva = direccionActiva === 'horizontal' ? 'vertical' : 'horizontal'; seleccionarCelda(f, c); }}
        }}

        function manejarTecla(e) {{
            if (e.key === 'Tab') {{
                e.preventDefault();
                if (e.shiftKey) moverAnterior(celdaActiva.fila, celdaActiva.columna);
                else moverSiguiente(celdaActiva.fila, celdaActiva.columna);
            }}
        }}

        function mover(f, c, df, dc) {{
            const nf = f + df, nc = c + dc;
            const input = getInput(nf, nc);
            if (input) {{ input.focus(); seleccionarCelda(nf, nc); }}
        }}

        function moverSiguiente(f, c) {{
            const palabra = encontrarPalabraEn(f, c, direccionActiva);
            if (!palabra) return;
            const df = palabra.direccion === 'horizontal' ? 0 : 1;
            const dc = palabra.direccion === 'horizontal' ? 1 : 0;
            const idx = Math.abs((f - palabra.fila_inicio) + (c - palabra.columna_inicio));
            if (idx + 1 < palabra.palabra.length) {{ mover(f, c, df, dc); }}
        }}

        function moverAnterior(f, c) {{
            const palabra = encontrarPalabraEn(f, c, direccionActiva);
            if (!palabra) return;
            const df = palabra.direccion === 'horizontal' ? 0 : 1;
            const dc = palabra.direccion === 'horizontal' ? 1 : 0;
            const idx = Math.abs((f - palabra.fila_inicio) + (c - palabra.columna_inicio));
            if (idx > 0) {{ mover(f, c, -df, -dc); }}
        }}

        function tecladoVirtual(tecla) {{
            if (!celdaActiva) return;
            const input = getInput(celdaActiva.fila, celdaActiva.columna);
            if (!input) return;
            if (tecla === 'BACKSPACE') {{
                if (input.value) {{ input.value = ''; }}
                else {{ moverAnterior(celdaActiva.fila, celdaActiva.columna); }}
            }} else {{
                input.value = tecla;
                input.dispatchEvent(new Event('input'));
            }}
        }}

        function verificarTodo() {{
            let correctas = 0;
            let totalLetras = 0;
            let letrasCorrectas = 0;

            PALABRAS.forEach(p => {{
                const df = p.direccion === 'horizontal' ? 0 : 1;
                const dc = p.direccion === 'horizontal' ? 1 : 0;
                let palabraCorrecta = true;

                for (let i = 0; i < p.palabra.length; i++) {{
                    const f = p.fila_inicio + i * df;
                    const c = p.columna_inicio + i * dc;
                    const input = getInput(f, c);
                    const letraCorrecta = p.palabra[i].toUpperCase();
                    totalLetras++;

                    if (input) {{
                        const val = input.value.toUpperCase();
                        const celda = getCeldaElement(f, c);
                        if (val === letraCorrecta) {{
                            letrasCorrectas++;
                            celda.classList.remove('incorrecta');
                            celda.classList.add('correcta');
                        }} else if (val) {{
                            palabraCorrecta = false;
                            celda.classList.remove('correcta');
                            celda.classList.add('incorrecta');
                        }} else {{
                            palabraCorrecta = false;
                            celda.classList.remove('correcta', 'incorrecta');
                        }}
                    }}
                }}

                if (palabraCorrecta && p.palabra.length > 0) {{
                    correctas++;
                    palabrasCompletadas.add(p.palabra);
                    const pistaEl = document.querySelector('.pista-item[data-palabra="' + p.palabra + '"]');
                    if (pistaEl) pistaEl.classList.add('completada');
                }}
            }});

            actualizarProgreso();

            if (correctas === PALABRAS.length) {{
                mostrarMensaje('FELICITACIONES: Completaste todo el crucigrama.', 'exito');
            }} else if (letrasCorrectas === totalLetras) {{
                mostrarMensaje('Vas muy bien. Llevas ' + correctas + ' de ' + PALABRAS.length + ' palabras.', 'exito');
            }} else {{
                mostrarMensaje('Sigue intentando. Llevas ' + correctas + ' de ' + PALABRAS.length + ' palabras correctas.', 'pista-msg');
            }}
        }}

        function actualizarProgreso() {{
            const completadas = palabrasCompletadas.size;
            const total = PALABRAS.length;
            const porcentaje = total > 0 ? Math.round((completadas / total) * 100) : 0;
            document.getElementById('contador').textContent = completadas + ' / ' + total + ' palabras';
            document.getElementById('porcentaje').textContent = porcentaje + '%';
            document.getElementById('barra-relleno').style.width = porcentaje + '%';
        }}

        function darPista() {{
            if (!celdaActiva) {{ mostrarMensaje('Selecciona una celda primero.', 'error'); return; }}
            const palabra = encontrarPalabraEn(celdaActiva.fila, celdaActiva.columna, direccionActiva);
            if (!palabra) {{ mostrarMensaje('No hay palabra en esta direccion.', 'error'); return; }}
            const df = palabra.direccion === 'horizontal' ? 0 : 1;
            const dc = palabra.direccion === 'horizontal' ? 1 : 0;
            for (let i = 0; i < palabra.palabra.length; i++) {{
                const f = palabra.fila_inicio + i * df;
                const c = palabra.columna_inicio + i * dc;
                const input = getInput(f, c);
                if (input && !input.value) {{
                    input.value = palabra.palabra[i].toUpperCase();
                    input.dispatchEvent(new Event('input'));
                    mostrarMensaje('Se revelo una letra de \"' + palabra.palabra + '\"', 'pista-msg');
                    return;
                }}
            }}
            mostrarMensaje('Esa palabra ya esta completa.', 'exito');
        }}

        function limpiarErrores() {{
            document.querySelectorAll('.celda.incorrecta').forEach(el => {{
                el.classList.remove('incorrecta');
                const input = el.querySelector('input');
                if (input) input.value = '';
            }});
            mostrarMensaje('Errores limpiados.', 'pista-msg');
        }}

        function reiniciar() {{
            if (!confirm('Seguro que quieres borrar todo y empezar de nuevo?')) return;
            document.querySelectorAll('input').forEach(input => input.value = '');
            document.querySelectorAll('.celda').forEach(el => el.classList.remove('correcta', 'incorrecta'));
            document.querySelectorAll('.pista-item').forEach(el => el.classList.remove('completada'));
            palabrasCompletadas.clear();
            actualizarProgreso();
            mostrarMensaje('Crucigrama reiniciado.', 'pista-msg');
        }}

        function mostrarMensaje(texto, tipo) {{
            const msg = document.getElementById('mensaje');
            msg.textContent = texto;
            msg.className = 'mensaje visible ' + tipo;
            setTimeout(() => {{ msg.classList.remove('visible'); }}, 3000);
        }}

        init();
        """

        teclado_html = """
        <div class="teclado" id="teclado">
            <button class="tecla" onclick="tecladoVirtual('A')">A</button>
            <button class="tecla" onclick="tecladoVirtual('B')">B</button>
            <button class="tecla" onclick="tecladoVirtual('C')">C</button>
            <button class="tecla" onclick="tecladoVirtual('D')">D</button>
            <button class="tecla" onclick="tecladoVirtual('E')">E</button>
            <button class="tecla" onclick="tecladoVirtual('F')">F</button>
            <button class="tecla" onclick="tecladoVirtual('G')">G</button>
            <button class="tecla" onclick="tecladoVirtual('H')">H</button>
            <button class="tecla" onclick="tecladoVirtual('I')">I</button>
            <button class="tecla" onclick="tecladoVirtual('J')">J</button>
            <button class="tecla" onclick="tecladoVirtual('K')">K</button>
            <button class="tecla" onclick="tecladoVirtual('L')">L</button>
            <button class="tecla" onclick="tecladoVirtual('M')">M</button>
            <button class="tecla" onclick="tecladoVirtual('N')">N</button>
            <button class="tecla" onclick="tecladoVirtual('\u00D1')">\u00D1</button>
            <button class="tecla" onclick="tecladoVirtual('O')">O</button>
            <button class="tecla" onclick="tecladoVirtual('P')">P</button>
            <button class="tecla" onclick="tecladoVirtual('Q')">Q</button>
            <button class="tecla" onclick="tecladoVirtual('R')">R</button>
            <button class="tecla" onclick="tecladoVirtual('S')">S</button>
            <button class="tecla" onclick="tecladoVirtual('T')">T</button>
            <button class="tecla" onclick="tecladoVirtual('U')">U</button>
            <button class="tecla" onclick="tecladoVirtual('V')">V</button>
            <button class="tecla" onclick="tecladoVirtual('W')">W</button>
            <button class="tecla" onclick="tecladoVirtual('X')">X</button>
            <button class="tecla" onclick="tecladoVirtual('Y')">Y</button>
            <button class="tecla" onclick="tecladoVirtual('Z')">Z</button>
            <button class="tecla tecla-borrar" onclick="tecladoVirtual('BACKSPACE')">\u232B</button>
        </div>
        """

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{self.title}</title>
    <style>{css}</style>
</head>
<body>
    <div class="contenedor">
        <header>
            <h1>{self.title}</h1>
            <div class="tema">{self.tema}</div>
        </header>

        <div class="resena">
            <h3>Resena del tema</h3>
            <p>{resena_html}</p>
        </div>

        <div class="barra-progreso">
            <div class="info">
                <span id="contador">0 / {total_palabras} palabras</span>
            </div>
            <div class="progreso-visual">
                <div class="relleno" id="barra-relleno"></div>
            </div>
            <div class="info" id="porcentaje">0%</div>
        </div>

        <div class="botones">
            <button class="btn btn-primario" onclick="verificarTodo()">Verificar</button>
            <button class="btn btn-pista" onclick="darPista()">Mostrar pista</button>
            <button class="btn btn-secundario" onclick="limpiarErrores()">Limpiar errores</button>
            <button class="btn btn-secundario" onclick="reiniciar()">Reiniciar</button>
        </div>

        <div class="layout">
            <div class="tablero-wrapper">
                <div class="tablero" id="tablero"></div>
            </div>

            <div class="pistas">
                <h3>Horizontales</h3>
                <div id="pistas-h"></div>
                <h3 style="margin-top: 16px;">Verticales</h3>
                <div id="pistas-v"></div>
            </div>
        </div>

        <footer>
            Escuela del Pensamiento - Crucigrama interactivo
        </footer>
    </div>

    <div class="mensaje" id="mensaje"></div>
    {teclado_html}

    <script>{js}</script>
</body>
</html>"""

        return html