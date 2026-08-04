import json
import os


class ThemeLoader:
    """Carga temas desde archivos JSON. No requiere editar código Python."""

    @staticmethod
    def load_from_json(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not data:
            raise ValueError("El archivo JSON está vacío.")
        semana_key = list(data.keys())[0]
        semana = data[semana_key]
        crucigramas = []
        for cw in semana.get("crucigramas", []):
            words = []
            clues = {}
            for item in cw.get("palabras", []):
                palabra = item["palabra"].strip().upper()
                pista = item["pista"].strip()
                words.append(palabra)
                clues[palabra] = pista
            crucigramas.append({
                "tema": cw.get("tema", "Sin tema"),
                "resena": cw.get("resena", ""),
                "words": words,
                "clues": clues,
            })
        return {
            "nombre_guia": semana.get("nombre_guia", "Guía Semanal"),
            "crucigramas": crucigramas
        }

    @staticmethod
    def validate_crucigrama(crucigrama):
        errores = []
        words = crucigrama.get("words", [])
        clues = crucigrama.get("clues", {})
        if len(words) == 0:
            errores.append("No hay palabras.")
        if len(words) < 10:
            errores.append(f"Solo {len(words)} palabras. Se recomiendan al menos 15.")
        sin_pista = [w for w in words if w not in clues or not clues[w]]
        if sin_pista:
            errores.append(f"Palabras sin pista: {sin_pista}")
        for palabra in clues:
            if palabra not in words:
                errores.append(f"Pista para '{palabra}' no tiene palabra correspondiente.")
        return len(errores) == 0, errores