import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo Excel
df = pd.read_excel('Proyecto BI/Encuesta_Vocacional_Completa.xlsx')

# ==================== RENOMBRAR COLUMNAS ====================
renombrar = {
    # Filtros
    'Género *': 'Genero',
    '¿Cuál es tu edad? *': 'Edad',
    '¿En qué grado estás actualmente? *': 'Grado',
    '¿En qué distrito o comunidad vives? *': 'Distrito',
    
    # Preguntas Sección 4: Accesibilidad y Oferta Educativa
    '¿Qué modalidad de estudio prefieres? *': 'Modalidad_Estudio',
    '¿Estarías dispuesto/a a mudarte a otra ciudad si en tu zona no existe la carrera que te interesa? *': 'Disposicion_Mudanza',
    '¿Qué tan definido tienes tu interés sobre qué estudiar después de la secundaria? *': 'Definicion_Interes',
    '¿Qué nivel de conocimiento tienes sobre las universidades, institutos o programas en tu zona? *': 'Conocimiento_Opciones',
    '¿En qué medida las opciones educativas cercanas coinciden con lo que quieres estudiar? *': 'Coincidencia_Opciones'
}

df = df.rename(columns=renombrar)

print("Columnas renombradas exitosamente:")
for old, new in renombrar.items():
    if old in df.columns or new in df.columns:
        print(f"  ✓ {new}")

# ==================== CONFIGURACIÓN DE FILTROS ====================
FILTROS = {
    # 'Genero': 'Femenino',           # Opciones: 'Femenino', 'Masculino'
    # 'Edad': '16',                   # Opciones: '16', '17', '18 a más'
    # 'Grado': '4°',                  # Opciones: '4°', '5°'
    # 'Distrito': 'San Luis',         # Opciones: 'San Luis', 'San Vicente', 'Imperial'
}

# ==================================================================

def aplicar_filtros(dataframe, filtros):
    """Aplica los filtros definidos al dataframe"""
    df_filtrado = dataframe.copy()
    filtros_aplicados = []
    
    for columna, valor in filtros.items():
        if columna in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado[columna] == valor]
            filtros_aplicados.append(f"{columna}={valor}")
    
    return df_filtrado, filtros_aplicados

def obtener_titulo_filtros(filtros_aplicados):
    """Genera un subtítulo con los filtros aplicados"""
    if not filtros_aplicados:
        return "Todos los estudiantes"
    return " | ".join(filtros_aplicados)

# Aplicar filtros
df_filtrado, filtros_aplicados = aplicar_filtros(df, FILTROS)
subtitulo_filtros = obtener_titulo_filtros(filtros_aplicados)

print("\n" + "=" * 60)
print(f"FILTROS APLICADOS: {subtitulo_filtros}")
print(f"Total de registros filtrados: {len(df_filtrado)}")
print(f"Total de registros originales: {len(df)}")
print("=" * 60)

# ==================== PREGUNTA 1: Modalidad de estudio ====================
print("\n1. MODALIDAD DE ESTUDIO PREFERIDA")
print("-" * 60)

columna_p1 = 'Modalidad_Estudio'
orden_p1 = ['Presencial', 'Virtual', 'Híbrido (presencial + virtual)', 'No tengo preferencia']

if columna_p1 in df_filtrado.columns:
    conteo_p1 = df_filtrado[columna_p1].value_counts().reindex(orden_p1, fill_value=0)
    
    # Crear gráfico de barras verticales con gradiente
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    
    x_pos = np.arange(len(orden_p1))
    colores = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
    
    bars = ax.bar(x_pos, conteo_p1.values, color=colores, alpha=0.9,
                  edgecolor='white', linewidth=2, width=0.7)
    
    # Añadir valores y porcentajes
    for i, (bar, val) in enumerate(zip(bars, conteo_p1.values)):
        if val > 0:
            pct = (val / conteo_p1.sum() * 100)
            ax.text(bar.get_x() + bar.get_width()/2., val + 1,
                   f'{int(val)}\n({pct:.1f}%)',
                   ha='center', va='bottom', fontsize=12, 
                   fontweight='bold', color='white')
    
    ax.set_xlabel('Modalidad de Estudio', fontsize=14, fontweight='bold', color='white')
    ax.set_ylabel('Cantidad de estudiantes', fontsize=14, fontweight='bold', color='white')
    ax.set_title(f'Modalidad de estudio preferida\n{subtitulo_filtros}', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    
    # Etiquetas del eje X más legibles
    labels_cortas = ['Presencial', 'Virtual', 'Híbrido', 'Sin preferencia']
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels_cortas, fontsize=11, fontweight='bold', color='white')
    
    ax.grid(axis='y', alpha=0.3, color='white', linestyle='--')
    ax.set_ylim(0, max(conteo_p1.values) * 1.15)
    
    # Personalizar spines
    for spine in ax.spines.values():
        spine.set_color('#333333')
    
    plt.tight_layout()
    plt.show()
    
    print(conteo_p1)
    print(f"Total: {conteo_p1.sum()}")
else:
    print("Columna no encontrada")

# ==================== PREGUNTA 2: Disposición a mudarse ====================
print("\n2. DISPOSICIÓN A MUDARSE POR ESTUDIOS")
print("-" * 60)

columna_p2 = 'Disposicion_Mudanza'
orden_p2 = ['Sí, sin problemas', 'Sí, pero solo si cuento con apoyo económico', 
           'No, prefiero estudiar otra carrera en mi zona', 'No lo sé aún']

if columna_p2 in df_filtrado.columns:
    conteo_p2 = df_filtrado[columna_p2].value_counts().reindex(orden_p2, fill_value=0)
    
    # Crear gráfico de dona mejorado
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    
    colores_p2 = ['#00ff88', '#ffd700', '#ff6b35', '#a78bfa']
    labels_cortas = ['Sí, sin problemas', 'Sí, con apoyo', 'No, otra carrera', 'No lo sé']
    
    wedges, texts, autotexts = ax.pie(conteo_p2.values, labels=None, autopct='',
                                        colors=colores_p2, startangle=90,
                                        counterclock=False,
                                        wedgeprops=dict(width=0.4, edgecolor='#0a0a0a', linewidth=3))
    
    # Círculo central
    circle = plt.Circle((0, 0), 0.6, color='#0a0a0a', linewidth=0)
    ax.add_artist(circle)
    
    # Texto central
    ax.text(0, 0.1, 'DISPOSICIÓN', ha='center', va='center', 
            fontsize=16, fontweight='bold', color='#666666')
    ax.text(0, -0.1, 'A MUDARSE', ha='center', va='center', 
            fontsize=16, fontweight='bold', color='#666666')
    ax.text(0, -0.3, f'{conteo_p2.sum()}', ha='center', va='center', 
            fontsize=32, fontweight='bold', color='white')
    
    # Título
    fig.text(0.5, 0.95, f'Disposición a mudarse por estudios\n{subtitulo_filtros}', 
             ha='center', va='top', fontsize=16, fontweight='bold', color='white')
    
    # Leyenda personalizada
    legend_y_start = -1.4
    for i, (label, val, color) in enumerate(zip(labels_cortas, conteo_p2.values, colores_p2)):
        y_pos = legend_y_start - (i * 0.15)
        circle_legend = plt.Circle((-0.8, y_pos), 0.05, color=color, transform=ax.transData)
        ax.add_patch(circle_legend)
        ax.text(-0.65, y_pos, label, ha='left', va='center', fontsize=12, 
                fontweight='bold', color='white', transform=ax.transData)
        pct = (val / conteo_p2.sum() * 100) if conteo_p2.sum() > 0 else 0
        ax.text(0.8, y_pos, f'{int(val)} ({pct:.1f}%)', ha='right', va='center', 
                fontsize=12, fontweight='bold', color=color, transform=ax.transData)
    
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-2.2, 1.2)
    
    plt.tight_layout()
    plt.show()
    
    print(conteo_p2)
    print(f"Total: {conteo_p2.sum()}")
else:
    print("Columna no encontrada")
# ==================== PREGUNTA 3: Definición del interés ====================
print("\n3. DEFINICIÓN DEL INTERÉS VOCACIONAL")
print("-" * 60)

columna_p3 = 'Definicion_Interes'
orden_p3 = ['Nada definido', 'Poco definido', 'Algo definido', 'Muy definido', 'Totalmente definido']

if columna_p3 in df_filtrado.columns:
    conteo_p3 = df_filtrado[columna_p3].value_counts().reindex(orden_p3, fill_value=0)
    
    # Crear gráfico de área con gradiente
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    
    x_pos = np.arange(len(orden_p3))
    color_principal = '#e74c3c'
    
    # Línea principal
    ax.plot(x_pos, conteo_p3.values, 'o-', linewidth=4, markersize=15,
            color=color_principal, markerfacecolor=color_principal, 
            markeredgecolor='white', markeredgewidth=3, zorder=3)
    
    # Área bajo la curva
    ax.fill_between(x_pos, 0, conteo_p3.values, alpha=0.3, color=color_principal, zorder=1)
    
    # Añadir valores
    for i, val in enumerate(conteo_p3.values):
        pct = (val / conteo_p3.sum() * 100) if conteo_p3.sum() > 0 else 0
        ax.text(i, val + 3, f'{int(val)}\n({pct:.1f}%)', ha='center', va='bottom',
                fontsize=11, fontweight='bold', color=color_principal,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#0a0a0a', 
                         edgecolor=color_principal, linewidth=2))
    
    ax.set_xlabel('Nivel de Definición', fontsize=14, fontweight='bold', color='white')
    ax.set_ylabel('Cantidad de estudiantes', fontsize=14, fontweight='bold', color='white')
    ax.set_title(f'Definición del interés vocacional\n{subtitulo_filtros}', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(orden_p3, fontsize=10, fontweight='bold', color='white', rotation=15)
    ax.grid(axis='y', alpha=0.3, color='white', linestyle='--')
    ax.set_ylim(0, max(conteo_p3.values) * 1.2)
    
    for spine in ax.spines.values():
        spine.set_color('#333333')
    
    plt.tight_layout()
    plt.show()
    
    print(conteo_p3)
    print(f"Total: {conteo_p3.sum()}")
else:
    print("Columna no encontrada")

# ==================== PREGUNTA 4: Conocimiento de opciones ====================
print("\n4. CONOCIMIENTO DE OPCIONES EDUCATIVAS")
print("-" * 60)

columna_p4 = 'Conocimiento_Opciones'
orden_p4 = ['No conozco ninguno', 'Conozco muy pocos', 'Conozco algunos', 
           'Conozco varios', 'Conozco muchas opciones']

if columna_p4 in df_filtrado.columns:
    conteo_p4 = df_filtrado[columna_p4].value_counts().reindex(orden_p4, fill_value=0)
    
    # Crear gráfico radar/spider
    fig = plt.figure(figsize=(11, 11))
    ax = fig.add_subplot(111, projection='polar')
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    ax.set_frame_on(False)
    
    n_vars = len(orden_p4)
    angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False)
    values = conteo_p4.values
    angles = np.concatenate((angles, [angles[0]]))
    values_plot = np.append(values, values[0])
    
    color_radar = '#3498db'
    
    # Dibujar el radar
    ax.plot(angles, values_plot, 'o-', linewidth=4, color=color_radar, 
            markersize=12, markerfacecolor=color_radar, markeredgecolor='white', 
            markeredgewidth=3)
    ax.fill(angles, values_plot, alpha=0.25, color=color_radar)
    
    # Configurar el radar
    max_val = max(values) if max(values) > 0 else 10
    ax.set_ylim(0, max_val * 1.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    
    # Etiquetas personalizadas
    labels_cortas = ['No conozco', 'Muy pocos', 'Algunos', 'Varios', 'Muchas opciones']
    label_distance = max_val * 1.4
    for angle, label in zip(angles[:-1], labels_cortas):
        ha = 'center'
        if 0 < angle < np.pi:
            ha = 'left'
        elif angle > np.pi:
            ha = 'right'
        ax.text(angle, label_distance, label, ha=ha, va='center', 
                fontsize=12, fontweight='bold', color='white')
    
    # Añadir valores en cada punto
    for angle, val in zip(angles[:-1], values):
        if val > 0:
            pct = (val / conteo_p4.sum() * 100) if conteo_p4.sum() > 0 else 0
            ax.text(angle, val + max_val * 0.1, f'{int(val)}\n({pct:.1f}%)', 
                   ha='center', va='center', fontsize=10, fontweight='bold', 
                   color=color_radar, bbox=dict(boxstyle='round,pad=0.3', 
                   facecolor='#0a0a0a', edgecolor=color_radar, alpha=0.8))
    
    # Configurar grid
    levels = np.linspace(0, max_val, 6)
    ax.set_yticks(levels)
    ax.set_yticklabels([f'{int(l)}' for l in levels], fontsize=9, color='#666666')
    ax.grid(color='#333333', linestyle='-', linewidth=1, alpha=0.7)
    
    # Título
    fig.text(0.5, 0.95, f'Conocimiento de opciones educativas locales\n{subtitulo_filtros}', 
             ha='center', va='top', fontsize=16, fontweight='bold', color='white')
    
    plt.subplots_adjust(top=0.88, bottom=0.12, left=0.1, right=0.9)
    plt.show()
    
    print(conteo_p4)
    print(f"Total: {conteo_p4.sum()}")
else:
    print("Columna no encontrada")

# ==================== PREGUNTA 5: Coincidencia de opciones ====================
print("\n5. COINCIDENCIA CON OPCIONES LOCALES")
print("-" * 60)

columna_p5 = 'Coincidencia_Opciones'
orden_p5 = ['No coinciden en nada', 'Coinciden muy poco', 'Coinciden parcialmente', 
           'Coinciden bastante', 'Coinciden totalmente']

if columna_p5 in df_filtrado.columns:
    conteo_p5 = df_filtrado[columna_p5].value_counts().reindex(orden_p5, fill_value=0)
    
    # Crear gráfico de barras horizontales con gradiente
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#0a0a0a')
    
    y_pos = np.arange(len(orden_p5))[::-1]
    colores = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
    
    # Barras horizontales
    bars = ax.barh(y_pos, conteo_p5.values, color=colores, alpha=0.9,
                   edgecolor='white', linewidth=2, height=0.6)
    
    # Añadir valores y porcentajes
    for i, (bar, val) in enumerate(zip(bars, conteo_p5.values)):
        if val > 0:
            pct = (val / conteo_p5.sum() * 100) if conteo_p5.sum() > 0 else 0
            ax.text(val + max(conteo_p5.values) * 0.02, bar.get_y() + bar.get_height()/2,
                   f'{int(val)} ({pct:.1f}%)', va='center', ha='left', 
                   fontsize=12, fontweight='bold', color='white')
    
    # Etiquetas del eje Y
    ax.set_yticks(y_pos)
    ax.set_yticklabels(orden_p5, fontsize=11, fontweight='bold', color='white')
    
    ax.set_xlabel('Cantidad de estudiantes', fontsize=14, fontweight='bold', color='white')
    ax.set_title(f'Coincidencia entre intereses y opciones locales\n{subtitulo_filtros}', 
                 fontsize=16, fontweight='bold', color='white', pad=20)
    
    ax.grid(axis='x', alpha=0.3, color='white', linestyle='--')
    ax.set_xlim(0, max(conteo_p5.values) * 1.25)
    
    for spine in ax.spines.values():
        spine.set_color('#333333')
    
    plt.tight_layout()
    plt.show()
    
    print(conteo_p5)
    print(f"Total: {conteo_p5.sum()}")
else:
    print("Columna no encontrada")

print("\n" + "=" * 60)
print("SECCIÓN 4: ACCESIBILIDAD Y OFERTA EDUCATIVA - COMPLETADA")
print("=" * 60)