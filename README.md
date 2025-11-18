# Generador de plantillas en dos fases

Esta versión reorganiza el proyecto en dos capas: interfaces ligeras con Streamlit y
módulos reutilizables con toda la lógica de procesamiento para documentos Word y PowerPoint.

## Estructura

```
apps/
  fase1_app.py   # UI de la Fase 1 (creación de plantilla y YAML)
  fase2_app.py   # UI de la Fase 2 (relleno de plantillas)
modules/
  phase1_core.py # Detección de variables y generación de plantillas
  phase2_core.py # Relleno de plantillas a partir de YAML
  text_utils.py  # Utilidades comunes para marcadores y tipos
F1Plantilla.py   # Punto de entrada para la UI de la Fase 1
F2Generador.py   # Punto de entrada para la UI de la Fase 2
utils_v2.py      # Librería de soporte existente (detección y reemplazo)
```

## Uso rápido

1. Instala dependencias (`pip install -r requirements.txt`).
2. Ejecuta la Fase 1 en un terminal:
   ```bash
   streamlit run F1Plantilla.py
   ```
   Carga un `.docx` o `.pptx` con marcadores (`{{variable}}`, `[variable]`, etc.) y descarga la plantilla
   normalizada junto al YAML generado.
3. Ejecuta la Fase 2:
   ```bash
   streamlit run F2Generador.py
   ```
   Sube la plantilla y el YAML, completa los valores y descarga el informe final.

## Pruebas

El proyecto incluye módulos desacoplados para facilitar pruebas programáticas. Consulta
`modules/phase1_core.py` y `modules/phase2_core.py` para usar las clases directamente en
scripts o notebooks sin cargar Streamlit.
