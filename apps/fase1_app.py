"""Interfaz Streamlit para la Fase 1."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import List

import streamlit as st

from modules.phase1_core import DetectedVariable, TemplateBuilder


def _show_detected_variables(detected: List[DetectedVariable]):
    st.subheader("Variables detectadas")
    if not detected:
        st.info("No se detectaron marcadores en el documento.")
        return
    for var in detected:
        st.markdown(
            f"- **{var.nombre}** → marcador original `{var.marcador_original}` · tipo sugerido: `{var.tipo}`"
        )


def run_ui():
    st.set_page_config(page_title="Fase 1 · Generar plantilla", page_icon="📝", layout="wide")
    st.title("Fase 1: Generador de Plantillas")
    st.write("Carga un DOCX o PPTX con marcadores y obtén la plantilla normalizada más su YAML.")

    uploaded = st.file_uploader("Selecciona un archivo .docx o .pptx", type=["docx", "pptx"])

    if uploaded:
        workdir = Path(tempfile.mkdtemp())
        builder = TemplateBuilder(workdir)
        saved_path = builder.save_upload(uploaded.getbuffer(), uploaded.name)

        if st.button("Generar plantilla", use_container_width=True):
            try:
                template_path, yaml_path, detected = builder.build_outputs(saved_path)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Error al procesar el archivo: {exc}")
                return

            _show_detected_variables(detected)

            col1, col2 = st.columns(2)
            with open(template_path, "rb") as fh:
                col1.download_button(
                    "📄 Descargar plantilla",
                    data=fh,
                    file_name=template_path.name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    if template_path.suffix == ".docx"
                    else "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                )
            with open(yaml_path, "rb") as fh:
                col2.download_button(
                    "🧾 Descargar YAML",
                    data=fh,
                    file_name=yaml_path.name,
                    mime="text/yaml",
                    use_container_width=True,
                )


if __name__ == "__main__":
    run_ui()
