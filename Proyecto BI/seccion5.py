import pandas as pd

# ==================== CARGA DE DATOS ====================
df = pd.read_excel('../data/RecopilaciónDeDatos-BI(respuestas).xlsx')

# ==================== LIMPIEZA DE NOMBRES ====================
df.columns = df.columns.str.strip().str.replace('\u200b', '', regex=True).str.replace('\n', '', regex=True)

# ==================== RENOMBRAR COLUMNAS ====================
renombrar = {
    # Filtros
    'Género': 'Genero',
    '¿Cuál es tu edad?': 'Edad',
    '¿En qué grado estás actualmente?': 'Grado',
    '¿En qué distrito vives?': 'Distrito',
    
    # Preguntas Sección 5
    '¿Qué tan difícil consideras cubrir los costos de matrícula y pensiones de estudios superiores?': 'Dificultad_Costos',
    '¿Qué tan importante sería contar con una beca para poder continuar tus estudios?': 'Importancia_Beca',
    '¿Qué tanto influye la distancia y transporte como barrera para estudiar en una institución superior?': 'Influencia_Distancia',
    '¿En qué medida consideras que el apoyo económico de tu familia es suficiente para tus estudios futuros?': 'Apoyo_Familiar',
    '¿Actualmente cuentas con computadora y conexión a internet en tu hogar?': 'Recursos_Tecnologicos'
}
df.rename(columns=renombrar, inplace=True)

# ==================== FILTROS OPCIONALES ====================
FILTROS = {
    # 'Genero': 'Masculino',
    # 'Grado': '5°',
    # 'Distrito': 'San Vicente'
}

# ==================== FUNCIONES ====================
def aplicar_filtros(df, filtros):
    """Aplica los filtros definidos al dataframe"""
    df_filtrado = df.copy()
    for col, val in filtros.items():
        if col in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado[col] == val]
    return df_filtrado

def analizar_pregunta(df, columna, categorias, titulo):
    """Muestra conteos y porcentajes totales de una pregunta"""
    print(f"\n{titulo}")
    print("-" * 60)

    if columna not in df.columns:
        print("Columna no encontrada.")
        return

    conteo = df[columna].value_counts().reindex(categorias, fill_value=0)
    total = conteo.sum()

    print(f"{'Categoría':<40} {'N° de respuestas':<18} {'Porcentaje'}")
    print("-" * 70)

    for cat in categorias:
        valor = conteo[cat]
        pct = (valor / total * 100) if total > 0 else 0
        print(f"{cat:<40} {valor:<18} {pct:>6.1f}%")

    print(f"\nTotal de respuestas: {total}")

# ==================== APLICAR FILTROS ====================
df_filtrado = aplicar_filtros(df, FILTROS)
df_analisis = df_filtrado if not df_filtrado.empty else df

print("\n" + "=" * 60)
print("SECCIÓN 5: BARRERAS Y APOYO")
print(f"Total registros: {len(df_analisis)}")
print("=" * 60)

# ==================== PREGUNTA 1 ====================
analizar_pregunta(df_analisis, 'Dificultad_Costos',
    ['Nada difícil', 'Poco difícil', 'Medianamente difícil', 'Difícil', 'Muy difícil'],
    "1. Dificultad para cubrir costos")

# ==================== PREGUNTA 2 ====================
analizar_pregunta(df_analisis, 'Importancia_Beca',
    ['Nada importante', 'Poco importante', 'Medianamente importante', 'Importante', 'Muy importante'],
    "2. Importancia de contar con beca")

# ==================== PREGUNTA 3 ====================
analizar_pregunta(df_analisis, 'Influencia_Distancia',
    ['Nada', 'Poco', 'Medianamente', 'Mucho', 'Demasiado'],
    "3. Influencia de la distancia y transporte")

# ==================== PREGUNTA 4 ====================
analizar_pregunta(df_analisis, 'Apoyo_Familiar',
    ['Nada suficiente', 'Poco suficiente', 'Medianamente suficiente', 'Suficiente', 'Muy suficiente'],
    "4. Suficiencia del apoyo familiar")

# ==================== PREGUNTA 5 ====================
analizar_pregunta(df_analisis, 'Recursos_Tecnologicos',
    ['Sí, cuento con ambos (computadora e internet)', 'Solo computadora', 'Solo internet', 'No cuento con ninguno'],
    "5. Acceso a recursos tecnológicos")

print("\n" + "=" * 60)
print("ANÁLISIS COMPLETADO")
print("=" * 60)
