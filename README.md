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
   normalizada junto al YAML generado. La detección ahora clasifica cada variable por tipo (texto,
   moneda, porcentaje, fecha, hora, lista, booleano…) y categoría consultora (identificación,
   financiera, temporal, geografía, riesgo, proyecto). El YAML incluye formato sugerido y ejemplo
   para acelerar la captura.
3. Ejecuta la Fase 2:
   ```bash
   streamlit run F2Generador.py
   ```
   Sube la plantilla y el YAML, completa los valores y descarga el informe final. Además del informe
   se generan:
   - `*_manifest.yaml` con todos los valores aplicados para trazabilidad.
   - `*_entrega.zip` con informe + manifiesto + resumen TXT, listo para envío a cliente o archivo de evidencia.

## Mejoras para operaciones Big4

- **Taxonomía ampliada de variables:** detección de porcentajes, booleanos de control, ubicaciones, listas y
  campos financieros con formato sugerido y ejemplos. Cada variable queda asociada a una categoría (financiera,
  temporal, geográfica, identificación, gobierno/riesgo o proyecto) para filtrar y auditar.
- **YAML enriquecido:** el archivo de esquema incluye preguntas sugeridas, ejemplos, formato esperado, indicador de
  requeridos y el marcador original detectado.
- **Entrega auditada en Fase 2:** al generar un informe se construye un manifiesto YAML y un paquete ZIP con
  resumen de valores aplicados, facilitando revisión de calidad, archivo de evidencia y trazabilidad.

## Pruebas

El proyecto incluye módulos desacoplados para facilitar pruebas programáticas. Consulta
`modules/phase1_core.py` y `modules/phase2_core.py` para usar las clases directamente en
scripts o notebooks sin cargar Streamlit.
