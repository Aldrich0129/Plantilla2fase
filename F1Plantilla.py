"""Entrada Streamlit para la Fase 1.

La lógica pesada vive en ``modules``; aquí solo lanzamos la UI mínima.
"""
from __future__ import annotations

from apps.fase1_app import run_ui


if __name__ == "__main__":
    run_ui()
