#!/bin/bash
# Script de verificación e instalación del sistema
# Ejecutar: bash setup.sh

echo "=================================="
echo "  SISTEMA DE AUTOMATIZACIÓN DE   "
echo "         PLANTILLAS v1.0          "
echo "=================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# 1. Verificar Python
echo "1. Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python instalado: versión $PYTHON_VERSION"
else
    print_error "Python no encontrado. Por favor instala Python 3.8 o superior."
    exit 1
fi

echo ""

# 2. Verificar pip
echo "2. Verificando pip..."
if command -v pip &> /dev/null; then
    PIP_VERSION=$(pip --version | cut -d' ' -f2)
    print_success "pip instalado: versión $PIP_VERSION"
else
    print_error "pip no encontrado. Por favor instala pip."
    exit 1
fi

echo ""

# 3. Instalar dependencias
echo "3. Instalando dependencias..."
echo "   Esto puede tardar unos minutos..."

# Intentar instalación normal primero
pip install -r requirements.txt &> /dev/null

# Si falla, intentar con --break-system-packages
if [ $? -ne 0 ]; then
    print_warning "Instalación normal falló, intentando con --break-system-packages..."
    pip install --break-system-packages -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_success "Dependencias instaladas correctamente"
    else
        print_error "Error instalando dependencias. Revisa requirements.txt"
        exit 1
    fi
else
    print_success "Dependencias instaladas correctamente"
fi

echo ""

# 4. Verificar instalaciones
echo "4. Verificando instalaciones..."

# Streamlit
if python3 -c "import streamlit" &> /dev/null; then
    STREAMLIT_VERSION=$(python3 -c "import streamlit; print(streamlit.__version__)")
    print_success "Streamlit $STREAMLIT_VERSION"
else
    print_error "Streamlit no instalado correctamente"
fi

# python-docx
if python3 -c "from docx import Document" &> /dev/null; then
    print_success "python-docx"
else
    print_error "python-docx no instalado correctamente"
fi

# python-pptx
if python3 -c "from pptx import Presentation" &> /dev/null; then
    print_success "python-pptx"
else
    print_error "python-pptx no instalado correctamente"
fi

# PyYAML
if python3 -c "import yaml" &> /dev/null; then
    print_success "PyYAML"
else
    print_error "PyYAML no instalado correctamente"
fi

# Pillow
if python3 -c "from PIL import Image" &> /dev/null; then
    print_success "Pillow"
else
    print_warning "Pillow no instalado (opcional)"
fi

echo ""

# 5. Verificar archivos del sistema
echo "5. Verificando archivos del sistema..."

if [ -f "utils.py" ]; then
    print_success "utils.py"
else
    print_error "utils.py no encontrado"
fi

if [ -f "fase1_generador_plantillas.py" ]; then
    print_success "fase1_generador_plantillas.py"
else
    print_error "fase1_generador_plantillas.py no encontrado"
fi

if [ -f "fase2_generador_informes.py" ]; then
    print_success "fase2_generador_informes.py"
else
    print_error "fase2_generador_informes.py no encontrado"
fi

if [ -f "ejemplo_informe.docx" ]; then
    print_success "ejemplo_informe.docx"
else
    print_warning "ejemplo_informe.docx no encontrado (opcional)"
fi

echo ""

# 6. Crear directorios recomendados
echo "6. Creando estructura de directorios..."

mkdir -p plantillas
mkdir -p informes_generados
mkdir -p documentacion

print_success "Directorios creados: plantillas/, informes_generados/, documentacion/"

echo ""

# 7. Resumen
echo "=================================="
echo "       INSTALACIÓN COMPLETA       "
echo "=================================="
echo ""
echo "📚 Documentación disponible:"
echo "   • INDEX.md - Índice principal"
echo "   • INICIO_RAPIDO.md - Guía de 5 minutos"
echo "   • README.md - Documentación completa"
echo ""
echo "🚀 Para empezar:"
echo ""
echo "   Fase 1 (Crear plantillas):"
echo "   $ streamlit run fase1_generador_plantillas.py"
echo ""
echo "   Fase 2 (Generar informes):"
echo "   $ streamlit run fase2_generador_informes.py"
echo ""
echo "🎓 Prueba con el ejemplo incluido:"
echo "   ejemplo_informe.docx"
echo ""
echo "=================================="
print_success "¡Sistema listo para usar!"
echo "=================================="
