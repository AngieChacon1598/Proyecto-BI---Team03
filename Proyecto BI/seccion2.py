import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importar configuración de gráficos
from config_graficos import (
    configurar_estilo_global,
    COLORES_PROFESIONALES, COLORES_COMPARATIVO, COLORES_GRADOS,
    TAMANO_BARRAS, TAMANO_PASTEL, TAMANO_BARRAS_HORIZONTALES, 
    TAMANO_COMPARATIVO, TAMANO_DASHBOARD,
    COLOR_TEXTO, COLOR_BORDE, ALPHA_BARRAS, GROSOR_BORDE_BARRAS,
    TAMANO_TEXTO_BARRAS, TAMANO_TEXTO_PASTEL, TAMANO_LEYENDA,
    TAMANO_TITULO_SECUNDARIO, TAMANO_TITULO_DASHBOARD,
    aplicar_estilo_ejes, aplicar_grid, aplicar_titulo, aplicar_etiquetas
)

# Importar scipy solo si está disponible
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("ADVERTENCIA: Scipy no esta disponible. Las pruebas estadisticas avanzadas estaran limitadas.")

# Configurar estilo global de gráficos
configurar_estilo_global()

# Cargar datos del archivo correcto
archivo = '../data/RecopilaciónDeDatos-BI(respuestas).xlsx'
df = pd.read_excel(archivo)


# Mapeo de columnas según el archivo real
col_grado = '  ¿En qué grado estás actualmente?   '
col_genero = 'Género ' if 'Género ' in df.columns else None


total_estudiantes = len(df)
conteo_por_grado = df[col_grado].value_counts()
conteo_por_genero = df[col_genero].value_counts() if col_genero else None

print("\n============================")
print("METRICAS GENERALES")
print("============================")
print(f"Total de estudiantes encuestados: {total_estudiantes}\n")

print("Distribucion por grado:")
for grado, cant in conteo_por_grado.items():
    print(f"   - {grado} de secundaria: {cant}")

if conteo_por_genero is not None:
    print("\nDistribucion por genero:")
    for genero, cant in conteo_por_genero.items():
        print(f"   - {genero}: {cant}")

# --- GRÁFICOS DE DISTRIBUCIÓN PROFESIONALES ---
# Gráfico de barras por grado
fig, ax = plt.subplots(figsize=TAMANO_BARRAS)
bars = ax.bar(conteo_por_grado.index, conteo_por_grado.values, 
              color=COLORES_PROFESIONALES[:len(conteo_por_grado)], 
              edgecolor=COLOR_BORDE, linewidth=GROSOR_BORDE_BARRAS, alpha=ALPHA_BARRAS)

# Agregar valores en las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{int(height)}', ha='center', va='bottom', 
            fontweight='bold', fontsize=TAMANO_TEXTO_BARRAS, color=COLOR_TEXTO)

aplicar_titulo(ax, "Distribución de Estudiantes por Grado")
aplicar_etiquetas(ax, xlabel="Grado", ylabel="Número de Estudiantes")
aplicar_grid(ax, eje='y')
ax.set_ylim(0, max(conteo_por_grado.values) * 1.1)
aplicar_estilo_ejes(ax)

plt.tight_layout()
plt.show()

# Gráfico de pastel por género (si existe)
if conteo_por_genero is not None:
    fig, ax = plt.subplots(figsize=TAMANO_PASTEL)
    
    wedges, texts, autotexts = ax.pie(conteo_por_genero.values, 
                                     labels=conteo_por_genero.index,
                                     autopct='%1.1f%%',
                                     startangle=90,
                                     colors=COLORES_PROFESIONALES[:len(conteo_por_genero)],
                                     explode=[0.05] * len(conteo_por_genero),
                                     shadow=True,
                                     textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    # Personalizar el texto de porcentajes
    for autotext in autotexts:
        autotext.set_color(COLOR_TEXTO)
        autotext.set_fontweight('bold')
        autotext.set_fontsize(TAMANO_TEXTO_PASTEL)
    
    aplicar_titulo(ax, "Distribución por Género")
    ax.legend(wedges, [f'{label}: {value}' for label, value in zip(conteo_por_genero.index, conteo_por_genero.values)],
              title="Género", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=TAMANO_LEYENDA, title_fontsize=12)
    
    plt.tight_layout()
    plt.show()

# --- FUNCIONES DE ANÁLISIS ESTADÍSTICO ---
def calcular_metricas_estadisticas(df, pregunta, titulo):
    """Calcula métricas estadísticas para una pregunta"""
    if pregunta not in df.columns:
        return None
    
    respuestas = df[pregunta].dropna()
    if respuestas.empty:
        return None
    
    conteo = respuestas.value_counts()
    total_respuestas = len(respuestas)
    
    # Métricas básicas
    moda = conteo.index[0]  # Respuesta más frecuente
    frecuencia_moda = conteo.iloc[0]
    porcentaje_moda = (frecuencia_moda / total_respuestas) * 100
    
    # Diversidad de respuestas (entropía)
    probabilidades = conteo / total_respuestas
    entropia = -np.sum(probabilidades * np.log2(probabilidades + 1e-10))
    
    # Índice de diversidad (1 - concentración)
    concentracion = np.sum(probabilidades**2)
    diversidad = 1 - concentracion
    
    return {
        'titulo': titulo,
        'total_respuestas': total_respuestas,
        'moda': moda,
        'frecuencia_moda': frecuencia_moda,
        'porcentaje_moda': porcentaje_moda,
        'entropia': entropia,
        'diversidad': diversidad,
        'conteo': conteo
    }

def comparar_grados_estadisticamente(df, pregunta, titulo):
    """Compara estadísticamente las respuestas entre grados"""
    grados = df[col_grado].unique()
    if len(grados) < 2:
        return None
    
    # Crear tabla de contingencia
    tabla_contingencia = pd.crosstab(df[col_grado], df[pregunta])
    
    if SCIPY_AVAILABLE:
        # Prueba chi-cuadrado
        chi2, p_value, dof, expected = stats.chi2_contingency(tabla_contingencia)
        
        # Cramer's V (medida de asociación)
        n = tabla_contingencia.sum().sum()
        cramers_v = np.sqrt(chi2 / (n * (min(tabla_contingencia.shape) - 1)))
        
        return {
            'tabla_contingencia': tabla_contingencia,
            'chi2': chi2,
            'p_value': p_value,
            'cramers_v': cramers_v,
            'significativo': p_value < 0.05
        }
    else:
        # Análisis básico sin scipy
        n = tabla_contingencia.sum().sum()
        total_por_grado = tabla_contingencia.sum(axis=1)
        total_por_respuesta = tabla_contingencia.sum(axis=0)
        
        # Calcular diferencias porcentuales
        diferencias = {}
        for grado in grados:
            for respuesta in tabla_contingencia.columns:
                observado = tabla_contingencia.loc[grado, respuesta]
                esperado = (total_por_grado[grado] * total_por_respuesta[respuesta]) / n
                diferencia = abs(observado - esperado)
                diferencias[f"{grado}_{respuesta}"] = diferencia
        
        diferencia_promedio = np.mean(list(diferencias.values()))
        
        return {
            'tabla_contingencia': tabla_contingencia,
            'diferencia_promedio': diferencia_promedio,
            'analisis_basico': True
        }

# --- SELECCIÓN DE GRADO ---
grados_disponibles = sorted(df[col_grado].dropna().unique())

print("\n" + "="*50)
print("SELECCION DE GRADOS PARA ANALISIS")
print("="*50)
print("Grados disponibles:")
for i, grado in enumerate(grados_disponibles, 1):
    cantidad = len(df[df[col_grado] == grado])
    print(f"{i}. {grado} de secundaria ({cantidad} estudiantes)")

print(f"\nOpciones:")
print("1. Solo 4to de secundaria")
print("2. Solo 5to de secundaria") 
print("3. Ambos grados (comparativo)")
print("4. Todos los grados disponibles")

opcion = input("\nElige una opción (1-4): ").strip()

if opcion == "1":
    grados_filtrar = ["4°"]
elif opcion == "2":
    grados_filtrar = ["5°"]
elif opcion == "3":
    grados_filtrar = ["4°", "5°"]
elif opcion == "4":
    grados_filtrar = grados_disponibles
else:
    print("Opción no válida. Se usarán ambos grados (4to y 5to).")
    grados_filtrar = ["4°", "5°"]

df_filtrado = df[df[col_grado].isin(grados_filtrar)]
print(f"\nAnalizando datos para: {', '.join(grados_filtrar)}")
print(f"Total de estudiantes: {len(df_filtrado)}")

# --- PREGUNTAS DE LA SECCIÓN 2: PREFERENCIAS E INTERESES ---
preguntas_seccion2 = {
    '¿Cómo prefieres aprender cosas nuevas?': '📚 Estilos de aprendizaje preferidos',
    '¿Qué tan importante consideras la tecnología (computadoras, internet, apps) para tu educación futura?': '💻 Valoración de la tecnología en la educación',
    '¿Qué factor influye más en tu elección de carrera?': '🎯 Factores que influyen en la elección de carrera',
    '¿Qué tipo de estudios prefieres seguir después del colegio?': '🎓 Ruta educativa post-colegio',
    '¿Dónde te imaginas trabajando en el futuro?': '🌍 Aspiraciones laborales',
    '¿Te entusiasma diseñar programas, aplicaciones o inventos?': '⚡ Interés en programación e innovación'
}

# --- FUNCIONES DE GRAFICADO  ---
def graficar_barras(serie, titulo, horizontal=False):
    """Gráfico de barras profesional (horizontal o vertical)"""
    if serie.empty:
        print(f"No hay datos para: {titulo}")
        return
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 8) if not horizontal else TAMANO_BARRAS_HORIZONTALES)
    
    # Ordenar datos según orientación
    if horizontal:
        serie_ordenada = serie.sort_values(ascending=True)
    else:
        serie_ordenada = serie.sort_values(ascending=False)
    
    # Crear barras con gradiente de colores
    colors = plt.cm.viridis(np.linspace(0, 1, len(serie_ordenada)))
    
    if horizontal:
        # Gráfico horizontal
        bars = ax.barh(range(len(serie_ordenada)), serie_ordenada.values, 
                       color=colors, edgecolor=COLOR_BORDE, linewidth=1.2, alpha=ALPHA_BARRAS)
        
        # Agregar valores en las barras
        for i, (bar, value) in enumerate(zip(bars, serie_ordenada.values)):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{int(value)} ({value/serie_ordenada.sum()*100:.1f}%)',
                    ha='left', va='center', fontweight='bold', fontsize=11, color=COLOR_TEXTO)
        
        # Personalizar ejes
        ax.set_yticks(range(len(serie_ordenada)))
        ax.set_yticklabels(serie_ordenada.index, fontsize=11)
        aplicar_etiquetas(ax, xlabel='Número de Respuestas')
        aplicar_titulo(ax, titulo)
        aplicar_grid(ax, eje='x')
        aplicar_estilo_ejes(ax)
        
        # Ajustar límites
        ax.set_xlim(0, max(serie_ordenada.values) * 1.15)
    else:
        # Gráfico vertical
        bars = ax.bar(range(len(serie_ordenada)), serie_ordenada.values, 
                       color=colors, edgecolor=COLOR_BORDE, linewidth=1.2, alpha=ALPHA_BARRAS)
        
        # Agregar valores en las barras
        for i, (bar, value) in enumerate(zip(bars, serie_ordenada.values)):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                    f'{int(value)} ({value/serie_ordenada.sum()*100:.1f}%)',
                    ha='center', va='bottom', fontweight='bold', fontsize=11, color=COLOR_TEXTO)
        
        # Personalizar ejes
        ax.set_xticks(range(len(serie_ordenada)))
        ax.set_xticklabels(serie_ordenada.index, fontsize=11, rotation=45, ha='right')
        aplicar_etiquetas(ax, xlabel='Respuestas', ylabel='Número de Estudiantes')
        aplicar_titulo(ax, titulo)
        aplicar_grid(ax, eje='y')
        aplicar_estilo_ejes(ax)
        
        # Ajustar límites
        ax.set_ylim(0, max(serie_ordenada.values) * 1.15)
    
    plt.tight_layout()
    plt.show()


def graficar_comparativo(df, pregunta, titulo, grados):
    """Gráfico comparativo profesional"""
    datos = {}
    for grado in grados:
        respuestas = df[df[col_grado] == grado][pregunta].value_counts()
        if not respuestas.empty:
            datos[grado] = respuestas

    if not datos:
        print(f"No hay respuestas para comparación en: {titulo}")
        return

    comparativo = pd.DataFrame(datos).fillna(0).astype(int)
    n_respuestas = len(comparativo)

    # Crear figura con un solo gráfico
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Gráfico de barras agrupadas
    x = np.arange(len(comparativo.index))
    width = 0.35
    
    for i, (grado, color) in enumerate(zip(comparativo.columns, COLORES_COMPARATIVO[:len(comparativo.columns)])):
        bars = ax.bar(x + i*width, comparativo[grado], width, 
                      label=f'{grado} de secundaria', color=color, 
                      edgecolor=COLOR_BORDE, linewidth=1, alpha=ALPHA_BARRAS)
        
        # Agregar valores en las barras
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{int(height)}', ha='center', va='bottom', 
                        fontweight='bold', fontsize=10, color=COLOR_TEXTO)

    aplicar_etiquetas(ax, xlabel='Respuestas', ylabel='Número de Estudiantes')
    aplicar_titulo(ax, f'{titulo}\nComparativo por Grado', tamano=TAMANO_TITULO_SECUNDARIO)
    ax.set_xticks(x + width/2)
    ax.set_xticklabels(comparativo.index, rotation=45, ha='right', fontsize=10)
    ax.legend(fontsize=TAMANO_LEYENDA, frameon=True, fancybox=True, shadow=True)
    aplicar_grid(ax, eje='y')
    aplicar_estilo_ejes(ax)

    plt.tight_layout()
    plt.show()

# --- ANÁLISIS DE LA SECCIÓN 2: PREFERENCIAS E INTERESES ---
print("\n" + "="*60)
print("ANALISIS DE LA SECCION 2: PREFERENCIAS E INTERESES")
print("="*60)

# Almacenar métricas para resumen final
metricas_totales = []

for pregunta, titulo in preguntas_seccion2.items():
    if pregunta not in df_filtrado.columns:
        print(f"ADVERTENCIA: La pregunta '{pregunta}' no se encontro en el archivo.")
        continue

    print(f"\n{'='*50}")
    print(f"{titulo}")
    print(f"{'='*50}")
    
    # Calcular métricas estadísticas
    metricas = calcular_metricas_estadisticas(df_filtrado, pregunta, titulo)
    if metricas:
        metricas_totales.append(metricas)
        
        # Mostrar métricas
        print(f"METRICAS ESTADISTICAS:")
        print(f"   - Total de respuestas: {metricas['total_respuestas']}")
        print(f"   - Respuesta mas frecuente: {metricas['moda']} ({metricas['porcentaje_moda']:.1f}%)")
        print(f"   - Diversidad de respuestas: {metricas['diversidad']:.3f} (0=concentrado, 1=diverso)")
        print(f"   - Entropia: {metricas['entropia']:.3f} bits")
        
        # Mostrar distribución
        print(f"\nDISTRIBUCION DE RESPUESTAS:")
        for respuesta, cantidad in metricas['conteo'].items():
            porcentaje = (cantidad / metricas['total_respuestas']) * 100
            print(f"   - {respuesta}: {cantidad} ({porcentaje:.1f}%)")
        

# --- RESUMEN FINAL ---
# Solo mostrar el resumen una vez al final
if metricas_totales:
    print(f"\n{'='*60}")
    print("RESUMEN EJECUTIVO - SECCION 2")
    print(f"{'='*60}")
    
    print(f"Total de preguntas analizadas: {len(metricas_totales)}")
    print(f"Total de estudiantes: {len(df_filtrado)}")
    print(f"Grados analizados: {', '.join(grados_filtrar)}")
    
    # Encontrar preguntas con mayor y menor diversidad
    diversidades = [(m['titulo'], m['diversidad']) for m in metricas_totales]
    diversidades.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nINSIGHTS PRINCIPALES:")
    print(f"   - Mayor diversidad de opiniones: {diversidades[0][0]} ({diversidades[0][1]:.3f})")
    print(f"   - Menor diversidad de opiniones: {diversidades[-1][0]} ({diversidades[-1][1]:.3f})")
    
    # Mostrar respuestas más frecuentes
    print(f"\nRESPUESTAS MAS FRECUENTES:")
    for metrica in metricas_totales:
        print(f"   - {metrica['titulo']}: {metrica['moda']} ({metrica['porcentaje_moda']:.1f}%)")

# --- GENERAR TODOS LOS GRÁFICOS AL FINAL ---
print(f"\n{'='*60}")
print("GENERANDO GRAFICOS VISUALES...")
print(f"{'='*60}")

if metricas_totales:
    print("Generando graficos individuales de cada pregunta...")
    
    # Generar gráficos individuales (alternando entre vertical y horizontal)
    for i, metrica in enumerate(metricas_totales):
        # Alternar: pares = vertical, impares = horizontal
        es_horizontal = i % 2 == 1
        orientacion = "horizontal" if es_horizontal else "vertical"
        print(f"  - Grafico {orientacion}: {metrica['titulo']}")
        graficar_barras(metrica['conteo'], metrica['titulo'], horizontal=es_horizontal)
    
    # Generar gráficos comparativos si hay múltiples grados
    if len(grados_filtrar) >= 2:
        print("\nGenerando graficos comparativos entre grados...")
        for pregunta, titulo in preguntas_seccion2.items():
            if pregunta in df_filtrado.columns:
                print(f"  - Comparativo: {titulo}")
                graficar_comparativo(df_filtrado, pregunta, titulo, grados_filtrar)

print(f"\n{'='*60}")
print("ANALISIS COMPLETADO EXITOSAMENTE")
print(f"{'='*60}")
