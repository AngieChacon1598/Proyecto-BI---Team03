import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Obtener la ruta absoluta del directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta al archivo Excel
excel_path = os.path.join(script_dir, '..', 'data', 'RecopilaciónDeDatos-BI_T03.xlsx')

# Leer el archivo Excel
df = pd.read_excel(excel_path)

# ==================== RENOMBRAR COLUMNAS ====================
# Primero limpiamos los espacios en blanco de todas las columnas
df.columns = df.columns.str.strip()

renombrar = {
    # Filtros
    'Género': 'Genero',
    '¿Cuál es tu edad?': 'Edad',
    '¿En qué grado estás actualmente?': 'Grado',
    '¿En qué distrito vives?': 'Distrito',

    # Preguntas Sección 6: Proyecto de Vida y Expectativas Futuras
    'Al terminar el colegio, ¿cuál es tu principal plan a seguir?': 'Plan_Despues_Colegio',
    '¿Qué es lo más importante que buscas en tu futuro trabajo o profesión?': 'Importante_Trabajo_Futuro',
    '¿Qué papel crees que juega la educación superior (universitaria o técnica para alcanzar el futuro que deseas?': 'Papel_Educacion_Superior',
    'Pensando en 10 años, ¿cómo te gustaría que fuera tu estilo de vida?': 'Estilo_Vida_10_Anos',
    '¿Cuál consideras que es el mayor desafío o preocupación que enfrentas al pensar en tu futuro después del colegio?': 'Mayor_Desafio_Futuro'
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

# ==================== PREGUNTA 6.1: Plan después del colegio ====================
print("\n6.1. PLAN DESPUÉS DEL COLEGIO")
print("-" * 60)

columna_p6_1 = 'Plan_Despues_Colegio'
opciones_p6_1 = [
    'Ingresar a la universidad para estudiar una carrera profesional.',
    'Estudiar en un instituto una carrera técnica corta.',
    'Empezar a trabajar lo antes posible para tener independencia económica.',
    'Tomarme un tiempo para decidir qué quiero hacer o viajar.'
]

if columna_p6_1 in df_filtrado.columns:
    conteo_p6_1 = df_filtrado[columna_p6_1].value_counts().reindex(opciones_p6_1, fill_value=0)

    # Crear gráfico de barras horizontales apiladas
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    etiquetas_cortas = [
        'Ingresar a la universidad para estudiar\nuna carrera profesional',
        'Estudiar en un instituto una carrera\ntécnica corta',
        'Empezar a trabajar lo antes posible\npara tener independencia económica',
        'Tomarme un tiempo para decidir\nqué quiero hacer o viajar'
    ]

    # Leyenda para las categorías
    leyenda = ['Cuarto', 'Quinto']
    colores_barra = ['#8b5cf6', '#d4a017']  # Morado y amarillo/dorado

    y_pos = np.arange(len(etiquetas_cortas))
    bar_height = 0.5

    # Calcular conteos por grado
    if 'Grado' in df_filtrado.columns:
        conteo_4to = []
        conteo_5to = []
        for opcion in opciones_p6_1:
            df_4to = df_filtrado[df_filtrado['Grado'] == '4°']
            df_5to = df_filtrado[df_filtrado['Grado'] == '5°']
            conteo_4to.append(len(df_4to[df_4to[columna_p6_1] == opcion]))
            conteo_5to.append(len(df_5to[df_5to[columna_p6_1] == opcion]))

        # Crear barras apiladas horizontales
        left_pos = np.zeros(len(etiquetas_cortas))

        # Barras de 4to (morado)
        bars1 = ax.barh(y_pos, conteo_4to, bar_height, left=left_pos,
                       color=colores_barra[0], label='Cuarto', alpha=0.9)

        # Agregar porcentajes en barras de 4to
        for i, (val, pos) in enumerate(zip(conteo_4to, y_pos)):
            if val > 0:
                total = conteo_4to[i] + conteo_5to[i]
                pct = (val / total * 100) if total > 0 else 0
                ax.text(left_pos[i] + val/2, pos, f'{pct:.0f}%',
                       va='center', ha='center', fontsize=13, fontweight='bold', color='white')

        left_pos = np.array(conteo_4to)

        # Barras de 5to (amarillo/dorado)
        bars2 = ax.barh(y_pos, conteo_5to, bar_height, left=left_pos,
                       color=colores_barra[1], label='Quinto', alpha=0.9)

        # Agregar porcentajes en barras de 5to
        for i, (val, pos) in enumerate(zip(conteo_5to, y_pos)):
            if val > 0:
                total = conteo_4to[i] + conteo_5to[i]
                pct = (val / total * 100) if total > 0 else 0
                ax.text(left_pos[i] + val/2, pos, f'{pct:.0f}%',
                       va='center', ha='center', fontsize=13, fontweight='bold', color='white')
    else:
        # Si no hay columna Grado, mostrar barras simples
        bars = ax.barh(y_pos, conteo_p6_1.values, bar_height, color='#8b5cf6', alpha=0.9)
        for i, (val, pos) in enumerate(zip(conteo_p6_1.values, y_pos)):
            if val > 0:
                pct = (val / conteo_p6_1.sum() * 100)
                ax.text(val/2, pos, f'{pct:.0f}%',
                       va='center', ha='center', fontsize=13, fontweight='bold', color='white')

    # Configurar etiquetas del eje Y (a la izquierda de las barras)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(etiquetas_cortas, fontsize=11, color='white', ha='right')
    ax.tick_params(axis='y', pad=10)

    # Título
    ax.set_title('Plan después del Colegio', fontsize=20, fontweight='bold',
                color='white', pad=20, loc='left')

    # Leyenda
    ax.legend(loc='upper right', framealpha=0.9, fontsize=12, facecolor='#2a2a3e', edgecolor='white')

    # Quitar bordes y configurar grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_xticks([])
    ax.grid(axis='x', alpha=0.1, color='white')

    # Ajustar márgenes para que se vean bien las etiquetas
    plt.subplots_adjust(left=0.3, right=0.95, top=0.93, bottom=0.07)
    plt.show()

    print(conteo_p6_1)
    print(f"Total: {conteo_p6_1.sum()}")
else:
    print("Columna no encontrada")

# ==================== PREGUNTA 6.2: Lo más importante en trabajo futuro ====================
print("\n6.2. LO MÁS IMPORTANTE EN TRABAJO FUTURO")
print("-" * 60)

columna_p6_2 = 'Importante_Trabajo_Futuro'
opciones_p6_2 = [
    'Estabilidad económica y un buen sueldo.',
    'Prestigio y reconocimiento en mi campo laboral.',
    'Poder ayudar a los demás y tener un impacto positivo en la sociedad.',
    'Un buen balance entre mi vida personal y el trabajo, con tiempo para mis pasatiempos.'
]

if columna_p6_2 in df_filtrado.columns:
    conteo_p6_2 = df_filtrado[columna_p6_2].value_counts().reindex(opciones_p6_2, fill_value=0)

    # Crear gráfico de barras verticales con gradiente
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor('#0f0f23')
    ax.set_facecolor('#0f0f23')

    etiquetas_cortas = ['Estabilidad\neconómica', 'Prestigio y\nreconocimiento',
                       'Poder ayudar a\nlos demás', 'Balance en\nla vida']

    x_pos = np.arange(len(etiquetas_cortas))

    # Colores con gradiente (de rosa/morado a cyan)
    colores_gradiente = ['#e91e8c', '#22c55e', '#f97316', '#eab308']

    # Calcular conteos por grado si existe la columna
    if 'Grado' in df_filtrado.columns:
        # Leyenda
        leyenda_labels = ['4to de Secundaria', '5to de Secundaria']
        leyenda_colors = ['#60a5fa', '#22d3ee']

        # Crear elementos para la leyenda manualmente
        legend_elements = [plt.Rectangle((0,0),1,1, fc=leyenda_colors[0], label=leyenda_labels[0]),
                          plt.Rectangle((0,0),1,1, fc=leyenda_colors[1], label=leyenda_labels[1])]
        ax.legend(handles=legend_elements, loc='upper right', framealpha=0.9,
                 fontsize=11, facecolor='#1a1a3e', edgecolor='white')

    bars = ax.bar(x_pos, conteo_p6_2.values, width=0.6, color=colores_gradiente,
                  alpha=0.95, edgecolor='none')

    # Agregar efecto de gradiente con sombras
    for i, (bar, color) in enumerate(zip(bars, colores_gradiente)):
        bar.set_edgecolor(color)
        bar.set_linewidth(2)

        # Agregar porcentaje arriba de la barra
        val = conteo_p6_2.values[i]
        if val > 0:
            pct = (val / conteo_p6_2.sum() * 100)
            ax.text(bar.get_x() + bar.get_width()/2, val + max(conteo_p6_2.values)*0.02,
                   f'{pct:.0f}%', ha='center', va='bottom',
                   fontsize=14, fontweight='bold', color=color)

    # Configuración de ejes
    ax.set_xticks(x_pos)
    ax.set_xticklabels(etiquetas_cortas, fontsize=12, fontweight='bold', color='white')
    ax.set_ylim(0, max(conteo_p6_2.values) * 1.15)

    # Título
    ax.set_title('Lo más importante en un trabajo futuro',
                fontsize=18, fontweight='bold', color='white', pad=20, loc='left')

    # Quitar bordes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Grid sutil
    ax.grid(axis='y', alpha=0.15, color='white', linestyle='-', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_yticks([])

    plt.tight_layout()
    plt.show()

    print(conteo_p6_2)
    print(f"Total: {conteo_p6_2.sum()}")
else:
    print("Columna no encontrada")

# ==================== PREGUNTA 6.3: Papel de la educación superior ====================
print("\n6.3. PAPEL DE LA EDUCACIÓN SUPERIOR")
print("-" * 60)

columna_p6_3 = 'Papel_Educacion_Superior'
opciones_p6_3 = [
    'Es fundamental y la única vía para asegurar el éxito profesional y personal.',
    'Es muy importante, pero creo que la experiencia y las habilidades prácticas son igual de valiosas.',
    'Es solo un requisito formal, pero no garantiza el éxito.',
    'No es tan necesaria; hay otras formas de alcanzar mis metas sin estudios superiores.'
]

if columna_p6_3 in df_filtrado.columns:
    conteo_p6_3 = df_filtrado[columna_p6_3].value_counts().reindex(opciones_p6_3, fill_value=0)

    # Crear gráfico tipo donut con categorías
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor('#0f0f23')
    ax.set_facecolor('#0f0f23')

    # Colores para cada categoría (del azul al verde)
    colores_p6_3 = ['#3b82f6', '#22c55e', '#f97316', '#8b5cf6']

    # Crear el gráfico de dona
    wedges, texts = ax.pie(conteo_p6_3.values, labels=None,
                           colors=colores_p6_3, startangle=45,
                           counterclock=False,
                           wedgeprops=dict(width=0.4, edgecolor='#0f0f23', linewidth=4))

    # Círculo interior para hacer el efecto donut
    circle = plt.Circle((0, 0), 0.6, color='#0f0f23', linewidth=0)
    ax.add_artist(circle)

    # Texto central
    ax.text(0, 0.05, '¿Qué tan', ha='center', va='center',
            fontsize=14, fontweight='normal', color='#ef4444')
    ax.text(0, -0.05, 'importante es la', ha='center', va='center',
            fontsize=14, fontweight='normal', color='#ef4444')
    ax.text(0, -0.15, 'educación?', ha='center', va='center',
            fontsize=14, fontweight='normal', color='#ef4444')

    # Título
    fig.text(0.5, 0.96, 'Papel de la Educación Superior',
             ha='center', va='top', fontsize=18, fontweight='bold', color='white')

    # Leyenda con iconos y valores
    etiquetas_leyenda = ['Es fundamental', 'Es muy importante', 'Es solo un requisito', 'No es tan necesaria']
    numeros_visuales = ['01', '02', '03', '04']

    # Leyenda para grados
    if 'Grado' in df_filtrado.columns:
        legend_labels = ['4to de Secundaria', '5to de Secundaria']
        legend_colors = ['#60a5fa', '#22d3ee']

        # Posicionar leyenda de grados en la parte superior derecha
        legend_y = 0.88
        for i, (label, color) in enumerate(zip(legend_labels, legend_colors)):
            circle_legend = plt.Circle((0.72, legend_y - i*0.05), 0.015, color=color,
                                     transform=fig.transFigure)
            fig.add_artist(circle_legend)
            fig.text(0.75, legend_y - i*0.05, label, ha='left', va='center',
                    fontsize=10, color='white', transform=fig.transFigure)

    # Añadir etiquetas con números y valores alrededor del donut
    legend_start_x = 0.15
    legend_start_y = 0.72
    legend_spacing = 0.18

    for i, (num, label, val, color) in enumerate(zip(numeros_visuales, etiquetas_leyenda,
                                                     conteo_p6_3.values, colores_p6_3)):
        y_pos = legend_start_y - (i * legend_spacing)

        # Número de categoría
        fig.text(legend_start_x, y_pos + 0.02, num, ha='center', va='center',
                fontsize=16, fontweight='bold', color=color,
                transform=fig.transFigure,
                bbox=dict(boxstyle='circle,pad=0.3', facecolor=color,
                         edgecolor='white', linewidth=2))

        # Etiqueta de categoría
        fig.text(legend_start_x + 0.05, y_pos + 0.02, label, ha='left', va='center',
                fontsize=11, fontweight='bold', color='white', transform=fig.transFigure)

        # Valor y porcentaje
        pct = (val / conteo_p6_3.sum() * 100) if conteo_p6_3.sum() > 0 else 0
        fig.text(legend_start_x + 0.05, y_pos - 0.02, f'{int(val)} estudiantes ({pct:.0f}%)',
                ha='left', va='center',
                fontsize=9, color='#888888', transform=fig.transFigure)

        # Gráfico de barras pequeñas a la derecha
        bar_x = 0.75
        bar_width = pct / 100 * 0.15
        bar_y = y_pos + 0.005
        bar_height = 0.01

        rect = plt.Rectangle((bar_x, bar_y), bar_width, bar_height,
                            transform=fig.transFigure,
                            facecolor=color, edgecolor='none', alpha=0.8)
        fig.add_artist(rect)

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)

    plt.tight_layout()
    plt.show()

    print(conteo_p6_3)
    print(f"Total: {conteo_p6_3.sum()}")
else:
    print("Columna no encontrada")

# ==================== PREGUNTA 6.4: Estilo de vida en 10 años ====================
print("\n6.4. ESTILO DE VIDA EN 10 AÑOS")
print("-" * 60)

columna_p6_4 = 'Estilo_Vida_10_Anos'
opciones_p6_4 = [
    'Con una vida estable, una casa propia y seguridad financiera.',
    'Con libertad para viajar por el mundo y vivir diferentes experiencias.',
    'Liderando mi propio negocio o siendo un profesional independiente.',
    'Dedicado/a a mi desarrollo profesional, ocupando un alto cargo en una empresa.'
]

if columna_p6_4 in df_filtrado.columns:
    conteo_p6_4 = df_filtrado[columna_p6_4].value_counts().reindex(opciones_p6_4, fill_value=0)

    # Crear figura con gráficos circulares de porcentaje
    fig = plt.figure(figsize=(16, 6))
    fig.patch.set_facecolor('#0f0f23')

    # Título principal
    fig.text(0.5, 0.95, 'Estilo de vida en 10 años', ha='center', va='top',
            fontsize=20, fontweight='bold', color='white')

    # Leyenda de grados
    if 'Grado' in df_filtrado.columns:
        legend_labels = ['4to de Secundaria', '5to de Secundaria']
        legend_colors = ['#60a5fa', '#22d3ee']

        legend_y = 0.88
        for i, (label, color) in enumerate(zip(legend_labels, legend_colors)):
            circle_legend = plt.Circle((0.45 + i*0.1, legend_y), 0.008, color=color,
                                     transform=fig.transFigure)
            fig.add_artist(circle_legend)
            fig.text(0.46 + i*0.1, legend_y, label, ha='left', va='center',
                    fontsize=10, color='white', transform=fig.transFigure)

    etiquetas_cortas = ['Una vida estable', 'Viajar por el mundo',
                       'Negocio propio', 'Cargo alto en una empresa']

    # Crear 4 gráficos circulares
    positions = [(0.15, 0.35), (0.38, 0.35), (0.61, 0.35), (0.84, 0.35)]
    color_circle = '#22c55e'  # Verde

    total = conteo_p6_4.sum()

    for idx, (pos_x, etiqueta, valor) in enumerate(zip(positions, etiquetas_cortas, conteo_p6_4.values)):
        # Calcular porcentaje
        pct = (valor / total * 100) if total > 0 else 0

        # Crear subplot para cada círculo
        ax = fig.add_axes([pos_x[0]-0.08, pos_x[1]-0.15, 0.16, 0.35])
        ax.set_facecolor('#0f0f23')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')

        # Círculo de fondo (gris)
        circle_bg = plt.Circle((0, 0), 1, color='#2a2a3e', linewidth=8, fill=False)
        ax.add_patch(circle_bg)

        # Círculo de progreso (verde)
        # Crear arco usando wedge
        theta = 360 * (pct / 100)
        wedge = plt.matplotlib.patches.Wedge((0, 0), 1.08, 90-theta, 90,
                                             width=0.16, facecolor=color_circle,
                                             edgecolor='none')
        ax.add_patch(wedge)

        # Texto del porcentaje en el centro
        ax.text(0, 0.1, f'{pct:.0f}%', ha='center', va='center',
               fontsize=28, fontweight='bold', color=color_circle)

        # Etiqueta debajo del círculo
        ax.text(0, -1.45, etiqueta, ha='center', va='top',
               fontsize=11, fontweight='bold', color='white',
               wrap=True, bbox=dict(boxstyle='round,pad=0.5',
                                   facecolor=color_circle,
                                   edgecolor='white', linewidth=1.5, alpha=0.3))

    plt.show()

    print(conteo_p6_4)
    print(f"Total: {conteo_p6_4.sum()}")
else:
    print("Columna no encontrada")

# ==================== PREGUNTA 6.5: Mayor desafío futuro ====================
print("\n6.5. MAYOR DESAFÍO FUTURO")
print("-" * 60)

columna_p6_5 = 'Mayor_Desafio_Futuro'
opciones_p6_5 = [
    'La dificultad económica para poder costear mis estudios o proyectos.',
    'La indecisión sobre qué carrera o camino profesional elegir.',
    'La alta competencia en el campo laboral y el miedo a no encontrar trabajo.',
    'La presión de mi familia o de la sociedad sobre lo que "debería" hacer.'
]

if columna_p6_5 in df_filtrado.columns:
    conteo_p6_5 = df_filtrado[columna_p6_5].value_counts().reindex(opciones_p6_5, fill_value=0)
    etiquetas_cortas = ['Dificultad\nEconómica', 'Indecisión sobre\nla carrera',
                       'Alta competencia\nlaboral', 'Presión familiar']

    # Crear gráfico de barras verticales agrupadas por grado
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor('#0f0f23')
    ax.set_facecolor('#0f0f23')

    x = np.arange(len(etiquetas_cortas))
    width = 0.35  # Ancho de las barras

    # Calcular conteos por grado
    if 'Grado' in df_filtrado.columns:
        conteo_4to = []
        conteo_5to = []
        for opcion in opciones_p6_5:
            df_4to = df_filtrado[df_filtrado['Grado'] == '4°']
            df_5to = df_filtrado[df_filtrado['Grado'] == '5°']
            conteo_4to.append(len(df_4to[df_4to[columna_p6_5] == opcion]))
            conteo_5to.append(len(df_5to[df_5to[columna_p6_5] == opcion]))

        # Colores para 4to y 5to
        color_4to = '#60a5fa'  # Azul
        color_5to = '#22d3ee'  # Cyan

        # Crear barras
        bars1 = ax.bar(x - width/2, conteo_4to, width, label='4° Grado',
                      color=color_4to, alpha=0.9, edgecolor='none')
        bars2 = ax.bar(x + width/2, conteo_5to, width, label='5° Grado',
                      color=color_5to, alpha=0.9, edgecolor='none')

        # Agregar valores sobre las barras
        for bars, valores in [(bars1, conteo_4to), (bars2, conteo_5to)]:
            for bar, val in zip(bars, valores):
                if val > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, val + 1,
                           f'{int(val)}',
                           ha='center', va='bottom', fontsize=11,
                           fontweight='bold', color='white')

        # Agregar porcentajes debajo de cada par de barras
        for i, (v4, v5) in enumerate(zip(conteo_4to, conteo_5to)):
            total = v4 + v5
            if total > 0:
                pct4 = (v4 / total * 100)
                pct5 = (v5 / total * 100)

                # Porcentaje para 4to
                ax.text(x[i] - width/2, -3, f'{pct4:.0f}%',
                       ha='center', va='top', fontsize=10,
                       fontweight='bold', color=color_4to)

                # Porcentaje para 5to
                ax.text(x[i] + width/2, -3, f'{pct5:.0f}%',
                       ha='center', va='top', fontsize=10,
                       fontweight='bold', color=color_5to)

        # Leyenda
        ax.legend(loc='upper right', framealpha=0.9, fontsize=12,
                 facecolor='#1a1a3e', edgecolor='white')
    else:
        # Si no hay columna Grado, mostrar barras simples
        colores_p6_5 = ['#60a5fa', '#3b82f6', '#10b981', '#ef4444']
        bars = ax.bar(x, conteo_p6_5.values, color=colores_p6_5, alpha=0.9,
                     edgecolor='none')

        for bar, val in zip(bars, conteo_p6_5.values):
            if val > 0:
                pct = (val / conteo_p6_5.sum() * 100)
                ax.text(bar.get_x() + bar.get_width()/2, val + 1,
                       f'{int(val)}\n({pct:.0f}%)',
                       ha='center', va='bottom', fontsize=11,
                       fontweight='bold', color='white')

    # Configuración de ejes
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas_cortas, fontsize=11, fontweight='bold', color='white')
    ax.set_ylim(-8, max(max(conteo_4to if 'Grado' in df_filtrado.columns else conteo_p6_5.values),
                        max(conteo_5to if 'Grado' in df_filtrado.columns else conteo_p6_5.values)) * 1.2)

    # Título
    ax.set_title('Mayor desafío en el Futuro', fontsize=18, fontweight='bold',
                color='white', pad=20, loc='left')

    # Quitar bordes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Grid sutil
    ax.grid(axis='y', alpha=0.15, color='white', linestyle='-', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_yticks([])

    plt.tight_layout()
    plt.show()

    print(conteo_p6_5)
    print(f"Total: {conteo_p6_5.sum()}")
else:
    print("Columna no encontrada")

print("\n" + "=" * 60)
print("ANÁLISIS SECCIÓN 6 COMPLETADO")
print("=" * 60)
