# 🚀 GUÍA RÁPIDA DE INICIO

## ⚡ Inicio Rápido en 5 Minutos

### 1️⃣ Probar con Documento de Ejemplo

Ya incluimos un documento de ejemplo listo para usar: `ejemplo_informe.docx`

**Paso a paso:**

```bash
# 1. Iniciar Fase 1
streamlit run fase1_generador_plantillas.py

# 2. En el navegador que se abre:
#    - Subir: ejemplo_informe.docx
#    - Seleccionar patrones:
#      ✅ {variable} - llaves_simples
#      ✅ {{variable}} - llaves_dobles  
#      ✅ [variable] - corchetes_simples
#      ✅ [[variable]] - corchetes_dobles
#      ✅ Colores: #ff0000 (rojo), #0000ff (azul), #008000 (verde), #800080 (morado)
#    
#    - Click "Detectar Variables"
#    - Revisar las 10 variables encontradas
#    - Click "Generar Plantilla y YAML"
#    - Descargar ambos archivos

# 3. Cerrar Fase 1 (Ctrl+C en terminal)

# 4. Iniciar Fase 2
streamlit run fase2_generador_informes.py

# 5. En el navegador:
#    - Subir la plantilla .docx generada
#    - Subir el archivo .yaml generado
#    - Rellenar el formulario con tus datos
#    - Click "Generar Informe"
#    - Descargar informe final
```

## 📝 Variables del Ejemplo

El documento de ejemplo incluye estas variables:

| Variable | Tipo | Patrón |
|----------|------|--------|
| nombre_proyecto | Texto | `{variable}` |
| nombre_cliente | Texto | `{{variable}}` + Color rojo |
| fecha_inicio | Fecha | `[variable]` |
| responsable_proyecto | Texto | `[[variable]]` |
| email_contacto | Email | `{variable}` + Color azul |
| telefono_contacto | Teléfono | `{{variable}}` |
| presupuesto_total | Número | `{variable}` |
| fecha_pago | Fecha | `{{variable}}` |
| estado_proyecto | Lista | `[variable]` + Color verde |
| descripcion_proyecto | Texto | `{{variable}}` + Color morado |
| fecha_generacion | Fecha | `[variable]` |

## 🎯 Consejos para Tu Primer Uso

### ✅ Hacer:
- Empieza con un documento simple (5-10 variables)
- Usa un solo patrón la primera vez
- Prueba la validación con emails y teléfonos
- Revisa el YAML generado para entender la estructura

### ❌ Evitar:
- No uses más de 3-4 patrones diferentes al inicio
- No combines patrones muy similares
- No uses espacios dentro de `{variable }`

## 🔧 Estructura de Archivos Generados

```
/
├── ejemplo_informe.docx           # Documento original con variables
│
Después de Fase 1:
├── plantilla_ejemplo_informe.docx # Plantilla normalizada
├── plantilla_ejemplo_informe_config.yaml # Configuración
│
Después de Fase 2:
└── informe_20251022_143000.docx  # Informe final generado
```

## 💡 Ejemplos de Patrones Reales

### Caso 1: Contrato Legal
```
Documento original:
"El ARRENDATARIO [nombre_completo] con DNI {dni_arrendatario}"

Patrones a seleccionar:
✅ [variable] - corchetes_simples
✅ {variable} - llaves_simples
```

### Caso 2: Informe Médico
```
Documento original:
Paciente: NOMBRE_PACIENTE (en rojo)
Fecha consulta: FECHA_CONSULTA (en azul)

Patrones a seleccionar:
✅ Color de texto: #FF0000 (rojo)
✅ Color de texto: #0000FF (azul)
```

### Caso 3: Presentación Comercial
```
Diapositiva con:
- Cliente: {{cliente}} (llaves dobles)
- Importe: {{importe}} (llaves dobles)
- Fecha: [fecha_presentacion] (corchetes)

Patrones a seleccionar:
✅ {{variable}} - llaves_dobles
✅ [variable] - corchetes_simples
```

## 🐛 Solución Rápida de Problemas

### "No se abren las apps"
```bash
# Verificar instalación de Streamlit
streamlit --version

# Si no está instalado:
pip install --break-system-packages streamlit
```

### "Error al detectar variables"
- Asegúrate de seleccionar AL MENOS un patrón
- Verifica que el documento tenga variables con ese patrón
- Prueba primero con el ejemplo incluido

### "Las variables no se reemplazan"
- Verifica que los nombres en el formulario coincidan con el YAML
- Revisa que no haya espacios extra: `{ variable }` ❌ vs `{variable}` ✅

## 📞 Comandos Útiles

```bash
# Ver archivos en el directorio
ls -lh

# Listar variables Python instaladas
pip list | grep -E "(streamlit|docx|pptx|yaml)"

# Detener aplicación Streamlit
Ctrl + C

# Limpiar cache de Streamlit
streamlit cache clear
```

## 🎓 Siguiente Nivel

Una vez domines el ejemplo, prueba:

1. **Crear tu propio documento** con variables
2. **Usar múltiples colores** para diferentes categorías
3. **Combinar varios patrones** en un mismo documento
4. **Agregar validación personalizada** en el YAML
5. **Usar listas de opciones** para campos predefinidos

## ⏱️ Tiempos Estimados

- **Primera instalación:** 5 minutos
- **Probar ejemplo completo:** 10 minutos
- **Crear tu primera plantilla:** 15-20 minutos
- **Generar primer informe:** 5 minutos

---

¿Listo para empezar? 🚀

```bash
streamlit run fase1_generador_plantillas.py
```
