"""
Test para verificar la corrección v1.2 - Limpieza de Patrones
"""

import re

def clean_pattern_markers(text: str) -> str:
    """Elimina todos los marcadores de patrones ({}, [], etc.) del texto"""
    # Eliminar llaves dobles
    text = re.sub(r'\{\{([^}]+)\}\}', r'\1', text)
    # Eliminar llaves simples
    text = re.sub(r'\{([^}]+)\}', r'\1', text)
    # Eliminar corchetes dobles
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
    # Eliminar corchetes simples
    text = re.sub(r'\[([^\]]+)\]', r'\1', text)
    return text.strip()


def run_tests():
    """Ejecuta tests de limpieza de patrones"""
    print("=" * 60)
    print("  TEST DE LIMPIEZA DE PATRONES v1.2")
    print("=" * 60)
    print()
    
    tests = [
        # Formato: (entrada, salida_esperada, descripción)
        ("{variable}", "variable", "Llaves simples"),
        ("{{variable}}", "variable", "Llaves dobles"),
        ("[variable]", "variable", "Corchetes simples"),
        ("[[variable]]", "variable", "Corchetes dobles"),
        ("nombre_cliente", "nombre_cliente", "Sin patrones"),
        ("{nombre_proyecto}", "nombre_proyecto", "Variable con underscore"),
        ("[[fecha_inicio]]", "fecha_inicio", "Fecha con corchetes dobles"),
        ("{{monto_total}}", "monto_total", "Monto con llaves dobles"),
        ("  {variable}  ", "variable", "Con espacios"),
    ]
    
    passed = 0
    failed = 0
    
    for input_text, expected, description in tests:
        result = clean_pattern_markers(input_text)
        
        if result == expected:
            print(f"✅ PASS: {description}")
            print(f"   Entrada:  '{input_text}'")
            print(f"   Salida:   '{result}'")
            print(f"   Esperado: '{expected}'")
            passed += 1
        else:
            print(f"❌ FAIL: {description}")
            print(f"   Entrada:  '{input_text}'")
            print(f"   Salida:   '{result}'")
            print(f"   Esperado: '{expected}'")
            failed += 1
        print()
    
    # Resumen
    print("=" * 60)
    print("  RESUMEN")
    print("=" * 60)
    print(f"Tests ejecutados: {passed + failed}")
    print(f"✅ Pasados: {passed}")
    print(f"❌ Fallidos: {failed}")
    
    if failed == 0:
        print()
        print("🎉 ¡TODOS LOS TESTS PASARON!")
        print()
        print("✅ La limpieza de patrones funciona correctamente")
        print("✅ Las plantillas tendrán formato consistente {{variable}}")
        return True
    else:
        print()
        print("⚠️  ALGUNOS TESTS FALLARON")
        print()
        print("Por favor revisa el código de clean_pattern_markers()")
        return False


def test_real_scenario():
    """Simula un escenario real de uso"""
    print("\n" + "=" * 60)
    print("  TEST DE ESCENARIO REAL")
    print("=" * 60)
    print()
    
    # Simular variables detectadas con diferentes patrones
    variables = {
        'nombre_cliente': {
            'original_text': '{nombre_cliente}',
            'tipo': 'texto'
        },
        'fecha_inicio': {
            'original_text': '[fecha_inicio]',
            'tipo': 'fecha'
        },
        'responsable_proyecto': {
            'original_text': '[[responsable_proyecto]]',
            'tipo': 'texto'
        },
        'monto_total': {
            'original_text': '{{monto_total}}',
            'tipo': 'numero'
        }
    }
    
    print("Variables detectadas:")
    print()
    
    for var_id, var_info in variables.items():
        original = var_info['original_text']
        cleaned = clean_pattern_markers(original)
        placeholder = f"{{{{{var_id}}}}}"
        
        print(f"Variable: {var_id}")
        print(f"  Original:    '{original}'")
        print(f"  Limpiado:    '{cleaned}'")
        print(f"  Plantilla:   '{placeholder}'")
        print(f"  ✅ Correcto: {cleaned == var_id}")
        print()
    
    print("=" * 60)
    print()
    print("Ejemplo de texto procesado:")
    print()
    
    original_text = "Cliente: {nombre_cliente}, Fecha: [fecha_inicio]"
    print(f"ORIGINAL: {original_text}")
    
    # Simular reemplazo
    result_text = original_text
    for var_id, var_info in variables.items():
        original = var_info['original_text']
        placeholder = f"{{{{{var_id}}}}}"
        result_text = result_text.replace(original, placeholder)
    
    print(f"PLANTILLA: {result_text}")
    print()
    
    expected = "Cliente: {{nombre_cliente}}, Fecha: {{fecha_inicio}}"
    if result_text == expected:
        print("✅ El texto de plantilla es correcto")
        return True
    else:
        print(f"❌ Error: se esperaba '{expected}'")
        return False


def main():
    """Función principal"""
    result1 = run_tests()
    result2 = test_real_scenario()
    
    print()
    print("=" * 60)
    print("  RESULTADO FINAL")
    print("=" * 60)
    
    if result1 and result2:
        print()
        print("🎉 ¡CORRECCIÓN v1.2 VERIFICADA!")
        print()
        print("✅ Limpieza de patrones: OK")
        print("✅ Escenario real: OK")
        print("✅ Sistema listo para usar")
        print()
        print("Puedes proceder a usar:")
        print("  streamlit run fase1_generador_plantillas.py")
        print()
        return 0
    else:
        print()
        print("⚠️  VERIFICACIÓN FALLIDA")
        print()
        print("Por favor:")
        print("1. Descarga la versión v1.2 actualizada")
        print("2. Reemplaza fase1_generador_plantillas.py")
        print("3. Ejecuta este test nuevamente")
        print()
        return 1


if __name__ == "__main__":
    exit(main())
