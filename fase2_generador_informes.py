"""
FASE 2: Generador de Informes
Rellena plantillas con datos del usuario y genera documentos finales
VERSIÓN 2: Compatible con utils_v2.py
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
from docx import Document
from pptx import Presentation
from utils_v2 import YAMLManager, DocumentProcessor, Validator
import io
from datetime import datetime
# === Helpers nuevos ===
def build_variables_map(config: dict) -> dict:
    """
    Convierte config['variables'] (lista) en dict {var_id: var_config}.
    var_id = 'nombre' en el YAML.
    """
    variables = config.get('variables', [])
    if isinstance(variables, list):
        out = {}
        for item in variables:
            var_id = item.get('nombre')
            if not var_id:
                continue
            out[var_id] = item
        return out
    elif isinstance(variables, dict):
        # por si en el futuro ya viene como dict
        return variables
    else:
        return {}

def currency_default(var_config: dict) -> str:
    return (var_config.get('meta') or {}).get('currency', 'EUR')

def phone_prefix_default(var_config: dict) -> str:
    return (var_config.get('meta') or {}).get('country_code', '+34')

def phone_prefix_catalog():
    # catálogo básico ampliable
    return [
        ('España', '+34'),
        ('Francia', '+33'),
        ('Portugal', '+351'),
        ('Italia', '+39'),
        ('Alemania', '+49'),
        ('Reino Unido', '+44'),
        ('Estados Unidos', '+1'),
        ('México', '+52'),
        ('Argentina', '+54'),
        ('China', '+86'),
        ('Hong Kong', '+852'),
        ('Taiwán', '+886'),
    ]

def format_currency_es(amount_str: str, currency: str) -> str:
    """
    Formatea de forma simple según convención ES:
    - separador decimal coma
    - símbolo postfijo para EUR (€) / USD ($)
    """
    if not amount_str:
        return ""
    # normalizar: sustituir comas por puntos para convertir
    amt_clean = amount_str.strip().replace('.', '').replace(',', '.')
    try:
        val = float(amt_clean)
    except:
        # si no es número, devolver tal cual con la divisa
        return f"{amount_str} {'€' if currency=='EUR' else '$'}"
    # formateo con coma decimal y sin separador de miles (simple)
    entero, dec = f"{val:.2f}".split('.')
    shown = f"{entero},{dec}"
    return f"{shown} {'€' if currency=='EUR' else '$'}"


# Configuración de la página
st.set_page_config(
    page_title="Fase 2: Generador de Informes",
    page_icon="📊",
    layout="wide"
)

# Inicializar estado de sesión
if 'config' not in st.session_state:
    st.session_state.config = None
if 'template_doc' not in st.session_state:
    st.session_state.template_doc = None
if 'doc_type' not in st.session_state:
    st.session_state.doc_type = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'validation_errors' not in st.session_state:
    st.session_state.validation_errors = {}
if 'work_dir' not in st.session_state:
    # Crear directorio temporal para trabajar (multiplataforma)
    st.session_state.work_dir = tempfile.mkdtemp()


def main():
    st.title("📊 Fase 2: Generador de Informes")
    st.markdown("---")
    
    # Sidebar con instrucciones
    with st.sidebar:
        st.header("📖 Guía de Uso")
        st.markdown("""
        ### Pasos:
        1. **Subir** plantilla (.docx o .pptx)
        2. **Subir** configuración YAML
        3. **Rellenar** datos solicitados
        4. **Validar** información (opcional)
        5. **Generar** informe final
        
        ### Tipos de datos:
        - ✏️ Texto libre
        - 🔢 Números
        - 📅 Fechas (DD/MM/YYYY)
        - ⏰ Horas (HH:MM)
        - 📧 Emails
        - 📱 Teléfonos
        - 📋 Listas de opciones
        """)
    
    # Paso 1: Subir plantilla
    st.header("1️⃣ Subir Plantilla")
    
    col1, col2 = st.columns(2)
    
    with col1:
        template_file = st.file_uploader(
            "Plantilla (Word o PowerPoint):",
            type=['docx', 'pptx'],
            help="Plantilla generada en la Fase 1"
        )
    
    with col2:
        config_file = st.file_uploader(
            "Configuración YAML:",
            type=['yaml', 'yml'],
            help="Archivo de configuración generado en la Fase 1"
        )
    
    if template_file and config_file:
        # Cargar plantilla
        file_extension = template_file.name.split('.')[-1].lower()
        st.session_state.doc_type = file_extension
        
        file_bytes = template_file.read()
        
        if file_extension == 'docx':
            st.session_state.template_doc = Document(io.BytesIO(file_bytes))
        else:
            st.session_state.template_doc = Presentation(io.BytesIO(file_bytes))
        
        # Cargar configuración YAML
        config_bytes = config_file.read()
        config_text = config_bytes.decode('utf-8')
        
        # Guardar temporalmente para cargar con YAMLManager
        work_dir = Path(st.session_state.work_dir)
        work_dir.mkdir(exist_ok=True)
        temp_config_path = work_dir / "temp_config.yaml"
        
        with open(temp_config_path, 'w', encoding='utf-8') as f:
            f.write(config_text)
        
        st.session_state.config = YAMLManager.load_yaml(str(temp_config_path))
        
        st.success(f"✅ Plantilla y configuración cargadas correctamente")
        # 🔧 NUEVO: convertir la lista de variables del YAML a dict indexado por 'nombre'
        variables_map = build_variables_map(st.session_state.config)
        if not variables_map:
            st.error("No se encontraron variables válidas en el YAML (se esperaba 'variables: [ {nombre: ...}, ... ]').")
            return
        
        st.session_state.config['__variables_map__'] = variables_map  # guardamos para acceso fácil
        st.info(f"📋 Variables a rellenar: **{len(variables_map)}**")

        st.markdown("---")

        
    # Paso 2: Formulario de datos
    st.header("2️⃣ Rellenar Datos del Informe")

    variables_map = st.session_state.config.get('__variables_map__', {})
    if not variables_map:
        st.warning("⬆️ Sube plantilla y YAML válidos para continuar.")
        return

    with st.form("data_form"):
        st.markdown("### Ingrese los datos solicitados:")

        cols_per_row = 2
        var_items = list(variables_map.items())

        for i in range(0, len(var_items), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j >= len(var_items):
                    break
                var_id, var_config = var_items[i + j]
                with cols[j]:
                    pregunta = var_config.get('pregunta') or f"Ingrese {var_id.replace('_',' ')}:"
                    tipo = var_config.get('tipo', 'texto')

                    if tipo == 'texto':
                        value = st.text_input(pregunta, key=f"input_{var_id}", help=f"Variable: {var_id}")

                    elif tipo == 'numero':
                        value = st.text_input(pregunta, key=f"input_{var_id}",
                                            help=f"Variable: {var_id} | Ingrese solo números")

                    elif tipo == 'fecha':
                        fecha_value = st.date_input(pregunta, key=f"input_{var_id}", help=f"Variable: {var_id}")
                        value = fecha_value.strftime("%d/%m/%Y") if fecha_value else ""

                    elif tipo == 'hora':
                        hora_value = st.time_input(pregunta, key=f"input_{var_id}", help=f"Variable: {var_id}")
                        value = hora_value.strftime("%H:%M") if hora_value else ""

                    elif tipo == 'email':
                        value = st.text_input(pregunta, key=f"input_{var_id}",
                                            help=f"Variable: {var_id} | Ejemplo: usuario@ejemplo.com")

                    elif tipo == 'telefono':
                        pref_def = phone_prefix_default(var_config)
                        cat = phone_prefix_catalog()
                        def_idx = next((idx for idx, (_p, c) in enumerate(cat) if c == pref_def), 0)
                        sel_idx = st.selectbox("Prefijo", options=list(range(len(cat))),
                                            format_func=lambda i: f"{cat[i][0]} ({cat[i][1]})",
                                            index=def_idx, key=f"pref_{var_id}")
                        chosen_prefix = cat[sel_idx][1]
                        number = st.text_input(pregunta, key=f"input_{var_id}",
                                            help=f"Variable: {var_id} | Solo dígitos, sin prefijo")
                        value = f"{chosen_prefix} {number.strip()}"

                    elif tipo == 'lista':
                        opciones = var_config.get('opciones', [])
                        if opciones:
                            value = st.selectbox(pregunta, options=[''] + opciones,
                                                key=f"input_{var_id}", help=f"Variable: {var_id}")
                        else:
                            value = st.text_input(pregunta, key=f"input_{var_id}",
                                                help=f"Variable: {var_id} | Sin opciones definidas")

                    elif tipo == 'moneda':
                        curr = currency_default(var_config)
                        sel_curr = st.selectbox("Moneda", options=['EUR', 'USD'],
                                                index=['EUR','USD'].index(curr) if curr in ['EUR','USD'] else 0,
                                                key=f"curr_{var_id}")
                        amount = st.text_input(pregunta, key=f"input_{var_id}",
                                            help=f"Variable: {var_id} | Admite coma/punto")
                        value = format_currency_es(amount, sel_curr)

                    else:
                        value = st.text_input(pregunta, key=f"input_{var_id}", help=f"Variable: {var_id}")

                    st.session_state.user_data[var_id] = value

        # --- Opciones y Submit DENTRO del form ---
        st.markdown("---")
        st.markdown("### ⚙️ Opciones")
        col1, col2 = st.columns(2)
        with col1:
            habilitar_validacion = st.checkbox("Habilitar validación de datos", value=True,
                                            help="Valida formatos de email, teléfono, fechas, etc.")
        with col2:
            nombre_informe = st.text_input("Nombre del informe:",
                                        value=f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                                        help="Nombre del archivo final")

        submitted = st.form_submit_button("🚀 Generar Informe", type="primary")

    # === Manejo tras Submit (fuera del with st.form) ===
    if submitted:
        validation_errors = {}
        if habilitar_validacion:
            for var_id, value in st.session_state.user_data.items():
                if not value:
                    continue
                var_config = variables_map[var_id]
                tipo = var_config.get('tipo', 'texto')
                if tipo == 'email' and not Validator.validate_email(value):
                    validation_errors[var_id] = "Formato de email inválido"
                elif tipo == 'numero' and not Validator.validate_number(value):
                    validation_errors[var_id] = "Debe ser un número válido"
                elif tipo == 'telefono':
                    if not value.strip().startswith('+'):
                        validation_errors[var_id] = "El teléfono debe incluir prefijo internacional (+..)."
                    elif hasattr(Validator, 'validate_phone') and not Validator.validate_phone(value):
                        validation_errors[var_id] = "Formato de teléfono inválido"
                elif tipo == 'moneda':
                    raw = value.replace('€','').replace('$','').strip()
                    raw = raw.replace('.', '').replace(',', '.')
                    try:
                        float(raw)
                    except:
                        validation_errors[var_id] = "Cantidad de moneda inválida"

        st.session_state.validation_errors = validation_errors

        if validation_errors:
            st.error("❌ Errores de validación encontrados:")
            for var_id, error in validation_errors.items():
                st.warning(f"**{var_id}**: {error}")
        else:
            with st.spinner("Generando informe..."):
                try:
                    work_dir = Path(st.session_state.work_dir)
                    work_dir.mkdir(exist_ok=True)
                    file_extension = st.session_state.doc_type

                    if file_extension == 'docx':
                        final_doc = DocumentProcessor.replace_in_docx(
                            st.session_state.template_doc, st.session_state.user_data
                        )
                        output_path = work_dir / f"{nombre_informe}.docx"
                        final_doc.save(str(output_path))
                    else:
                        final_prs = DocumentProcessor.replace_in_pptx(
                            st.session_state.template_doc, st.session_state.user_data
                        )
                        output_path = work_dir / f"{nombre_informe}.pptx"
                        final_prs.save(str(output_path))

                    st.success("✅ ¡Informe generado correctamente!")
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label=f"📥 Descargar Informe (.{file_extension})",
                            data=f.read(),
                            file_name=f"{nombre_informe}.{file_extension}",
                            mime=("application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                if file_extension=='docx'
                                else "application/vnd.openxmlformats-officedocument.presentationml.presentation")
                        )

                    st.markdown("---")
                    st.markdown("### 📊 Resumen del Informe")
                    filled_vars = sum(1 for v in st.session_state.user_data.values() if v)
                    total_vars = len(st.session_state.user_data)
                    st.info(f"""
    - **Variables rellenadas:** {filled_vars} / {total_vars}
    - **Tipo de documento:** {file_extension.upper()}
    - **Validación:** {'✅ Activada' if habilitar_validacion else '⚠️ Desactivada'}
    - **Archivo generado:** {nombre_informe}.{file_extension}
    """)
                    with st.expander("👀 Ver datos ingresados"):
                        for var_id, value in st.session_state.user_data.items():
                            if value:
                                st.text(f"{var_id}: {value}")

                except Exception as e:
                    st.error(f"❌ Error al generar el informe: {str(e)}")
                    st.exception(e)

if __name__ == "__main__":
    main()
