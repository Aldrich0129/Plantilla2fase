"""Lógica desacoplada para la Fase 2 (relleno de plantillas)."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from docx import Document
from pptx import Presentation

from utils_v2 import DocumentProcessor, YAMLManager


class ReportFiller:
    def __init__(self, workdir: Path):
        self.workdir = Path(workdir)
        self.workdir.mkdir(parents=True, exist_ok=True)

    def load_schema(self, yaml_path: Path) -> List[Dict]:
        data = YAMLManager.load_yaml(str(yaml_path))
        return data.get("variables", []) if data else []

    def fill(self, template_path: Path, values: Dict[str, str]) -> Path:
        suffix = template_path.suffix.lower()
        if suffix == ".docx":
            filled = self._fill_docx(template_path, values)
        elif suffix == ".pptx":
            filled = self._fill_pptx(template_path, values)
        else:
            raise ValueError("Formato no soportado. Usa .docx o .pptx")
        return filled

    def _fill_docx(self, template_path: Path, values: Dict[str, str]) -> Path:
        doc = Document(template_path)
        doc = DocumentProcessor.replace_in_docx(doc, values)
        output = self.workdir / f"{template_path.stem}_completado.docx"
        doc.save(output)
        return output

    def _fill_pptx(self, template_path: Path, values: Dict[str, str]) -> Path:
        prs = Presentation(template_path)
        prs = DocumentProcessor.replace_in_pptx(prs, values)
        output = self.workdir / f"{template_path.stem}_completado.pptx"
        prs.save(output)
        return output


__all__ = ["ReportFiller"]
