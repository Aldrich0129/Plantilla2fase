"""Utilities compartidas para el procesamiento de texto y placeholders."""
from __future__ import annotations

import re
import unicodedata
from typing import List, Optional

_SANITIZE_PATTERNS = [
    (r'[\[\(\{]\s*\{\{\s*([^\}]+?)\s*\}\}\s*[\]\)\}]', r"{{\1}}"),
    (r'\{\{\s*([^\}]+?)\s*\}\}\s*[\]\}\)]', r"{{\1}}"),
    (r'[\[\(\{]\s*\{\{\s*([^\}]+?)\s*\}\}', r"{{\1}}"),
    (r'\{\{\s*([^\}]+?)\s*\}\}', lambda m: "{{" + re.sub(r"\s+", "_", m.group(1).strip()) + "}}"),
]


def sanitize_placeholders(text: str) -> str:
    """Normaliza placeholders mal escritos como ``{{ var }}]`` -> ``{{var}}``.

    Args:
        text: Cadena a limpiar.

    Returns:
        Texto con marcadores limpiados.
    """

    t = unicodedata.normalize("NFKC", text).replace("\u00A0", " ")
    changed = True
    while changed:
        changed = False
        for pat, repl in _SANITIZE_PATTERNS:
            new_t = re.sub(pat, repl, t)
            if new_t != t:
                t = new_t
                changed = True
    return t


def clean_pattern_markers(text: str) -> str:
    """Elimina símbolos ``{{ }}``, ``[]`` o ``{ }`` alrededor del texto."""

    text = re.sub(r"\{\{([^}]+)\}\}", r"\1", text)
    text = re.sub(r"\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]", r"\1", text)
    return text.strip()


def infer_variable_type(text: str, options: Optional[List[str]] = None) -> str:
    """Devuelve un tipo aproximado de variable basándose en palabras clave.

    Se amplía la taxonomía para cubrir necesidades típicas de firmas de
    consultoría internacionales: porcentajes, booleanos de control, y
    campos financieros o de ubicación.
    """

    if options:
        return "lista"

    text_lower = text.lower()
    if any(tok in text_lower for tok in ["%", "porcentaje", "percent"]):
        return "porcentaje"
    if any(tok in text_lower for tok in ["si/no", "sí/no", "aplica", "aplicable", "yes/no", "true", "false"]):
        return "booleano"
    if any(tok in text_lower for tok in ["€", "eur", "euro", "euros", "usd", "$", "dólar", "dolar", "dólares", "dolares", "importe", "monto", "facturación", "ingreso", "tarifa"]):
        return "moneda"
    if any(word in text_lower for word in ["fecha", "date", "día", "mes", "año"]):
        return "fecha"
    if any(word in text_lower for word in ["hora", "time", "horario"]):
        return "hora"
    if any(word in text_lower for word in ["email", "correo", "mail"]):
        return "email"
    if any(word in text_lower for word in ["teléfono", "telefono", "phone", "móvil", "movil", "cel", "celular"]):
        return "telefono"
    if any(word in text_lower for word in ["número", "numero", "cantidad", "monto", "precio", "tasa"]):
        return "numero"
    if any(word in text_lower for word in ["país", "pais", "ciudad", "jurisdicción", "region", "oficina"]):
        return "ubicacion"
    return "texto"


def infer_variable_category(text: str, var_type: str) -> str:
    """Clasifica la variable en categorías consultoras estándar."""

    text_lower = text.lower()
    if var_type in {"email", "telefono"}:
        return "contacto"
    if var_type in {"fecha", "hora"}:
        return "temporal"
    if var_type in {"moneda", "numero", "porcentaje"}:
        return "financiera"
    if var_type == "ubicacion" or any(word in text_lower for word in ["pais", "ciudad", "jurisdiccion", "región", "region", "oficina"]):
        return "geografia"
    if any(word in text_lower for word in ["cliente", "empresa", "entidad", "compañía", "compania", "sociedad", "ruc", "nit", "rut"]):
        return "identificacion"
    if any(word in text_lower for word in ["riesgo", "control", "cumplimiento", "auditoria", "política", "politica"]):
        return "gobierno_riesgo"
    if any(word in text_lower for word in ["proyecto", "alcance", "entregable", "fase", "hito", "milestone", "engagement"]):
        return "proyecto"
    return "general"


def suggest_format(var_type: str) -> Optional[str]:
    """Sugiere un formato esperado para el tipo de variable."""

    formats = {
        "fecha": "DD/MM/AAAA",
        "hora": "HH:MM",
        "moneda": "9999999.99",
        "porcentaje": "0.00%",
        "telefono": "+[código]-#########",
    }
    return formats.get(var_type)


def hex_to_color_name(hex_color: str) -> str:
    """Convierte un color hex a una etiqueta amigable."""

    color_map = {
        "#ff0000": "🔴 Rojo",
        "#00ff00": "🟢 Verde Lima",
        "#0000ff": "🔵 Azul",
        "#ffff00": "🟡 Amarillo",
        "#ff00ff": "🟣 Magenta",
        "#00ffff": "🔵 Cian",
        "#000000": "⚫ Negro",
        "#ffffff": "⚪ Blanco",
        "#808080": "⚪ Gris",
        "#800000": "🔴 Rojo Oscuro",
        "#008000": "🟢 Verde",
        "#000080": "🔵 Azul Marino",
        "#808000": "🟡 Oliva",
        "#800080": "🟣 Púrpura",
        "#008080": "🔵 Verde Azulado",
        "#c0c0c0": "⚪ Plata",
        "#ff6600": "🟠 Naranja",
        "#ff9900": "🟠 Naranja Claro",
        "#993300": "🟤 Marrón",
        "#660000": "🔴 Granate",
        "#006600": "🟢 Verde Oscuro",
        "#003366": "🔵 Azul Oscuro",
        "#663399": "🟣 Púrpura Medio",
        "#336699": "🔵 Azul Acero",
    }

    if hex_color.lower() in color_map:
        return color_map[hex_color.lower()]

    hex_lower = hex_color.lower().replace("#", "")
    if len(hex_lower) == 6:
        r = int(hex_lower[0:2], 16)
        g = int(hex_lower[2:4], 16)
        b = int(hex_lower[4:6], 16)

        if r > 200 and g < 100 and b < 100:
            return "🔴 Rojo"
        if r < 100 and g > 200 and b < 100:
            return "🟢 Verde"
        if r < 100 and g < 100 and b > 200:
            return "🔵 Azul"
        if r > 200 and g > 200 and b < 100:
            return "🟡 Amarillo"
        if r > 200 and g < 100 and b > 200:
            return "🟣 Magenta"
        if r < 100 and g > 200 and b > 200:
            return "🔵 Cian"
        if r > 150 and g > 100 and b < 100:
            return "🟠 Naranja"
        if r > 100 and g < 100 and b > 150:
            return "🟣 Púrpura"
        if r < 50 and g < 50 and b < 50:
            return "⚫ Negro"
        if r > 200 and g > 200 and b > 200:
            return "⚪ Blanco"
        return "⚪ Gris"
    return hex_color
