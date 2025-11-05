# 📝 Sistema de Automatización de Plantillas

Sistema profesional de dos fases para automatizar la creación y generación de informes a partir de documentos Word y PowerPoint.

## 🎯 Características Principales

### ✨ Fase 1: Generador de Plantillas
- ✅ Importa archivos Word (.docx) y PowerPoint (.pptx)
- ✅ Detecta variables con múltiples patrones:
  - `{variable}` - Llaves simples
  - `{{variable}}` - Llaves dobles
  - `[variable]` - Corchetes simples
  - `[[variable]]` - Corchetes dobles
  - Color de texto específico
  - Color de subrayado (Word)
- ✅ Permite selección de múltiples patrones simultáneamente
- ✅ Identifica automáticamente todos los colores usados en el documento
- ✅ Normaliza variables y mantiene diseño original
- ✅ Genera configuración YAML con mapeo de preguntas
- ✅ Soporta variables en tablas, encabezados y pies de página

### ✨ Fase 2: Generador de Informes
- ✅ Carga plantillas con variables
- ✅ Lee configuración YAML para formularios dinámicos
- ✅ Tipos de datos soportados:
  - Texto libre
  - Números
  - Fechas (DD/MM/YYYY)
  - Horas (HH:MM)
  - Emails (con validación)
  - Teléfonos (con validación)
  - Listas de opciones predefinidas
- ✅ Validación opcional de datos
- ✅ Preserva diseño exacto del documento original
- ✅ Exporta informe final listo para usar

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Verificar instalación:**
```bash
streamlit --version
```

## 📖 Uso del Sistema

### Fase 1: Crear Plantilla

1. **Iniciar la aplicación:**
```bash
streamlit run fase1_generador_plantillas.py
```

2. **Subir documento:**
   - Click en "Browse files"
   - Seleccionar archivo Word (.docx) o PowerPoint (.pptx)
   - El documento debe tener variables marcadas

3. **Seleccionar patrones:**
   - **Patrones de texto:** Marcar los patrones que usas (llaves, corchetes, etc.)
   - **Patrones de color:** La app detectará automáticamente todos los colores
   - Puedes seleccionar múltiples patrones simultáneamente

4. **Detectar variables:**
   - Click en "🔍 Detectar Variables"
   - El sistema encontrará todas las variables únicas

5. **Configurar variables:**
   - Revisar cada variable detectada
   - Personalizar nombre si es necesario
   - Seleccionar tipo (texto, número, fecha, etc.)
   - Para tipo "lista": definir opciones
   - Agregar pregunta personalizada (opcional)

6. **Generar archivos:**
   - Dar nombre a la plantilla
   - Click en "🚀 Generar Plantilla y YAML"
   - Descargar ambos archivos:
     - `plantilla_[nombre].docx/pptx`
     - `plantilla_[nombre]_config.yaml`

### Fase 2: Generar Informe

1. **Iniciar la aplicación:**
```bash
streamlit run fase2_generador_informes.py
```

2. **Subir archivos:**
   - Subir la plantilla (.docx o .pptx)
   - Subir el archivo de configuración (.yaml)

3. **Rellenar datos:**
   - Completar el formulario con los datos solicitados
   - Cada campo se adapta al tipo de variable:
     - Fechas: selector de calendario
     - Horas: selector de hora
     - Listas: menú desplegable
     - Otros: campo de texto

4. **Opciones:**
   - ✅ Habilitar validación (recomendado)
   - Personalizar nombre del informe

5. **Generar:**
   - Click en "🚀 Generar Informe"
   - Si hay errores de validación, corregirlos
   - Descargar informe final

## 📋 Ejemplos de Uso

### Ejemplo 1: Informe Legal

**Documento original:**
```
Contrato de [TIPO_CONTRATO] entre {{nombre_cliente}} y la empresa.
Fecha de inicio: {fecha_inicio}
```

**Variables detectadas:**
- `tipo_contrato` → Tipo: Lista (opciones: Arrendamiento, Compraventa, Servicios)
- `nombre_cliente` → Tipo: Texto
- `fecha_inicio` → Tipo: Fecha

### Ejemplo 2: Presentación Comercial

**Slide original con texto en rojo:**
```
Cliente: NOMBRE_EMPRESA (en rojo)
Presupuesto: MONTO (en rojo)
```

**Configuración:**
- Seleccionar "Color de texto: #FF0000"
- Variables detectadas:
  - `nombre_empresa` → Tipo: Texto
  - `monto` → Tipo: Número

## 🔧 Características Avanzadas

### Múltiples Patrones Simultáneos
El sistema puede detectar varios patrones a la vez:
- Variables en `{llaves}` Y subrayadas en amarillo
- Variables en `[[corchetes]]` Y con texto rojo
- Variables con color Y en tablas

### Variables Repetidas
Si una variable aparece múltiples veces, se reemplazará en todas sus ocurrencias:
```
Cliente: {{nombre_cliente}}
...
Dirección de {{nombre_cliente}}: ...
```

### Validación de Datos
- **Email:** Verifica formato válido (usuario@dominio.com)
- **Teléfono:** Acepta múltiples formatos internacionales
- **Fecha:** Formato DD/MM/YYYY
- **Hora:** Formato HH:MM (24 horas)
- **Número:** Solo valores numéricos

### Preguntas Automáticas
Si no defines una pregunta personalizada, el sistema genera automáticamente:
- `fecha_inicio` → "Ingrese la fecha para fecha inicio (DD/MM/YYYY):"
- `email_contacto` → "Ingrese el email para email contacto:"
- `monto_total` → "Ingrese el número para monto total:"

## 📁 Estructura de Archivos

```
/
├── requirements.txt                    # Dependencias del proyecto
├── utils.py                           # Librería común de utilidades
├── fase1_generador_plantillas.py     # App Fase 1
├── fase2_generador_informes.py       # App Fase 2
└── README.md                          # Esta documentación
```

## 🔄 Flujo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    FASE 1: PLANTILLAS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Documento Original (Word/PPT)                           │
│           ↓                                                  │
│  2. Detectar Patrones (colores, llaves, etc.)              │
│           ↓                                                  │
│  3. Configurar Variables (tipos, preguntas)                 │
│           ↓                                                  │
│  4. Exportar:                                               │
│     • Plantilla normalizada                                 │
│     • Config YAML                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    FASE 2: INFORMES                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Cargar Plantilla + Config YAML                          │
│           ↓                                                  │
│  2. Formulario Dinámico                                     │
│           ↓                                                  │
│  3. Validar Datos (opcional)                                │
│           ↓                                                  │
│  4. Generar Informe Final                                   │
│     • Diseño original preservado                            │
│     • Variables reemplazadas                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## ⚡ Consejos de Rendimiento

### Documentos Grandes
- Word: Hasta 20 páginas funciona óptimamente
- PowerPoint: Hasta 50 slides funciona óptimamente
- Para documentos más grandes, considerar dividir en secciones

### Múltiples Patrones
- Usa patrones distintos para diferentes tipos de variables
- Ejemplo: `{datos_principales}` + texto_rojo para `datos_opcionales`

### Validación
- Actívala siempre para emails y teléfonos
- Puede desactivarse para agilizar pruebas

## 🐛 Solución de Problemas

### Error: "No se detectaron variables"
- Verifica que los patrones seleccionados coincidan con el documento
- Revisa que las variables no tengan espacios extra
- Intenta con otro patrón

### Error: "Formato de documento corrupto"
- Asegúrate de usar archivos .docx/.pptx recientes (no .doc/.ppt)
- Abre y guarda el documento con Office/LibreOffice actual

### Variables no se reemplazan
- Verifica que el nombre en YAML coincida exactamente
- Revisa que no haya espacios extra en el formato `{{variable}}`

## 🔒 Consideraciones de Seguridad

- Los archivos se procesan localmente
- No se envía información a servidores externos
- Los documentos temporales se eliminan al cerrar la app

## 📞 Soporte

Para dudas o problemas:
1. Revisar esta documentación
2. Verificar ejemplos incluidos
3. Comprobar logs de la aplicación Streamlit

## 🚀 Próximas Mejoras (Roadmap)

- [ ] Soporte para Excel (.xlsx)
- [ ] Integración con bases de datos
- [ ] API REST para automatización
- [ ] Multi-usuario con autenticación
- [ ] Plantillas compartidas
- [ ] Historial de informes generados

## 📄 Licencia

Sistema desarrollado para uso interno del despacho.

---

**Versión:** 1.0  
**Última actualización:** Octubre 2025
