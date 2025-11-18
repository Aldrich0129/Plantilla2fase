"""Interfaz Streamlit para la Fase 2."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Dict

import streamlit as st

from modules.phase2_core import ReportFiller
from utils_v2 import Validator


def _render_input(var: Dict):
    nombre = var.get("nombre")
    var_type = var.get("tipo", "texto")
    pregunta = var.get("pregunta", f"Valor para {nombre}")
    opciones = var.get("opciones")

    if var_type == "lista" and opciones:
        return st.selectbox(pregunta, opciones, key=nombre)
    if var_type in {"numero", "moneda"}:
        return st.number_input(pregunta, key=nombre)
    return st.text_input(pregunta, key=nombre)


def run_ui():
    st.set_page_config(page_title="Fase 2 · Rellenar plantilla", page_icon="✅", layout="wide")
    st.title("Fase 2: Generador de Informe Completo")
    st.write("Sube la plantilla y el YAML para rellenar las variables.")

    template_file = st.file_uploader("Plantilla DOCX o PPTX", type=["docx", "pptx"])
    yaml_file = st.file_uploader("Archivo YAML", type=["yaml", "yml"])

    if template_file and yaml_file:
        workdir = Path(tempfile.mkdtemp())
        filler = ReportFiller(workdir)
        template_path = workdir / template_file.name
        template_path.write_bytes(template_file.getbuffer())
        yaml_path = workdir / yaml_file.name
        yaml_path.write_bytes(yaml_file.getbuffer())

        variables = filler.load_schema(yaml_path)
        st.subheader("Valores a completar")

        with st.form("values_form"):
            collected: Dict[str, str] = {}
            for var in variables:
                collected[var["nombre"]] = _render_input(var)
            submitted = st.form_submit_button("Generar informe")

        if submitted:
            errors = _validate(collected, variables)
            if errors:
                st.error("\n".join(errors))
                return
            output_path = filler.fill(template_path, collected)
            with open(output_path, "rb") as fh:
                st.download_button(
                    "⬇️ Descargar informe",
                    data=fh,
                    file_name=output_path.name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    if output_path.suffix == ".docx"
                    else "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                )


def _validate(collected: Dict[str, str], variables: Dict) -> Dict[str, str]:
    errors = []
    for var in variables:
        name = var.get("nombre")
        value = collected.get(name)
        var_type = var.get("tipo")
        if var_type == "email" and value and not Validator.validate_email(value):
            errors.append(f"{name}: email inválido")
        if var_type == "telefono" and value and not Validator.validate_phone(str(value)):
            errors.append(f"{name}: teléfono inválido")
        if var_type == "fecha" and value and not Validator.validate_date(str(value)):
            errors.append(f"{name}: fecha inválida (DD/MM/YYYY)")
        if var_type == "hora" and value and not Validator.validate_time(str(value)):
            errors.append(f"{name}: hora inválida (HH:MM)")
    return errors


if __name__ == "__main__":
    run_ui()
