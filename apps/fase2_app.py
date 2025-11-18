"""Interfaz Streamlit para la Fase 2."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Dict, List

import streamlit as st

from modules.phase2_core import ReportFiller
from utils_v2 import Validator


def _render_input(var: Dict):
    nombre = var.get("nombre")
    var_type = var.get("tipo", "texto")
    pregunta = var.get("pregunta", f"Valor para {nombre}")
    opciones = var.get("opciones")
    help_text = " / ".join(filter(None, [var.get("categoria"), var.get("formato")]))

    if help_text:
        st.caption(f"{nombre}: {help_text}")

    if var_type == "lista" and opciones:
        return st.selectbox(pregunta, opciones, key=nombre)
    if var_type in {"numero", "moneda"}:
        return st.number_input(pregunta, key=nombre, format="%0.2f")
    if var_type == "porcentaje":
        return st.number_input(pregunta, key=nombre, min_value=0.0, max_value=100.0, step=0.1, format="%0.2f")
    if var_type == "booleano":
        choice = st.selectbox(pregunta, ["Sí", "No"], key=nombre)
        return choice
    if var_type == "fecha":
        date_val = st.date_input(pregunta, key=nombre)
        return date_val.strftime("%d/%m/%Y") if date_val else ""
    if var_type == "hora":
        time_val = st.time_input(pregunta, key=nombre)
        return time_val.strftime("%H:%M") if time_val else ""
    if var_type == "texto_largo":
        return st.text_area(pregunta, key=nombre)
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

        variables: List[Dict] = filler.load_schema(yaml_path)
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
            output_path, manifest_path, package_path = filler.generate_delivery(template_path, collected, variables)

            st.success("Informe generado y auditado correctamente.")
            with st.expander("Revisión rápida de valores"):
                for key, value in collected.items():
                    st.write(f"**{key}** → {value}")

            col1, col2, col3 = st.columns(3)
            with open(output_path, "rb") as fh:
                col1.download_button(
                    "⬇️ Informe",
                    data=fh,
                    file_name=output_path.name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    if output_path.suffix == ".docx"
                    else "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                )
            with open(manifest_path, "rb") as fh:
                col2.download_button(
                    "🧾 Manifesto YAML",
                    data=fh,
                    file_name=manifest_path.name,
                    mime="text/yaml",
                    use_container_width=True,
                )
            with open(package_path, "rb") as fh:
                col3.download_button(
                    "📦 Paquete Big4",
                    data=fh,
                    file_name=package_path.name,
                    mime="application/zip",
                    use_container_width=True,
                )


def _validate(collected: Dict[str, str], variables: Dict) -> Dict[str, str]:
    errors = []
    for var in variables:
        name = var.get("nombre")
        value = collected.get(name)
        var_type = var.get("tipo")
        requerido = var.get("requerido", True)
        if requerido and (value is None or value == ""):
            errors.append(f"{name}: es requerido")
        if var_type == "email" and value and not Validator.validate_email(value):
            errors.append(f"{name}: email inválido")
        if var_type == "telefono" and value and not Validator.validate_phone(str(value)):
            errors.append(f"{name}: teléfono inválido")
        if var_type == "fecha" and value and not Validator.validate_date(str(value)):
            errors.append(f"{name}: fecha inválida (DD/MM/YYYY)")
        if var_type == "hora" and value and not Validator.validate_time(str(value)):
            errors.append(f"{name}: hora inválida (HH:MM)")
        if var_type == "porcentaje" and value not in {None, ""}:
            try:
                pct = float(value)
                if pct < 0 or pct > 100:
                    errors.append(f"{name}: el porcentaje debe estar entre 0 y 100")
            except ValueError:
                errors.append(f"{name}: ingrese un valor numérico para porcentaje")
        if var_type in {"numero", "moneda"} and value not in {None, ""}:
            if not Validator.validate_number(str(value)):
                errors.append(f"{name}: valor numérico inválido")
    return errors


if __name__ == "__main__":
    run_ui()
