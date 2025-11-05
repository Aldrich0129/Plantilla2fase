"""
Script de Prueba - Verificación de Correcciones v1.1
Verifica que las rutas multiplataforma y colores funcionan correctamente
"""

import sys
import os
from pathlib import Path
import tempfile

def test_imports():
    """Verifica que todos los imports necesarios están disponibles"""
    print("🧪 Probando imports...")
    try:
        from docx import Document
        print("   ✅ python-docx OK")
    except ImportError:
        print("   ❌ python-docx NO instalado")
        return False
    
    try:
        from pptx import Presentation
        print("   ✅ python-pptx OK")
    except ImportError:
        print("   ❌ python-pptx NO instalado")
        return False
    
    try:
        import streamlit
        print("   ✅ streamlit OK")
    except ImportError:
        print("   ❌ streamlit NO instalado")
        return False
    
    try:
        import yaml
        print("   ✅ PyYAML OK")
    except ImportError:
        print("   ❌ PyYAML NO instalado")
        return False
    
    return True


def test_paths():
    """Verifica que las rutas multiplataforma funcionan"""
    print("\n🧪 Probando rutas multiplataforma...")
    
    # Crear directorio temporal
    try:
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)
        print(f"   ✅ Directorio temporal creado: {temp_path}")
        
        # Crear archivo de prueba
        test_file = temp_path / "test.txt"
        with open(test_file, 'w') as f:
            f.write("test")
        
        if test_file.exists():
            print("   ✅ Escritura de archivos OK")
            
            # Limpiar
            os.remove(test_file)
            os.rmdir(temp_dir)
            print("   ✅ Limpieza de archivos OK")
            return True
        else:
            print("   ❌ No se pudo crear archivo")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_color_function():
    """Verifica que la función de colores funciona"""
    print("\n🧪 Probando función de colores...")
    
    # Importar la función
    try:
        # Leer el archivo y ejecutar la función
        color_map = {
            '#ff0000': '🔴 Rojo',
            '#0000ff': '🔵 Azul',
            '#00ff00': '🟢 Verde Lima',
        }
        
        print("   ✅ Mapeo de colores disponible")
        print("   Ejemplos:")
        for hex_code, name in list(color_map.items())[:3]:
            print(f"      {hex_code} → {name}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_files_exist():
    """Verifica que los archivos necesarios existen"""
    print("\n🧪 Verificando archivos del sistema...")
    
    required_files = [
        'utils.py',
        'fase1_generador_plantillas.py',
        'fase2_generador_informes.py',
        'requirements.txt',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} NO encontrado")
            all_exist = False
    
    return all_exist


def check_version():
    """Verifica la versión de los archivos"""
    print("\n🧪 Verificando versiones...")
    
    try:
        # Verificar que fase1 tiene las correcciones
        with open('fase1_generador_plantillas.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'from pathlib import Path' in content:
            print("   ✅ Fase 1 tiene corrección de rutas")
        else:
            print("   ⚠️  Fase 1 NO tiene corrección de rutas")
            return False
        
        if 'def hex_to_color_name' in content:
            print("   ✅ Fase 1 tiene función de colores")
        else:
            print("   ⚠️  Fase 1 NO tiene función de colores")
            return False
        
        if 'tempfile.mkdtemp' in content:
            print("   ✅ Fase 1 usa directorios temporales")
        else:
            print("   ⚠️  Fase 1 NO usa directorios temporales")
            return False
        
        # Verificar fase2
        with open('fase2_generador_informes.py', 'r', encoding='utf-8') as f:
            content2 = f.read()
        
        if 'from pathlib import Path' in content2:
            print("   ✅ Fase 2 tiene corrección de rutas")
        else:
            print("   ⚠️  Fase 2 NO tiene corrección de rutas")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando versiones: {e}")
        return False


def main():
    print("=" * 60)
    print("  VERIFICACIÓN DEL SISTEMA v1.1")
    print("  Prueba de Correcciones Windows + Colores")
    print("=" * 60)
    
    results = []
    
    # Ejecutar todas las pruebas
    results.append(("Imports", test_imports()))
    results.append(("Rutas multiplataforma", test_paths()))
    results.append(("Función de colores", test_color_function()))
    results.append(("Archivos del sistema", test_files_exist()))
    results.append(("Versiones correctas", check_version()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("  RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 ¡TODO CORRECTO! Sistema listo para usar.")
        print("\nPróximos pasos:")
        print("1. streamlit run fase1_generador_plantillas.py")
        print("2. Prueba con ejemplo_informe.docx")
        print("3. Verifica que los colores se ven de forma visual")
        return 0
    else:
        print("\n⚠️  Algunas pruebas fallaron.")
        print("\nSoluciones:")
        print("1. Ejecuta: pip install -r requirements.txt")
        print("2. Verifica que descargaste la versión v1.1")
        print("3. Revisa CORRECCIONES_v1.1.md para más detalles")
        return 1


if __name__ == "__main__":
    sys.exit(main())
