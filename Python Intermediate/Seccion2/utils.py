"""
Utilidades comunes para los scripts de análisis
"""

import pandas as pd

def menu_filtro_grado(df):
    """
    Muestra un menú interactivo para seleccionar el filtro de grado.
    Retorna el DataFrame filtrado según la selección del usuario.
    
    Args:
        df: DataFrame con los datos
        
    Returns:
        DataFrame filtrado según la selección del usuario
    """
    col_grado = "  ¿En qué grado estás actualmente?   "
    
    # Verificar que la columna existe
    if col_grado not in df.columns:
        print("[ADVERTENCIA] No se encontró la columna de grado. Mostrando todos los datos.")
        return df
    
    # Contar estudiantes por grado
    conteo_4to = len(df[df[col_grado] == '4°'])
    conteo_5to = len(df[df[col_grado] == '5°'])
    
    print("\n" + "=" * 80)
    print("FILTRO POR GRADO")
    print("=" * 80)
    print(f"Total de estudiantes: {len(df)}")
    print(f"  - 4to año: {conteo_4to} estudiantes")
    print(f"  - 5to año: {conteo_5to} estudiantes")
    print("\nSelecciona una opción:")
    print("  1. Solo 4to año")
    print("  2. Solo 5to año")
    print("  3. Ambos grados (todos)")
    print("=" * 80)
    
    while True:
        try:
            opcion = input("\nIngresa tu opción (1, 2 o 3): ").strip()
            
            if opcion == '1':
                df_filtrado = df[df[col_grado] == '4°'].copy()
                print(f"\n[OK] Filtrando solo estudiantes de 4to año ({len(df_filtrado)} estudiantes)")
                return df_filtrado
            elif opcion == '2':
                df_filtrado = df[df[col_grado] == '5°'].copy()
                print(f"\n[OK] Filtrando solo estudiantes de 5to año ({len(df_filtrado)} estudiantes)")
                return df_filtrado
            elif opcion == '3':
                print(f"\n[OK] Mostrando todos los estudiantes ({len(df)} estudiantes)")
                return df
            else:
                print("[ERROR] Opción inválida. Por favor ingresa 1, 2 o 3.")
        except KeyboardInterrupt:
            print("\n\n[ADVERTENCIA] Operación cancelada. Mostrando todos los datos.")
            return df
        except Exception as e:
            print(f"[ERROR] Error al procesar la opción: {e}")
            print("Mostrando todos los datos por defecto.")
            return df

