"""Lógica desacoplada para la Fase 2 (relleno de plantillas)."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
from zipfile import ZipFile

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

    def generate_delivery(self, template_path: Path, values: Dict[str, str], schema: List[Dict]) -> Tuple[Path, Path, Path]:
        """Crea el informe final más un paquete de entrega para auditoría."""

        filled_path = self.fill(template_path, values)
        manifest = YAMLManager.create_value_manifest(values, schema, filled_path.name)
        manifest_path = self.workdir / f"{template_path.stem}_manifest.yaml"
        YAMLManager.save_yaml(manifest, str(manifest_path))

        package_path = self.workdir / f"{template_path.stem}_entrega.zip"
        with ZipFile(package_path, "w") as zf:
            zf.write(filled_path, filled_path.name)
            zf.write(manifest_path, manifest_path.name)
            zf.writestr("resumen.txt", self._build_summary(manifest))

        return filled_path, manifest_path, package_path

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

    @staticmethod
    def _build_summary(manifest: Dict[str, str]) -> str:
        lines = ["Resumen de entrega", "===================", ""]
        lines.append(f"Archivo: {manifest.get('informe')}")
        lines.append(f"Generado en: {manifest.get('generado_en')}")
        lines.append("")
        lines.append("Variables aplicadas:")
        for var in manifest.get('valores', []):
            lines.append(
                f"- {var.get('nombre')} ({var.get('tipo')}, {var.get('categoria')}): {var.get('valor')}"
            )
        return "\n".join(lines)


__all__ = ["ReportFiller"]
