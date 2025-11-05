# 📝 Sistema de Automatización de Plantillas v2.0

Sistema profesional de dos fases para automatizar la creación y generación de informes a partir de documentos Word y PowerPoint.

## 🎯 Descripción General

Este sistema permite:
- **Fase 1 (F1Plantilla.py)**: Detectar variables en documentos y generar plantillas normalizadas con configuración YAML
- **Fase 2 (F2Generador.py)**: Rellenar plantillas con datos del usuario y generar informes finales personalizados

## ✨ Características Principales

### 🔧 Fase 1: Generador de Plantillas

- ✅ Soporte para Word (.docx) y PowerPoint (.pptx)
- ✅ Detección de múltiples patrones de variables:
  - `{variable}` - Llaves simples
  - `{{variable}}` - Llaves dobles
  - `[variable]` - Corchetes simples
  - `[[variable]]` - Corchetes dobles
  - Variables con colores de texto específicos
  - Variables con colores de subrayado (Word)
- ✅ **Patrón combinado**: Detecta variables que cumplan AMBOS patrones simultáneamente (AND)
- ✅ **Detección de fechas con "de"**: Reconoce patrones como "día de mes de año" con prioridad
- ✅ **Gestión avanzada de variables**:
  - Fusionar múltiples variables en una
  - Dividir variables por delimitador (/, |, etc.)
  - División libre por selección de índices
  - División por contexto (seleccionar ubicaciones específicas)
  - Desactivar variables temporalmente
- ✅ **Visualización de contexto**: Ver dónde aparece cada variable en el documento
- ✅ **Prevención de duplicados**: Evita detectar variables solapadas
- ✅ Soporte para variables en tablas, encabezados y pies de página
- ✅ Generación automática de configuración YAML
- ✅ Preservación exacta del diseño original

### 🎨 Fase 2: Generador de Informes

- ✅ Carga de plantillas con variables normalizadas
- ✅ Formularios dinámicos según configuración YAML
- ✅ Tipos de datos soportados:
  - Texto libre
  - Números
  - Fechas (DD/MM/YYYY con selector de calendario)
  - Horas (HH:MM con selector de hora)
  - Emails (con validación)
  - Teléfonos (con prefijo internacional y validación)
  - Listas de opciones predefinidas
  - Moneda (EUR/USD con formato localizado)
- ✅ Validación opcional de datos
- ✅ Preservación del diseño original al 100%
- ✅ Reemplazo inteligente de variables manteniendo formato

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Contenido de requirements.txt:
```
streamlit==1.28.0
python-docx==1.1.0
python-pptx==0.6.23
PyYAML==6.0.1
Pillow==10.1.0
openpyxl==3.1.2
```

## 📖 Uso del Sistema

### Fase 1: Crear Plantilla

1. **Iniciar la aplicación:**
   ```bash
   streamlit run F1Plantilla.py
   ```

2. **Subir documento:**
   - Subir archivo Word (.docx) o PowerPoint (.pptx)
   - El documento debe tener variables marcadas con algún patrón

3. **Seleccionar patrones de detección:**
   - **Patrones de texto**: Marcar formatos como {}, [[]], etc.
   - **Patrones de color**: Seleccionar colores detectados en el documento
   - **Patrón combinado** (opcional): Combinar dos patrones con operador AND

4. **Detectar variables:**
   - Click en "🔍 Detectar Variables"
   - El sistema encontrará todas las variables únicas
   - **Prioridad**: Variables con "de" (fecha) se detectan primero

5. **Configurar variables:**
   - **Pestaña Configuración**:
     - Seleccionar tipo de dato (texto, número, fecha, lista, moneda, etc.)
     - Definir pregunta personalizada
     - Para listas: agregar opciones
     - Para moneda: seleccionar divisa (EUR/USD)
     - Para teléfono: seleccionar prefijo internacional
   - **Pestaña Dividir Variable**:
     - Por delimitador (/, |, etc.)
     - Por selección libre (índices)
     - Por contexto (ubicaciones específicas)
   - **Pestaña Contexto**:
     - Ver todas las apariciones de la variable
     - Identificar ubicaciones en el documento

6. **Operaciones adicionales:**
   - **Fusionar variables**: Combinar múltiples variables en una
   - **Desactivar variables**: Marcar variables para ignorarlas

7. **Generar archivos:**
   - Dar nombre a la plantilla
   - Click en "🚀 Generar"
   - Descargar:
     - Plantilla normalizada (.docx/.pptx)
     - Configuración YAML (.yaml)

### Fase 2: Generar Informe

1. **Iniciar la aplicación:**
   ```bash
   streamlit run F2Generador.py
   ```

2. **Subir archivos:**
   - Plantilla (.docx o .pptx)
   - Configuración YAML (.yaml)

3. **Rellenar formulario:**
   - Completar los datos solicitados
   - Los campos se adaptan al tipo de variable:
     - Fechas: selector de calendario
     - Horas: selector de hora
     - Listas: menú desplegable
     - Moneda: campo numérico + selector de divisa
     - Teléfono: selector de prefijo + número
     - Otros: campo de texto

4. **Opciones:**
   - Habilitar validación (recomendado)
   - Personalizar nombre del informe

5. **Generar:**
   - Click en "🚀 Generar Informe"
   - Si hay errores de validación, corregirlos
   - Descargar informe final

## 🗂️ Estructura del Proyecto

```
Plantilla2fase/
│
├── F1Plantilla.py              # Aplicación Fase 1 (Generador de Plantillas)
├── F2Generador.py              # Aplicación Fase 2 (Generador de Informes)
├── utils_v2.py                 # Librería común con clases compartidas
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Esta documentación
```

## 🔧 Arquitectura del Código

### utils_v2.py - Clases Compartidas

**PatternDetector**: Detecta patrones de variables en documentos
- `detect_colors_in_docx()` / `detect_colors_in_pptx()`: Detecta colores usados
- `extract_variables_by_pattern()`: Extrae variables según patrón regex
- `extract_variables_by_color()`: Extrae variables por color de texto/subrayado
- `detect_date_with_de_patterns()`: Detecta fechas con "de" (día de mes de año)
- `extract_variable_context()`: Extrae contexto de variables en el documento
- `is_substring_of_any()`: Previene detección de variables duplicadas

**VariableNormalizer**: Normaliza nombres de variables
- `normalize_name()`: Convierte texto a nombre de variable válido
- `generate_default_question()`: Genera pregunta por defecto según tipo

**YAMLManager**: Gestiona archivos de configuración
- `create_variable_config()`: Crea estructura YAML con metadatos
- `save_yaml()` / `load_yaml()`: Guardar/cargar configuración

**DocumentProcessor**: Procesa documentos Word y PowerPoint
- `replace_in_docx()` / `replace_in_pptx()`: Reemplaza variables en documentos
- Mantiene formato original durante el reemplazo

**Validator**: Valida datos según tipo
- `validate_email()`: Valida formato de email
- `validate_phone()`: Valida formato de teléfono
- `validate_date()`: Valida formato de fecha DD/MM/YYYY
- `validate_time()`: Valida formato de hora HH:MM
- `validate_number()`: Valida números

### F1Plantilla.py - Funciones Específicas

- `sanitize_placeholders()`: Limpia artefactos y normaliza placeholders
- `hex_to_color_name()`: Convierte códigos hex a nombres de colores legibles
- `clean_pattern_markers()`: Elimina marcadores de patrones
- `infer_variable_type()`: Infiere tipo de variable según contenido
- `merge_variables()`: Fusiona múltiples variables en una
- `split_variable()`: Divide variable por delimitador
- `split_variable_free()`: División libre por índices
- `split_variable_by_context()`: División selectiva por contextos
- `toggle_variable_enabled()`: Activa/desactiva variables
- `detect_combined_pattern_variables()`: Detecta con patrón combinado AND
- `create_template_docx()` / `create_template_pptx()`: Crea plantillas normalizadas

### F2Generador.py - Funciones Específicas

- `build_variables_map()`: Convierte lista de variables YAML a diccionario
- `currency_default()`: Obtiene moneda por defecto de metadatos
- `phone_prefix_default()`: Obtiene prefijo telefónico por defecto
- `phone_prefix_catalog()`: Catálogo de prefijos internacionales
- `format_currency_es()`: Formatea moneda según convención española

## 🆕 Nuevas Funcionalidades en v2.0

### Patrón Combinado (AND)
Detecta variables que cumplan **AMBOS** patrones simultáneamente.

**Ejemplo**: Variables que sean `{texto}` **Y** tengan color rojo

### Desactivar Variables
Permite marcar variables como desactivadas sin eliminarlas.
- Las variables desactivadas no aparecen en el YAML
- Pueden reactivarse en cualquier momento

### Contexto de Variables
Muestra todas las ubicaciones donde aparece una variable en el documento.
- Ver texto antes y después de cada aparición
- Identificar ubicación exacta (párrafo, tabla, slide, etc.)
- Estadísticas de apariciones

### División de Variables

**Por Delimitador:**
```
"día/mes/año" → "día", "mes", "año"
```

**Por Selección Libre:**
Seleccionar porción específica del texto usando índices.

**Por Contexto:**
Crear nueva variable con solo ciertos contextos seleccionados.
- Variable original mantiene contextos restantes
- Útil cuando misma variable tiene significados diferentes según ubicación

### Fechas con "de"
Detección prioritaria de patrones como:
- "día de mes de año" (PRIORIDAD 1)
- "día de mes" (PRIORIDAD 2)
- "mes de año" (PRIORIDAD 3)

Evita detectar subconjuntos cuando hay patrón más completo.

### Prevención de Duplicados
El sistema automáticamente previene detectar variables que ya están dentro de otras variables detectadas.

## 📋 Ejemplos de Uso

### Ejemplo 1: Contrato Legal

**Documento original:**
```
Contrato de [TIPO_CONTRATO] entre {{nombre_cliente}} y la empresa.
Fecha de inicio: {fecha_inicio}
Monto: {{importe_total}}
```

**Variables detectadas:**
- `tipo_contrato` → Tipo: Lista (Arrendamiento, Compraventa, Servicios)
- `nombre_cliente` → Tipo: Texto
- `fecha_inicio` → Tipo: Fecha
- `importe_total` → Tipo: Moneda (EUR)

### Ejemplo 2: Informe con Colores

**Documento con texto en rojo:**
```
Cliente: NOMBRE_EMPRESA (en rojo)
Responsable: NOMBRE_RESPONSABLE (en rojo)
```

**Configuración:**
- Seleccionar "Color de texto: #FF0000 🔴 Rojo"
- Variables detectadas automáticamente con agrupación de runs consecutivos

### Ejemplo 3: Patrón Combinado

**Documento con variables:**
```
{dato_importante} en azul
{dato_normal} en negro
```

**Configuración:**
- Patrón 1: Formato {variable}
- Patrón 2: Color de texto azul
- Solo detectará: `dato_importante`

### Ejemplo 4: División por Contexto

**Variable `fecha` aparece 5 veces:**
- 3 veces como "fecha de inicio"
- 2 veces como "fecha de cierre"

**Solución:**
1. Seleccionar los 2 contextos de "fecha de cierre"
2. Crear nueva variable `fecha_cierre`
3. Variable original `fecha` queda con 3 contextos de "fecha de inicio"

## 🔒 Seguridad y Privacidad

- ✅ Procesamiento **100% local** (sin envío a internet)
- ✅ Sin almacenamiento permanente de datos
- ✅ Archivos temporales eliminados automáticamente
- ✅ Control total del usuario sobre los datos

## 🐛 Solución de Problemas

### No se detectan variables
- Verificar que los patrones seleccionados coincidan con el documento
- Revisar que las variables no tengan espacios extra
- Probar con otro patrón de detección

### Variables no se reemplazan
- Verificar que el nombre en YAML coincida exactamente
- Revisar espacios en formato `{{variable}}`
- Asegurar que la plantilla es la generada por Fase 1

### Error de formato de documento
- Usar archivos .docx/.pptx recientes (no .doc/.ppt)
- Abrir y guardar con Office/LibreOffice actualizado

### Validación falla
- Email: Verificar formato usuario@dominio.com
- Teléfono: Incluir prefijo internacional
- Fecha: Usar formato DD/MM/YYYY
- Hora: Usar formato HH:MM

## 📊 Rendimiento

- **Documentos Word**: Óptimo hasta 20 páginas
- **Presentaciones PowerPoint**: Óptimo hasta 50 slides
- **Variables por documento**: Sin límite práctico
- **Patrones simultáneos**: Hasta 6 recomendado
- **Ahorro de tiempo**: 80-90% vs proceso manual

## 🔄 Flujo de Trabajo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    FASE 1: PLANTILLAS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Documento Original (Word/PPT)                           │
│           ↓                                                  │
│  2. Detectar Patrones (colores, llaves, combinados, etc.)  │
│           ↓                                                  │
│  3. Configurar Variables (tipos, preguntas, divisiones)     │
│           ↓                                                  │
│  4. Exportar:                                               │
│     • Plantilla normalizada (.docx/.pptx)                  │
│     • Config YAML (.yaml)                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    FASE 2: INFORMES                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Cargar Plantilla + Config YAML                          │
│           ↓                                                  │
│  2. Formulario Dinámico (adaptado a tipos)                  │
│           ↓                                                  │
│  3. Validar Datos (opcional pero recomendado)               │
│           ↓                                                  │
│  4. Generar Informe Final                                   │
│     • Diseño original preservado 100%                       │
│     • Variables reemplazadas correctamente                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🎓 Mejores Prácticas

1. **Organización de patrones**: Usa patrones diferentes para tipos diferentes de variables
2. **Validación siempre activa**: Especialmente para emails y teléfonos
3. **Revisar contexto**: Antes de dividir variables, visualiza dónde aparecen
4. **Backup de plantillas**: Guarda las plantillas y YAML generados
5. **Nombres descriptivos**: Usa nombres de variables claros y consistentes
6. **División inteligente**: Usa división por contexto para casos complejos

## 📞 Soporte

Para problemas o dudas:
1. Consultar esta documentación
2. Revisar mensajes de error en la interfaz
3. Verificar logs de Streamlit en la consola

## 🚀 Roadmap Futuro

- [ ] Soporte para Excel (.xlsx)
- [ ] Plantillas predefinidas comunes
- [ ] Exportación a PDF
- [ ] Multi-usuario con autenticación
- [ ] Historial de informes generados
- [ ] Integración con bases de datos

## 📄 Información del Proyecto

**Versión**: 2.0 Final
**Estado**: ✅ Producción
**Fecha**: Noviembre 2025
**Tecnologías**: Python, Streamlit, python-docx, python-pptx, PyYAML

---

**¡Sistema listo para uso en producción!** 🎉
