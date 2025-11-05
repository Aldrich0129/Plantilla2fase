# 📦 ESTRUCTURA DEL PROYECTO

## 📂 Archivos del Sistema

```
sistema-automatizacion-plantillas/
│
├── 📄 requirements.txt                     # Dependencias Python
│
├── 📚 DOCUMENTACIÓN
│   ├── README.md                          # Documentación completa
│   ├── INICIO_RAPIDO.md                   # Guía de inicio rápido
│   └── ESTRUCTURA_PROYECTO.md             # Este archivo
│
├── 🔧 CÓDIGO FUENTE
│   ├── utils.py                           # Librería común de utilidades
│   ├── fase1_generador_plantillas.py     # Aplicación Fase 1
│   └── fase2_generador_informes.py       # Aplicación Fase 2
│
├── 📝 EJEMPLOS
│   ├── ejemplo_informe.docx              # Documento Word de ejemplo
│   └── crear_ejemplo.py                   # Script para crear ejemplos
│
└── 🎯 ARCHIVOS GENERADOS (en uso)
    ├── plantilla_*.docx/pptx             # Plantillas normalizadas
    ├── *_config.yaml                      # Configuraciones YAML
    └── informe_*.docx/pptx               # Informes finales generados
```

## 📋 Descripción de Archivos

### 🔹 Archivos Esenciales (SIEMPRE necesarios)

| Archivo | Descripción | Tamaño |
|---------|-------------|--------|
| `requirements.txt` | Lista de dependencias Python | ~100 bytes |
| `utils.py` | Funciones compartidas (detección, validación, YAML) | ~12 KB |
| `fase1_generador_plantillas.py` | App para crear plantillas | ~19 KB |
| `fase2_generador_informes.py` | App para generar informes | ~14 KB |

### 📘 Archivos de Documentación (RECOMENDADOS)

| Archivo | Descripción | Cuándo Leer |
|---------|-------------|-------------|
| `README.md` | Documentación completa del sistema | Primera instalación |
| `INICIO_RAPIDO.md` | Guía de inicio en 5 minutos | Primer uso |
| `ESTRUCTURA_PROYECTO.md` | Este archivo - estructura del proyecto | Organización |

### 📝 Archivos de Ejemplo (OPCIONALES)

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| `ejemplo_informe.docx` | Documento con 11 variables de ejemplo | Pruebas y aprendizaje |
| `crear_ejemplo.py` | Script para generar documentos de ejemplo | Crear más ejemplos |

## 🔄 Flujo de Archivos

```
┌──────────────────────┐
│  Documento Original  │
│     (.docx/.pptx)    │
└──────────┬───────────┘
           │
           ▼
    ┌──────────────┐
    │   FASE 1     │
    │ (Plantillas) │
    └──────┬───────┘
           │
           ├──► 📄 plantilla_X.docx/pptx  (Plantilla normalizada)
           │
           └──► ⚙️ plantilla_X_config.yaml (Configuración de variables)
                     │
                     ▼
              ┌──────────────┐
              │   FASE 2     │
              │  (Informes)  │
              └──────┬───────┘
                     │
                     └──► 📊 informe_final.docx/pptx (Documento completo)
```

## 💾 Requisitos de Espacio

| Componente | Espacio en Disco |
|------------|------------------|
| Código fuente | ~50 KB |
| Documentación | ~20 KB |
| Dependencias Python | ~200 MB (primera instalación) |
| Documento de ejemplo | ~40 KB |
| **Total inicial** | **~200 MB** |

### Por Uso:
- Plantilla generada: ~40-100 KB (según documento original)
- Config YAML: ~1-5 KB
- Informe final: ~40-100 KB (similar al original)

## 🗂️ Organización Recomendada

### Para Uso en Despacho:

```
servidor-despacho/
│
├── sistema/                          # Código del sistema
│   ├── requirements.txt
│   ├── utils.py
│   ├── fase1_generador_plantillas.py
│   └── fase2_generador_informes.py
│
├── documentacion/                    # Guías y manuales
│   ├── README.md
│   ├── INICIO_RAPIDO.md
│   └── ESTRUCTURA_PROYECTO.md
│
├── plantillas/                       # Plantillas generadas
│   ├── contratos/
│   │   ├── contrato_alquiler.docx
│   │   └── contrato_alquiler_config.yaml
│   │
│   ├── informes/
│   │   ├── informe_mensual.docx
│   │   └── informe_mensual_config.yaml
│   │
│   └── presentaciones/
│       ├── propuesta_cliente.pptx
│       └── propuesta_cliente_config.yaml
│
└── informes_generados/              # Informes finales (por fecha)
    ├── 2025-10/
    │   ├── informe_cliente_A_20251015.docx
    │   └── informe_cliente_B_20251022.docx
    │
    └── 2025-11/
        └── ...
```

## 🔐 Archivos Sensibles

⚠️ **IMPORTANTE:** Los siguientes archivos pueden contener datos confidenciales:

| Archivo | Tipo de Datos | Acción |
|---------|---------------|--------|
| `*_config.yaml` | Preguntas, opciones de variables | Revisar antes de compartir |
| `informe_*.docx/pptx` | Datos reales de clientes | **NO compartir** |
| Plantillas finales | Pueden tener estructura sensible | Evaluar caso por caso |

### ✅ Archivos Seguros para Compartir:
- `requirements.txt`
- `utils.py`
- `fase1_generador_plantillas.py`
- `fase2_generador_informes.py`
- `README.md`
- `INICIO_RAPIDO.md`
- `ejemplo_informe.docx` (ejemplo genérico)

## 📤 Migración/Backup

### Archivos Mínimos para Backup:

**Sistema completo:**
```bash
# Crear backup
tar -czf backup_sistema_$(date +%Y%m%d).tar.gz \
  requirements.txt \
  utils.py \
  fase1_generador_plantillas.py \
  fase2_generador_informes.py \
  README.md
```

**Solo plantillas:**
```bash
# Backup de plantillas
tar -czf backup_plantillas_$(date +%Y%m%d).tar.gz \
  plantillas/
```

### Restauración en Nuevo Servidor:

1. Descomprimir archivos del sistema
2. Instalar dependencias: `pip install -r requirements.txt`
3. Copiar carpeta de plantillas (si existe)
4. Ejecutar: `streamlit run fase1_generador_plantillas.py`

## 🔄 Actualización del Sistema

Al actualizar el sistema:

### ✅ Archivos que PUEDES actualizar:
- `utils.py`
- `fase1_generador_plantillas.py`
- `fase2_generador_informes.py`
- `requirements.txt`

### ⚠️ Archivos que NO DEBES modificar:
- Plantillas ya generadas (`.docx`, `.pptx`)
- Archivos YAML de configuración
- Informes finales generados

### 📝 Proceso de Actualización:

```bash
# 1. Backup del sistema actual
tar -czf backup_antes_actualizar.tar.gz sistema/

# 2. Reemplazar archivos del sistema
cp nuevo_utils.py utils.py
cp nueva_fase1.py fase1_generador_plantillas.py
cp nueva_fase2.py fase2_generador_informes.py

# 3. Actualizar dependencias si es necesario
pip install --break-system-packages -r requirements.txt --upgrade

# 4. Probar con documento de ejemplo
streamlit run fase1_generador_plantillas.py
```

## 📊 Estadísticas de Uso

Para monitorizar el uso del sistema:

```bash
# Contar plantillas generadas
ls plantillas/*_config.yaml | wc -l

# Contar informes generados este mes
ls informes_generados/$(date +%Y-%m)/ | wc -l

# Ver tamaño total de plantillas
du -sh plantillas/

# Ver tamaño total de informes
du -sh informes_generados/
```

---

💡 **Consejo:** Mantén esta estructura organizada desde el inicio para facilitar:
- Búsqueda rápida de plantillas
- Backups eficientes
- Trabajo en equipo
- Auditorías y control de versiones
